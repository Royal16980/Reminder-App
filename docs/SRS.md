# CircleAI Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose
CircleAI is an AI-powered relationship calendar that helps people stay in touch with important contacts (family, friends, coworkers, clients) by:
- Tracking important dates (birthdays, anniversaries, milestones).
- Monitoring gaps in communication.
- Generating thoughtful messages and prompts.
- Suggesting and scheduling calls, meetups, and check-ins.
- Providing a “relationship health” view of social circles.

The app integrates with calendars, contacts, email, messaging apps, and (optionally) call logs to reduce the mental load of keeping in touch.

### 1.2 Scope
Product type: Mobile app (iOS/Android) and Web app, with backend services and integrations.

Key capabilities:
- Import and organize contacts into Circles.
- Automatically detect and track important events (birthdays, anniversaries, work milestones, etc.).
- Maintain a timeline of interactions per contact (calls, messages, meetings, notes).
- Run a “stay-in-touch” engine that surfaces who to contact, when, and why.
- Use AI to draft messages (e.g., birthday wishes, check-ins, congratulations) for review or auto-send.
- Suggest meetings/dates/catch-ups by scanning calendars and proposing times.
- Provide daily/weekly digests of upcoming dates and people to connect with.
- Respect strict privacy and consent for all data sources, with user control over access and usage.

### 1.3 Stakeholders and Users
- **End Users:**
  - Everyday individuals who want to remember birthdays and keep up with friends/family.
  - Busy professionals/executives maintaining networks.
  - Freelancers/creators using it as a lightweight personal CRM.
- **Stakeholders:**
  - Product owner/founder.
  - Engineering team.
  - Privacy and legal teams (GDPR, CCPA compliance).
  - Third-party integration partners (Google, Microsoft, Apple, WhatsApp, etc.).

## 2. System Context and Integrations

### 2.1 External Systems
1. **Calendars**
   - Google Calendar
   - Microsoft Outlook / Microsoft 365
   - Apple Calendar (via device/iCloud)
2. **Contacts and Social Graph**
   - Phone address book (iOS/Android)
   - Google Contacts
   - Microsoft People
   - (Later) LinkedIn API / other network sources
3. **Communication Channels**
   - Email: Gmail, Outlook, IMAP
   - SMS (via device or carrier APIs where possible)
   - WhatsApp / WhatsApp Business API
   - Telegram
   - (Optional) Slack / Teams for work contacts
4. **Call Logs (optional, high-consent)**
   - Device call history: incoming/outgoing calls (timestamp, contact, duration)
5. **Device and OS APIs**
   - Push notifications
   - Local storage and secure keychain
   - Background activity (sync and reminders)

## 3. Core Concepts and Data Objects
- **User** – The person using CircleAI.
- **Contact** – A person the user may want to stay in touch with.
- **Circle** – A group of contacts (e.g., Family, Close Friends, Work – Team A).
- **Relationship Profile** – Aggregated info about a contact: tags, last contact, interaction frequency, notes, preferences.
- **Event** – A date associated with a contact: birthday, anniversary, work anniversary, kids’ birthdays, etc.
- **Interaction** – Any meaningful touchpoint (call, message, meeting, note).
- **Reminder/Nudge** – A generated prompt to reach out or to acknowledge an upcoming date.
- **Message Draft** – AI-generated text ready to be reviewed or auto-sent.
- **Preference/Boundary** – User settings around how often to contact, what channels to use, auto-send rules, quiet hours, etc.

## 4. Functional Requirements

### 4.1 Contact and Circle Management
- **FR-1.1** Import contacts from selected sources (phone, Google, Microsoft) with explicit user consent.
- **FR-1.2** Allow users to manually add/edit/delete contacts.
- **FR-1.3** Support Circles:
  - Create, edit, delete circles.
  - Assign contacts to one or more circles.
  - Default circles: Family, Close Friends, Work, Clients.
- **FR-1.4** Allow tagging and rating relationship priority (e.g., “VIP”, “Inner Circle”, “Acquaintance”).
- **FR-1.5** Maintain a merged profile for a contact even if they appear in multiple sources (phone + email + calendar).

### 4.2 Event and Date Management
- **FR-2.1** Automatically detect birthdays from:
  - Contacts (birthday field).
  - Emails (e.g., “Happy birthday” repeated annually).
  - Social or imported sources (where allowed).
