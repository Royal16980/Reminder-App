from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

from .models import (
    Circle,
    Contact,
    Event,
    Interaction,
    MessageDraft,
    MessageTone,
)
from .store import InMemoryStore, seed_default_circles

app = FastAPI(title="CircleAI Reminder Service", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = InMemoryStore()
seed_default_circles(store)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/circles")
def list_circles() -> dict:
    return {"circles": store.list_circles()}


@app.post("/circles", status_code=201)
def create_circle(circle: Circle) -> Circle:
    circle_id = store.add_circle(circle.name, circle.description)
    return store.circles[circle_id]


@app.get("/circles/{circle_id}")
def get_circle(circle_id: uuid.UUID) -> Circle:
    try:
        return store.circles[circle_id]
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Circle not found") from exc


@app.put("/circles/{circle_id}")
def update_circle(circle_id: uuid.UUID, circle: Circle) -> Circle:
    if circle_id not in store.circles:
        raise HTTPException(status_code=404, detail="Circle not found")
    return store.update_circle(circle_id, name=circle.name, description=circle.description)


@app.delete("/circles/{circle_id}", status_code=204)
def delete_circle(circle_id: uuid.UUID) -> Response:
    if circle_id not in store.circles:
        raise HTTPException(status_code=404, detail="Circle not found")
    store.delete_circle(circle_id)
    return Response(status_code=204)


@app.get("/contacts")
def list_contacts() -> List[Contact]:
    return list(store.contacts.values())


@app.post("/contacts", status_code=201)
def create_contact(contact: Contact) -> Contact:
    for circle_id in contact.circles:
        if circle_id not in store.circles:
            raise HTTPException(status_code=400, detail="Circle not found for contact assignment")
    store.add_contact(contact)
    return contact


@app.get("/contacts/{contact_id}")
def get_contact(contact_id: uuid.UUID) -> Contact:
    try:
        return store.contacts[contact_id]
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Contact not found") from exc


@app.put("/contacts/{contact_id}")
def update_contact(contact_id: uuid.UUID, contact: Contact) -> Contact:
    if contact_id not in store.contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    for circle_id in contact.circles:
        if circle_id not in store.circles:
            raise HTTPException(status_code=400, detail="Circle not found for contact assignment")
    store.update_contact(contact_id, contact.model_dump())
    return store.contacts[contact_id]


@app.delete("/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: uuid.UUID) -> Response:
    if contact_id not in store.contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    store.delete_contact(contact_id)
    return Response(status_code=204)


@app.post("/contacts/{contact_id}/events", status_code=201)
def add_event(contact_id: uuid.UUID, event: Event) -> Event:
    if contact_id not in store.contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    if event.contact_id != contact_id:
        raise HTTPException(status_code=400, detail="Event contact_id mismatch")
    store.add_event(event)
    return event


@app.get("/contacts/{contact_id}/events")
def list_contact_events(contact_id: uuid.UUID) -> List[Event]:
    if contact_id not in store.contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    return store.list_events_for_contact(contact_id)


@app.post("/contacts/{contact_id}/interactions", status_code=201)
def log_interaction(contact_id: uuid.UUID, interaction: Interaction) -> Interaction:
    if contact_id not in store.contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    if interaction.contact_id != contact_id:
        raise HTTPException(status_code=400, detail="Interaction contact_id mismatch")
    return store.add_interaction(interaction)


@app.get("/contacts/{contact_id}/interactions")
def list_contact_interactions(contact_id: uuid.UUID) -> List[Interaction]:
    if contact_id not in store.contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    return store.list_interactions_for_contact(contact_id)


@app.get("/circles/{circle_id}/contacts")
def list_contacts_for_circle(circle_id: uuid.UUID) -> dict:
    if circle_id not in store.circles:
        raise HTTPException(status_code=404, detail="Circle not found")
    return {"contacts": store.list_contacts_for_circle(circle_id)}


@app.get("/digest/today")
def daily_digest(window_days: int = 7, limit: int | None = None) -> dict:
    reminders = store.generate_reminders(window_days=window_days)
    if limit:
        reminders = reminders[:limit]
    return {"count": len(reminders), "reminders": reminders}


@app.get("/stay-in-touch/{contact_id}")
def stay_in_touch_status(contact_id: uuid.UUID) -> dict:
    if contact_id not in store.contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact = store.contacts[contact_id]
    if contact.last_contact is None:
        return {"contact_id": contact_id, "status": "no_interactions", "due_in_days": 0}
    days_since_contact = (datetime.now(timezone.utc).date() - contact.last_contact.date()).days
    remaining = contact.desired_frequency_days - days_since_contact
    return {
        "contact_id": contact_id,
        "status": "on_track" if remaining > 0 else "overdue",
        "due_in_days": max(remaining, 0),
    }


@app.get("/contacts/{contact_id}/timeline")
def contact_timeline(contact_id: uuid.UUID) -> dict:
    if contact_id not in store.contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"timeline": store.contact_timeline(contact_id)}


@app.get("/contacts/{contact_id}/health")
def relationship_health(contact_id: uuid.UUID) -> dict:
    if contact_id not in store.contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact = store.contacts[contact_id]
    return {"health": store.health_for_contact(contact)}


@app.get("/search")
def search_entities(q: str) -> dict:
    return store.search(q)


@app.post("/messages/draft", status_code=201)
def create_message_draft(
    contact_id: uuid.UUID | None = None,
    occasion: str = "check_in",
    tone: MessageTone = MessageTone.warm,
    context: str | None = None,
) -> MessageDraft:
    contact = store.contacts.get(contact_id) if contact_id else None
    if contact_id and contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    message = store.generate_message_draft(contact, occasion=occasion, tone=tone, context=context)
    return MessageDraft(contact_id=contact_id, message=message, tone=tone, occasion=occasion)
