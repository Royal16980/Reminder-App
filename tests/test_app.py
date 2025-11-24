from datetime import date, datetime, timedelta, timezone

from fastapi.testclient import TestClient

from app.main import app, store
from app.models import Channel, Contact, Event, EventType, Interaction, MessageTone

client = TestClient(app)


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def reset_store():
    store.contacts.clear()
    store.events.clear()
    store.interactions.clear()
    store.contact_to_circles.clear()


def test_contact_workflow_generates_reminders():
    reset_store()

    contact = Contact(name="Ada Lovelace", desired_frequency_days=7)
    create_response = client.post("/contacts", json=contact.model_dump(mode="json"))
    assert create_response.status_code == 201
    contact_id = create_response.json()["id"]

    event = Event(
        contact_id=contact.id,
        date=date.today() + timedelta(days=2),
        label="Birthday",
        type=EventType.birthday,
    )
    event_response = client.post(
        f"/contacts/{contact_id}/events", json=event.model_dump(mode="json")
    )
    assert event_response.status_code == 201

    interaction = Interaction(
        contact_id=contact.id,
        occurred_at=datetime.now(timezone.utc) - timedelta(days=10),
        channel=Channel.email,
        note="Checked in",
    )
    interaction_response = client.post(
        f"/contacts/{contact_id}/interactions", json=interaction.model_dump(mode="json")
    )
    assert interaction_response.status_code == 201

    digest_response = client.get("/digest/today")
    digest = digest_response.json()
    assert digest_response.status_code == 200
    reasons = {item["reason"] for item in digest["reminders"]}
    assert "overdue_contact" in reasons
    assert "upcoming_event" in reasons


def test_message_draft_is_personalized_and_toned():
    reset_store()
    contact = Contact(name="Grace Hopper")
    client.post("/contacts", json=contact.model_dump(mode="json"))

    draft_response = client.post(
        "/messages/draft",
        params={"contact_id": str(contact.id), "occasion": "birthday", "tone": MessageTone.playful.value},
    )
    assert draft_response.status_code == 201
    payload = draft_response.json()
    assert "Grace Hopper" in payload["message"]
    assert payload["tone"] == MessageTone.playful.value


def test_health_and_timeline_reflect_interactions():
    reset_store()
    contact = Contact(name="Linus Torvalds", desired_frequency_days=3)
    client.post("/contacts", json=contact.model_dump(mode="json"))

    interaction = Interaction(
        contact_id=contact.id,
        occurred_at=datetime.now(timezone.utc) - timedelta(days=1),
        channel=Channel.call,
        duration_minutes=5,
    )
    client.post(
        f"/contacts/{contact.id}/interactions", json=interaction.model_dump(mode="json")
    )

    health_response = client.get(f"/contacts/{contact.id}/health")
    health = health_response.json()["health"]
    assert health_response.status_code == 200
    assert health["status"] == "healthy"

    timeline_response = client.get(f"/contacts/{contact.id}/timeline")
    assert timeline_response.status_code == 200
    timeline = timeline_response.json()["timeline"]
    assert any(item["type"] == "interaction" for item in timeline)


def test_search_surfaces_events_and_notes():
    reset_store()
    contact = Contact(name="Ada Byron", tags=["math"]) 
    client.post("/contacts", json=contact.model_dump(mode="json"))
    event = Event(contact_id=contact.id, date=date.today(), label="Graduation", type=EventType.custom)
    client.post(f"/contacts/{contact.id}/events", json=event.model_dump(mode="json"))
    interaction = Interaction(contact_id=contact.id, channel=Channel.note, note="Loves analytical engines")
    client.post(
        f"/contacts/{contact.id}/interactions", json=interaction.model_dump(mode="json")
    )

    response = client.get("/search", params={"q": "engine"})
    assert response.status_code == 200
    results = response.json()
    assert len(results["contacts"]) >= 1
    assert len(results["interactions"]) >= 1