- **FR-2.2** Support manual creation and editing of:
  - Birthdays.
  - Anniversaries.
  - Work anniversaries.
  - Custom dates (e.g., “Graduation day”, “Sobriety anniversary”).
- **FR-2.3** Sync user calendars to detect:
  - Past and upcoming meetings with contacts.
  - Important milestones (e.g., recurring 1:1s, project launches).
- **FR-2.4** Show a chronological timeline of events for each contact.

### 4.3 Stay-in-Touch Engine
- **FR-3.1** Calculate a “last meaningful contact” date for each contact by analyzing:
  - Calls (duration above threshold).
  - Direct messages/emails.
  - In-person/online meetings.
- **FR-3.2** Allow users to configure desired contact frequency per contact or circle (e.g., “every 2 weeks”, “every 3 months”).
- **FR-3.3** Generate nudges when:
  - Time since last contact exceeds desired frequency.
  - An important date is approaching (e.g., birthday in 7 days).
  - A long gap is detected with previously frequent contacts.
- **FR-3.4** Let users snooze nudges, mark them as done, and adjust frequency based on fatigue (e.g., “too many nudges about X, reduce frequency”).
- **FR-3.5** Provide a daily “People to connect with” list (max items per day configurable).

### 4.4 AI Message Generation
- **FR-4.1** Generate message drafts for birthdays, anniversaries, check-ins, congratulations, and sympathy/support.
- **FR-4.2** Support multiple tones: warm/casual, professional, short & direct, playful (where permitted).
- **FR-4.3** Personalize messages using name/pronouns, past interaction notes, known interests, and context from last interaction.
- **FR-4.4** Never auto-send messages by default; initial configuration is manual review only.
- **FR-4.5** Allow per-contact or per-circle auto-send toggles with clear warnings and logs.
- **FR-4.6** Display previews and allow users to edit drafts, regenerate variants, and save custom templates.

### 4.5 Scheduling Calls, Meetings, and Meetups
- **FR-5.1** Propose call/meeting suggestions based on shared free calendar slots, user preferred windows, and contact locale/timezone (where known).
- **FR-5.2** Generate “Suggest a time” messages for email/WhatsApp/etc. or create a scheduling link.
- **FR-5.3** Support one-click creation of calendar events (with invite) and “call reminder” events with contact details.
- **FR-5.4** For groups (e.g., circles), suggest candidate time slots, generate a poll link (external or internal), and provide a message template.

### 4.6 Interaction Logging
- **FR-6.1** Log interactions from email (threads, subject, timestamp), calendar (meetings, attendees), call logs (number, duration), SMS/WhatsApp/Telegram (metadata by default; optional content analysis with explicit consent).
- **FR-6.2** Allow manual logging (e.g., “We had coffee today, talked about X” and quick notes such as “Loves Arsenal and Ethiopian food”).
- **FR-6.3** Provide search across contacts, notes, events, and topics (e.g., “Who did I talk to about [topic]?”).

### 4.7 Relationship Insights and Dashboards
- **FR-7.1** Home screen shows today’s/tomorrow’s important dates, people to reach out to today, and upcoming events within the next 7/30 days.
- **FR-7.2** Relationship Health score per contact and circle based on frequency vs. target, recency of contact, and diversity of interaction types.
- **FR-7.3** Highlight “drifting relationships” (once-close contacts now quiet) and “over-contacted” relationships (nudges could be reduced).

### 4.8 Notifications and Digests
- **FR-8.1** Send daily digest notifications (configurable time) summarizing today’s occasions, top people to contact, and quick suggestions/message drafts.
- **FR-8.2** Send weekly review emails or in-app summaries (connections made, new relationships added, upcoming key dates).
- **FR-8.3** Respect user quiet hours, Do Not Disturb modes, and notification preferences per channel (push, email, SMS).

### 4.9 Privacy, Security, and Consent (Functional)
- **FR-9.1** Present clear consent screens for each integration (calendar, email, call logs, messaging).
- **FR-9.2** Provide granular toggles for read-only vs. send-on-your-behalf, content vs. metadata access, and inclusion/exclusion of circles/contacts.
- **FR-9.3** Offer data export and full account delete options.
- **FR-9.4** Maintain an activity log for messages sent on the user’s behalf, calendar events created, and changes to auto-send rules.

## 5. Non-Functional Requirements

### 5.1 Performance
- Generate message drafts within a few seconds of user action.
- Ensure daily digests and reminders are ready at scheduled times.
- Use incremental and efficient sync with external providers.

