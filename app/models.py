from __future__ import annotations

import enum
import uuid
from datetime import date, datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field


class Priority(str, enum.Enum):
    vip = "vip"
    inner_circle = "inner_circle"
    regular = "regular"
    acquaintance = "acquaintance"


class Contact(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    circles: List[uuid.UUID] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    priority: Priority = Priority.regular
    desired_frequency_days: int = 30
    last_contact: Optional[datetime] = None
    timezone: Optional[str] = None


class Circle(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    description: Optional[str] = None


class MessageTone(str, enum.Enum):
    warm = "warm"
    professional = "professional"
    short = "short"
    playful = "playful"


class MessageDraft(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    contact_id: Optional[uuid.UUID] = None
    message: str
    tone: MessageTone = MessageTone.warm
    occasion: str


class EventType(str, enum.Enum):
    birthday = "birthday"
    anniversary = "anniversary"
    work_anniversary = "work_anniversary"
    custom = "custom"


class Event(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    contact_id: uuid.UUID
    date: date
    label: Optional[str] = None
    type: EventType = EventType.custom


class Channel(str, enum.Enum):
    email = "email"
    sms = "sms"
    call = "call"
    meeting = "meeting"
    note = "note"


class Interaction(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    contact_id: uuid.UUID
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    channel: Channel
    note: Optional[str] = None
    duration_minutes: Optional[int] = None


class ReminderReason(str, enum.Enum):
    overdue_contact = "overdue_contact"
    upcoming_event = "upcoming_event"


class Reminder(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    contact_id: uuid.UUID
    reason: ReminderReason
    due_date: date
    message: str
    related_event_id: Optional[uuid.UUID] = None


class RelationshipHealth(BaseModel):
    contact_id: uuid.UUID
    score: int
    status: str
    days_since_last_contact: Optional[int]
    overdue_by_days: Optional[int]
    interaction_channels: List[str]
