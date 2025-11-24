# Reminder-App

This repository now includes a lightweight FastAPI backend that begins implementing the CircleAI requirements described in [`docs/SRS.md`](docs/SRS.md).

## Project Overview
- **Platforms:** Backend API to power iOS, Android, and Web clients described in the SRS.
- **Core Goals:** Track important dates and interactions, generate thoughtful AI-assisted messages, and recommend when and how to reconnect—while prioritizing privacy and consent.
- **Capabilities in this scaffold:**
  - Default circle seeding (Family, Close Friends, Work, Clients) with Circle CRUD and listings by circle.
  - CRUD endpoints for contacts, events, and interactions plus per-contact timelines.
  - Daily digest endpoint that surfaces overdue contacts and upcoming events within a configurable window and optional cap.
  - Stay-in-touch and relationship-health helpers per contact.
  - Search across contacts, events, and interactions.
  - AI-like message draft generation with tone controls for common occasions.

## Getting Started
1. Install dependencies (ideally in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
2. Run the API locally:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Explore the interactive docs at `http://127.0.0.1:8000/docs`.

## Tests
Run the automated checks:
```bash
python -m pytest
```

## Next Steps
- Swap the in-memory store for a real database layer (PostgreSQL) and background job queue as outlined in the SRS.
- Add authentication, consent recording, and integration connectors (Google, Microsoft, device contacts, messaging providers).
- Extend the AI layer to draft messages and scheduling suggestions as specified in the SRS.
- Add notification scheduling, snooze workflows, and weekly digest emails.