### 5.2 Reliability and Availability
- Target SaaS-grade uptime (specific SLOs to be defined later).
- Provide graceful degradation when an integration is temporarily unavailable (e.g., show stale but marked data).

### 5.3 Security
- Use HTTPS/TLS for all communication with external services.
- Encrypt sensitive data at rest (e.g., AES-256).
- Rely on token-based access (OAuth2) for external providers.
- Where feasible, separate storage of tokens from main data.

### 5.4 Privacy and Compliance
- Align data handling with GDPR/CCPA.
- Minimize data retention; store only what is necessary.
- Offer options to keep certain notes local to the device (if supported).
- Do not use user data for training external models without explicit opt-in.

### 5.5 Usability and Accessibility
- Mobile-first design with responsive web version.
- Aim for WCAG 2.1 AA for core flows where possible.
- Provide simple onboarding: choose circles, connect data sources, set initial contact frequencies.

### 5.6 Internationalization
- Support multiple languages for UI and message templates.
- Handle multiple timezones, date formats, and locales.

## 6. High-Level Data Model (Conceptual)

### 6.1 Entities
- User
- Contact
- Circle
- Event (contact-specific or global)
- Interaction
- Reminder
- MessageDraft
- Template
- IntegrationAccount
- ConsentRecord

### 6.2 Relations
- User 1–N Circle
- Circle N–M Contact
- Contact 1–N Event
- Contact 1–N Interaction
- User 1–N Reminder
- User 1–N IntegrationAccount

## 7. Constraints and Assumptions
- User has at least one supported calendar.
- Some integrations may be read-only initially (e.g., email).
- Mobile OSes may limit continuous access to call logs/SMS; behavior may vary by platform.
- Users may be highly sensitive to privacy; UX must be trust-first and transparent.

## 8. Product Development Plan (PDP)

### 8.1 Product Vision
CircleAI helps you be the person who remembers and shows up: an AI calendar and companion focused on the humans in your life.

Positioning vs. current market:
- Personal CRMs (Monica, Clay, Covve, Queue, etc.) focus on organizing contacts and reminders for networking.
- AI calendars (Toki, Clockwise, Akiflow, etc.) focus on time optimization and work tasks.
- Family organizers (e.g., Gether) focus on shared schedules and parenting logistics.

CircleAI’s unique focus: relationship-centric AI calendar that treats connections as the primary object, not just events.

### 8.2 Target Users and Jobs-To-Be-Done
- **Persona 1: The Overloaded Professional**
  - Long work hours; forgets birthdays and friend catch-ups.
  - JTBD: “Help me maintain my relationships without needing to remember everything.”
- **Persona 2: The Network-Builder**
  - Consultant, freelancer, or founder.
  - JTBD: “Help me stay warm with my network and never miss key moments.”
- **Persona 3: The Relationship-Guardian**
  - Values family and long-term friendships.
  - JTBD: “Help me be more intentional: remember milestones, check in, and schedule time together.”

### 8.3 Roadmap – Phases and Scope

**Phase 0 – Discovery and Foundations**
- 10–20 user interviews across personas.
- Map out privacy red lines and must-haves.
- Decide initial platforms (likely: web + iOS, then Android).
- Design core user flows (onboarding, Today screen, contact profile, draft-and-send flow).
- Deliverables: UX prototypes (Figma or similar), prioritized backlog, data protection impact assessment outline.

**Phase 1 – MVP: “Never Miss Birthdays and Check-Ins”**
- Goal: Deliver a lean product that imports contacts (phone + Google), detects birthdays/key dates, provides simple stay-in-touch reminders, and drafts messages without auto-send.
- Included features:
  - Basic onboarding: connect contacts and one calendar; create core circles (Family, Friends, Work).
  - Birthday and custom date tracking.
  - Manual frequency settings per circle (e.g., “Family – every 2 weeks”).
  - Daily “People to contact today” view.
  - AI-generated drafts for birthday messages and generic check-ins.
  - Manual send via copy/paste or email integration (send from user email).
  - Core privacy controls: clear permissions, easy revocation/disconnect.
- Success criteria (MVP):
  - % of onboarded users connecting at least one data source.
  - % of daily active users sending at least one message/week via CircleAI.
  - Qualitative feedback: “This helped me remember and reach out.”

