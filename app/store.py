from __future__ import annotations

import uuid
from collections import defaultdict
from datetime import date, timedelta
from typing import Dict, List, Optional

from .models import (
    Channel,
    Circle,
    Contact,
    Event,
    Interaction,
    MessageTone,
    Reminder,
    ReminderReason,
    RelationshipHealth,
)


class InMemoryStore:
    def __init__(self) -> None:
        self.contacts: Dict[uuid.UUID, Contact] = {}
        self.circles: Dict[uuid.UUID, Circle] = {}
        self.events: Dict[uuid.UUID, Event] = {}
        self.interactions: Dict[uuid.UUID, Interaction] = {}
        self.contact_to_circles: Dict[uuid.UUID, List[uuid.UUID]] = defaultdict(list)

    def add_circle(self, name: str, description: str | None = None) -> uuid.UUID:
        circle = Circle(name=name, description=description)
        self.circles[circle.id] = circle
        return circle.id

    def list_circles(self) -> List[Circle]:
        return list(self.circles.values())

    def update_circle(self, circle_id: uuid.UUID, name: str, description: Optional[str]) -> Circle:
        circle = self.circles[circle_id]
        updated = circle.model_copy(update={"name": name, "description": description})
        self.circles[circle_id] = updated
        return updated

    def delete_circle(self, circle_id: uuid.UUID) -> None:
        self.circles.pop(circle_id, None)
        for contact_id, circle_ids in list(self.contact_to_circles.items()):
            if circle_id in circle_ids:
                self.contact_to_circles[contact_id] = [c for c in circle_ids if c != circle_id]

    def add_contact(self, contact: Contact) -> Contact:
        self.contacts[contact.id] = contact
        for circle_id in contact.circles:
            self.contact_to_circles[contact.id].append(circle_id)
        return contact

    def update_contact(self, contact_id: uuid.UUID, data: dict) -> Contact:
        contact = self.contacts[contact_id]
        updated = contact.model_copy(update=data)
        self.contacts[contact_id] = updated
        if "circles" in data:
            self.contact_to_circles[contact_id] = list(data.get("circles", []))
        return updated

    def delete_contact(self, contact_id: uuid.UUID) -> None:
        self.contacts.pop(contact_id, None)
        self.contact_to_circles.pop(contact_id, None)
        for event_id, event in list(self.events.items()):
            if event.contact_id == contact_id:
                self.events.pop(event_id, None)
        for interaction_id, interaction in list(self.interactions.items()):
            if interaction.contact_id == contact_id:
                self.interactions.pop(interaction_id, None)

    def add_event(self, event: Event) -> Event:
        self.events[event.id] = event
        return event

    def list_events_for_contact(self, contact_id: uuid.UUID) -> List[Event]:
        return [event for event in self.events.values() if event.contact_id == contact_id]

    def add_interaction(self, interaction: Interaction) -> Interaction:
        if interaction.channel == Channel.call and interaction.duration_minutes is None:
            interaction.duration_minutes = 1
        self.interactions[interaction.id] = interaction
        contact = self.contacts[interaction.contact_id]
        if contact.last_contact is None or interaction.occurred_at > contact.last_contact:
            contact.last_contact = interaction.occurred_at
            self.contacts[interaction.contact_id] = contact
        return interaction

    def list_interactions_for_contact(self, contact_id: uuid.UUID) -> List[Interaction]:
        return [value for value in self.interactions.values() if value.contact_id == contact_id]

    def list_contacts_for_circle(self, circle_id: uuid.UUID) -> List[Contact]:
        return [
            contact
            for contact_id, circle_ids in self.contact_to_circles.items()
            if circle_id in circle_ids
            for contact in [self.contacts.get(contact_id)]
            if contact is not None
        ]

    def generate_reminders(self, window_days: int = 7) -> List[Reminder]:
        today = date.today()
        reminders: List[Reminder] = []

        for contact in self.contacts.values():
            last_contact_date = contact.last_contact.date() if contact.last_contact else None
            desired_frequency = timedelta(days=contact.desired_frequency_days)
            if last_contact_date:
                overdue_date = last_contact_date + desired_frequency
                if overdue_date <= today:
                    reminders.append(
                        Reminder(
                            contact_id=contact.id,
                            reason=ReminderReason.overdue_contact,
                            due_date=overdue_date,
                            message=f"Reach out to {contact.name}; cadence is overdue.",
                        )
                    )
            else:
                reminders.append(
                    Reminder(
                        contact_id=contact.id,
                        reason=ReminderReason.overdue_contact,
                        due_date=today,
                        message=f"Introduce yourself to {contact.name}; no interactions logged yet.",
                    )
                )

            for event in self.list_events_for_contact(contact.id):
                days_until_event = (event.date - today).days
                if 0 <= days_until_event <= window_days:
                    reminders.append(
                        Reminder(
                            contact_id=contact.id,
                            reason=ReminderReason.upcoming_event,
                            due_date=event.date,
                            message=f"{event.label or event.type.title()} for {contact.name} on {event.date.isoformat()}.",
                            related_event_id=event.id,
                        )
                    )

        return reminders

    def contact_timeline(self, contact_id: uuid.UUID) -> List[dict]:
        entries: List[dict] = []
        for event in self.list_events_for_contact(contact_id):
            entries.append(
                {
                    "type": "event",
                    "timestamp": event.date.isoformat(),
                    "label": event.label or event.type.value,
                }
            )
        for interaction in self.list_interactions_for_contact(contact_id):
            entries.append(
                {
                    "type": "interaction",
                    "timestamp": interaction.occurred_at.isoformat(),
                    "channel": interaction.channel.value,
                    "note": interaction.note,
                }
            )
        return sorted(entries, key=lambda item: item["timestamp"], reverse=True)

    def health_for_contact(self, contact: Contact) -> RelationshipHealth:
        if contact.last_contact:
            days_since = (date.today() - contact.last_contact.date()).days
        else:
            days_since = None
        overdue_by = None
        if days_since is not None:
            overdue_by = days_since - contact.desired_frequency_days
            overdue_by = overdue_by if overdue_by > 0 else 0
        score = 100
        if days_since is None:
            score = 40
        elif overdue_by and overdue_by > 0:
            score = max(10, 100 - min(70, overdue_by * 2))
        elif days_since > 0:
            score = max(40, 100 - min(40, int(days_since / max(contact.desired_frequency_days, 1) * 30)))

        channels = {interaction.channel.value for interaction in self.list_interactions_for_contact(contact.id)}
        diversity_bonus = min(len(channels) * 5, 15)
        score = min(score + diversity_bonus, 100)

        status = "healthy"
        if score < 40:
            status = "at_risk"
        elif score < 70:
            status = "drifting"

        return RelationshipHealth(
            contact_id=contact.id,
            score=int(score),
            status=status,
            days_since_last_contact=days_since,
            overdue_by_days=overdue_by,
            interaction_channels=sorted(list(channels)),
        )

    def search(self, query: str) -> dict:
        lowered = query.lower()
        contacts = [
            c
            for c in self.contacts.values()
            if lowered in c.name.lower() or any(lowered in tag.lower() for tag in c.tags)
        ]
        events = [e for e in self.events.values() if (e.label and lowered in e.label.lower())]
        interactions = [i for i in self.interactions.values() if i.note and lowered in i.note.lower()]

        related_contact_ids = {e.contact_id for e in events}.union({i.contact_id for i in interactions})
        for contact_id in related_contact_ids:
            contact = self.contacts.get(contact_id)
            if contact and contact not in contacts:
                contacts.append(contact)

        return {"contacts": contacts, "events": events, "interactions": interactions}

    def generate_message_draft(
        self,
        contact: Optional[Contact],
        occasion: str,
        tone: MessageTone = MessageTone.warm,
        context: Optional[str] = None,
    ) -> str:
        name = contact.name if contact else "there"
        base_messages = {
            "birthday": f"Happy birthday, {name}! I hope you celebrate with something that makes you smile.",
            "check_in": f"Hi {name}, it's been a bit—how have you been?",
            "congratulations": f"Congratulations, {name}! I'm really happy for you and wanted to reach out.",
            "sympathy": f"Hi {name}, I'm thinking of you and wanted to offer support if you need anything.",
        }
        message = base_messages.get(occasion, f"Hi {name}, wanted to say hello and catch up soon.")
        if context:
            message += f" Also, {context}."

        tone_additions = {
            MessageTone.professional: "Keeping it brief—let me know when you have time to connect.",
            MessageTone.short: "Just a quick note to send good vibes!",
            MessageTone.playful: "Let's make something fun happen soon!",
        }
        if tone in tone_additions:
            message = f"{message} {tone_additions[tone]}".strip()
        return message


def seed_default_circles(store: InMemoryStore) -> None:
    for name in ("Family", "Close Friends", "Work", "Clients"):
        store.add_circle(name)