**Phase 2 – V1: Smart Cadence and Light Automation**
- Goal: Make CircleAI more proactive and useful while remaining trust-first.
- New capabilities: per-contact frequency tuning, insights dashboard (losing touch, weekly relationships), scheduling suggestions via calendar integrations, deeper Gmail/Outlook logging, saved templates and custom tones, optional auto-send for birthdays with explicit opt-in, weekly email summary/plan.

**Phase 3 – Pro Features and “Circles of Life”**
- Goal: Move toward premium offering and advanced use cases.
- New capabilities: advanced analytics (relationship health per circle, top contacted vs least), optional call log integration, SMS/WhatsApp integration for one-tap send (and in-app send where allowed), group scheduling suggestions and poll links, nuanced AI (gift ideas, conversation prompts), work mode with light CRM features (leads, clients, deal stage tags).
- Monetization options:
  - Free tier: birthdays, basic reminders, limited AI drafts.
  - Pro tier: multiple integrations, advanced analytics, auto-send, group features.

### 8.4 Technical Architecture (High-Level)
- **Frontend:** React Native or Flutter for cross-platform mobile; React/Next.js for web.
- **Backend:** Node.js (TypeScript) or Python (FastAPI); PostgreSQL for relational data; Redis for caching.
- **Background jobs:** Queue system (e.g., BullMQ, Celery) for daily digests, syncing integrations, reminder generation.
- **AI Layer:** LLM API (e.g., OpenAI GPT-5.x) with prompt templates per use case (birthday, check-in, sympathy), guardrails for safety/tone, and optional fine-tuning or structured prompts.
- **Integrations:** Google Workspace APIs (Calendar, People, Gmail); Microsoft Graph (Calendar, People, Email); device contacts and call logs via native permissions; messaging APIs (WhatsApp, Telegram, Twilio SMS, email providers).

### 8.5 Team and Roles
- Product Lead/Founder: Vision, roadmap, prioritization, stakeholder management.
- Tech Lead/Architect: Technical decisions, integration strategies, security.
- Backend Engineer(s): APIs, data model, integrations, job queues.
- Mobile/Frontend Engineer(s): iOS/Android apps, web dashboard.
- AI/Prompt Engineer: Message templates, safety filters, personalization strategies.
- Designer (UX/UI): Flows, visual identity, interaction design.
- Privacy and Legal Advisor: Consent flows, data processing agreements, policies.
- Customer Success/Support: Early user onboarding, feedback loops.

### 8.6 Metrics and Analytics
- **Activation:** % of new users connecting ≥1 integration; % completing onboarding (creating circles, selecting frequencies).
- **Engagement:** Daily/weekly active users; messages drafted per user per week; nudges acted on vs. ignored.
- **Outcome-focused:** Increase in distinct contacts reached per month; reduced “involuntary drift” (long gaps).
- **Satisfaction:** NPS/in-app rating; quick surveys (“Did this message feel like you?”).
- **Trust:** Opt-outs and permission revocations; support tickets related to privacy concerns.

### 8.7 Risks and Mitigations
1. **Privacy/Security Concerns**
   - Mitigation: privacy-first branding; clear consent; minimal data access by default; strong encryption; easily accessible privacy controls.
2. **Platform Dependency (APIs changing)**
   - Mitigation: abstraction layer for integrations; monitoring; fallbacks and graceful degradation.
3. **AI Hallucinations/Inappropriate Messaging**
   - Mitigation: manual review by default; filters for tone/language/sensitive topics; never auto-send without explicit per-contact opt-in.
4. **Notification Fatigue**
   - Mitigation: tunable frequency; “I’m overwhelmed” control to auto-reduce nudges; smart batching into daily digest instead of constant pushes.
5. **Over-Automation/Feeling Inauthentic**
   - Mitigation: emphasize co-writing (AI drafts, user finalizes); personalization sliders (formality, length); encourage adding a personal line before sending.

### 8.8 Immediate Next Steps
1. Refine product narrative and naming (lock the name/tagline and single-sentence description).
2. Design core user flows (onboarding, Today screen, contact profile, draft and send flow).
3. Pick initial integrations (e.g., Google Calendar + Google Contacts + Gmail).
4. Define an MVP experiment for 1–2 personas: “Never forget birthdays again, and send thoughtful, AI-assisted messages in 10 seconds.”
5. Run user testing with 5–10 target users to validate that reminders and AI drafts feel helpful, not intrusive.
