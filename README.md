
# Reminder-App
A simple reminder app

Software Requirements Specification (SRS)

1.1 Purpose

CircleAI is an AI-powered relationship calendar that helps users stay in touch with the important people in their lives (family, friends, coworkers, clients). It does this by:
	•	Tracking important dates (birthdays, anniversaries, milestones)
	•	Monitoring gaps in communication
	•	Generating thoughtful messages and prompts
	•	Suggesting and scheduling calls, meetups, and check-ins
	•	Providing a “relationship health” view of your social circles

It integrates with calendars, contacts, email, messaging apps, and (optionally) call logs to reduce the mental load of remembering to keep in touch.

1.2 Scope

Product type: Mobile app (iOS / Android) + Web app, with backend services and integrations.

Key capabilities:
	•	Import & organize contacts into Circles
	•	Automatically detect and track important events (birthdays, anniversaries, work milestones, etc.)
	•	Maintain a timeline of interactions per contact: calls, messages, meetings, notes (personal CRM style).  ￼
	•	Run a “stay-in-touch” engine that surfaces who you should contact, when, and why
	•	Use AI to draft messages (e.g., birthday wishes, check-ins, congratulations) for review or auto-send
	•	Suggest meetings / dates / catch-up calls by scanning everyone’s calendars and proposing times  ￼
	•	Provide daily/weekly digests of upcoming dates and people to connect with (similar to family/organizer assistants)  ￼
	•	Respect strict privacy and consent for all data sources, with user control over what’s accessed and how it’s used (inspired by privacy-first personal AIs like Kin).  ￼

1.3 Stakeholders & Users
	•	End Users
	•	Everyday individuals wanting to remember birthdays and keep up with friends/family.
	•	Busy professionals / executives who need to maintain networks.
	•	Freelancers/creators using it as a light-weight personal CRM.
	•	Stakeholders
	•	Product owner / founder
	•	Engineering team
	•	Privacy & legal (GDPR, CCPA compliance)
	•	Third-party integration partners (Google, Microsoft, Apple, WhatsApp, etc.)

⸻

2. System Context & Integrations

2.1 External Systems

CircleAI will integrate with:
	1.	Calendars
	•	Google Calendar
	•	Microsoft Outlook / Microsoft 365
	•	Apple Calendar (via device / iCloud)
	2.	Contacts & Social Graph
	•	Phone address book (iOS/Android)
	•	Google Contacts
	•	Microsoft People
	•	(Later) LinkedIn API / other network sources
	3.	Communication Channels
	•	Email: Gmail, Outlook, IMAP
	•	SMS (via device or carrier APIs where possible)
	•	WhatsApp / WhatsApp Business API
	•	Telegram
	•	(Optional) Slack / Teams for work contacts
	4.	Call Logs (optional, high-consent)
	•	Device call history: incoming/outgoing calls (timestamp, contact, duration)
	5.	Device & OS APIs
	•	Push notifications
	•	Local storage and secure keychain
	•	Background activity (sync & reminders)

⸻

3. Core Concepts & Data Objects
	•	User – The person using CircleAI.
	•	Contact – A person the user may want to stay in touch with.
	•	Circle – A group of contacts (e.g., Family, Close Friends, Work – Team A).
	•	Relationship Profile – Aggregated info about a contact: tags, last contact, interaction frequency, notes, preferences.
	•	Event – A date associated with a contact: birthday, anniversary, work anniversary, kids’ birthdays, etc.
	•	Interaction – Any meaningful touchpoint (call, message, meeting, note).
	•	Reminder / Nudge – A generated prompt to reach out or to acknowledge an upcoming date.
	•	Message Draft – AI-generated text ready to be reviewed or auto-sent.
	•	Preference / Boundary – User settings around how often to contact, what channels to use, auto-send rules, quiet hours, etc.

⸻

4. Functional Requirements

4.1 Contact & Circle Management

FR-1.1 The system shall import contacts from selected sources (phone, Google, Microsoft) with explicit user consent.

FR-1.2 The system shall allow the user to manually add/edit/delete contacts.

FR-1.3 The system shall support Circles:
	•	Create, edit, delete circles
	•	Assign contacts to one or more circles
	•	Default circles: Family, Close Friends, Work, Clients

FR-1.4 The system shall allow tagging and rating relationship priority (e.g., “VIP”, “Inner Circle”, “Acquaintance”).

FR-1.5 The system shall maintain a merged profile for a contact even if they appear in multiple sources (phone + email + calendar).

⸻

4.2 Event & Date Management

FR-2.1 The system shall automatically detect birthdays from:
	•	Contacts (birthday field)
	•	Emails (e.g., “Happy birthday” repeated annually)
	•	Social or imported sources (where allowed)

FR-2.2 The system shall allow manual creation and editing of:
	•	Birthdays
	•	Anniversaries
	•	Work anniversaries
	•	Custom dates (e.g., “Graduation day”, “Sobriety anniversary”)

FR-2.3 The system shall sync user’s calendars to detect:
	•	Past & upcoming meetings with contacts
	•	Important milestones (e.g., recurring 1:1s, project launches)  ￼

FR-2.4 The system shall show a chronological timeline of events for each contact.

⸻

4.3 Stay-in-Touch Engine

FR-3.1 The system shall calculate a “last meaningful contact” date for each contact by analyzing:
	•	Calls (duration above threshold)
	•	Direct messages / emails
	•	In-person / online meetings

FR-3.2 The system shall allow the user to configure desired contact frequency per contact or circle (e.g., “every 2 weeks”, “every 3 months”). Personal CRM tools commonly provide stay-in-touch reminders; CircleAI should match and improve on this baseline.  ￼

FR-3.3 The system shall generate nudges when:
	•	The time since last contact > desired frequency
	•	An important date is approaching (e.g., birthday in 7 days)
	•	A long gap is detected with previously frequent contacts

FR-3.4 The system shall allow users to:
	•	Snooze nudges
	•	Mark them as done (after contact)
	•	Adjust frequency based on fatigue (e.g., “too many nudges about X, reduce frequency”).

FR-3.5 The system shall provide a daily “People to connect with” list (max items per day configurable).

⸻

4.4 AI Message Generation

FR-4.1 The system shall generate message drafts for:
	•	Birthdays
	•	Anniversaries
	•	Check-in messages (“Hey, it’s been a while…”)
	•	Congratulations (promotions, new job, achievements)
	•	Sympathy/support messages (sensitive tone)

FR-4.2 The system shall support multiple tones:
	•	Warm / casual
	•	Professional
	•	Short & direct
	•	Playful (where user permits)

FR-4.3 The system shall personalize messages using:
	•	Name, pronouns
	•	Past interaction notes
	•	Known interests (where stored)
	•	Context from last interaction (e.g., “How did the move go?”)

FR-4.4 The system shall never auto-send messages by default. Initial configuration must be manual review-only.

FR-4.5 The system shall allow per-contact or per-circle auto-send toggles with clear warnings and logs.

FR-4.6 The system shall display a preview and allow the user to:
	•	Edit the draft
	•	Regenerate variants
	•	Save custom templates

⸻

4.5 Scheduling Calls, Meetings & Meetups

FR-5.1 The system shall propose call or meeting suggestions based on:
	•	Shared free calendar slots (for users whose calendars can be read)
	•	User’s preferred windows (e.g., evenings, weekends)
	•	Contact’s locale/timezone (where known)  ￼

FR-5.2 The system shall generate a “Suggest a time” message that can be sent via email/WhatsApp etc., or create a scheduling link.

FR-5.3 The system shall allow one-click creation of:
	•	Calendar events (with invite)
	•	“Call reminder” events with contact details attached

FR-5.4 For groups (e.g., “Uni Friends” circle), the system shall:
	•	Suggest a few candidate time slots
	•	Generate a poll link (external or internal) and message template

⸻

4.6 Interaction Logging

FR-6.1 The system shall log interactions from:
	•	Email (threads, subject, timestamp)
	•	Calendar (meetings, attendees)
	•	Call logs (number, duration)
	•	SMS/WhatsApp/Telegram (metadata only by default; optional content analysis with explicit consent)

FR-6.2 The system shall allow manual logging:
	•	“We had coffee today, talked about X”
	•	Quick notes (e.g., “Loves Arsenal and Ethiopian food”)

FR-6.3 The system shall offer search across:
	•	Contacts
	•	Notes
	•	Events
	•	“Who did I talk to about [topic]?”

⸻

4.7 Relationship Insights & Dashboards

FR-7.1 The system shall provide a Home screen including:
	•	Today’s / tomorrow’s important dates
	•	People to reach out to today
	•	Upcoming events within next 7/30 days

FR-7.2 The system shall provide a Relationship Health score per contact and circle, based on:
	•	Frequency vs. target
	•	Recency of contact
	•	Diversity of interaction types (not just likes on IG, but calls, messages, meets)

FR-7.3 The system shall highlight:
	•	“Drifting relationships” – once-close contacts now quiet
	•	“Over-contacted” – where nudges could be reduced

⸻

4.8 Notifications & Digests

FR-8.1 The system shall send daily digest notifications (time configurable) summarizing:
	•	Today’s occasions
	•	Top X people to contact
	•	Quick suggestions & message drafts

FR-8.2 The system shall send weekly review emails or in-app summaries:
	•	How many people you connected with
	•	New relationships added
	•	Coming week’s key dates

FR-8.3 The system shall respect:
	•	User quiet hours
	•	Do Not Disturb modes
	•	Notification preferences per channel (push, email, SMS)

⸻

4.9 Privacy, Security & Consent (Functional)

FR-9.1 The system shall present clear consent screens for each integration (calendar, email, call logs, messaging).

FR-9.2 The system shall allow granular toggles:
	•	Read-only vs send-on-your-behalf
	•	Access to message content vs metadata-only
	•	Which circles/contacts to include or exclude

FR-9.3 The system shall provide a data export and full account delete option.

FR-9.4 The system shall provide an activity log:
	•	Messages sent on user’s behalf
	•	Calendar events created
	•	Changes to auto-send rules

⸻

5. Non-Functional Requirements

5.1 Performance
	•	Generate message drafts within a few seconds of user action.
	•	Daily digests and reminders should be ready at scheduled times.
	•	Sync with external providers must be incremental and efficient.

5.2 Reliability & Availability
	•	Target high uptime (e.g., SaaS-grade; specific SLOs defined later).
	•	Graceful degradation when an integration is temporarily unavailable (e.g., show stale but marked data).

5.3 Security
	•	All communication with external services via HTTPS/TLS.
	•	Encryption of sensitive data at rest (e.g., AES-256).
	•	Token-based access (OAuth2) for external providers.
	•	Separate storage of tokens from main data where feasible.

5.4 Privacy & Compliance
	•	GDPR/CCPA-aligned data handling and consent.
	•	Minimal data retention: only store what is necessary for the service.
	•	Option to keep certain notes only local to device (if supported).
	•	No use of user data for training external models without explicit opt-in.

5.5 Usability & Accessibility
	•	Mobile-first design with responsive web version.
	•	WCAG 2.1 AA for core flows where possible.
	•	Simple onboarding wizard:
	•	Choose circles
	•	Connect data sources
	•	Set initial contact frequencies

5.6 Internationalization
	•	Support multiple languages for UI and message templates.
	•	Handle multiple timezones, date formats, and locales.

⸻

6. High-Level Data Model (Conceptual)

Entities (simplified):
	•	User
	•	Contact
	•	Circle
	•	Event (contact-specific or global)
	•	Interaction
	•	Reminder
	•	MessageDraft
	•	Template
	•	IntegrationAccount
	•	ConsentRecord

Relations:
	•	User 1–N Circle
	•	Circle N–M Contact
	•	Contact 1–N Event
	•	Contact 1–N Interaction
	•	User 1–N Reminder
	•	User 1–N IntegrationAccount

⸻

7. Constraints & Assumptions
	•	User has at least one supported calendar.
	•	Some integrations may be read-only initially (e.g., email).
	•	Mobile OSes may limit continuous access to call logs / SMS; behavior may vary by platform.
	•	Users may be highly sensitive to privacy; UX must be trust-first and transparent.

⸻

2. Product Development Plan (PDP)

2.1 Product Vision

CircleAI helps you be the person who remembers and shows up.
An AI calendar and companion focused not on tasks or projects, but on the humans in your life.

Positioning vs current market:
	•	Personal CRMs (Monica, Clay, Covve, Queue, etc.) focus on organizing contacts and reminding you to follow up, often for networking.  ￼
	•	AI calendars (Toki, Clockwise, Akiflow, etc.) focus on time optimization and work tasks.  ￼
	•	Family organizers (e.g., Gether) focus on shared schedules and parenting logistics.  ￼

CircleAI’s unique focus: relationship-centric AI calendar that treats your connections as the primary object, not just events.

⸻

2.2 Target Users & Jobs-To-Be-Done

Personas
	1.	The Overloaded Professional
	•	Long work hours, forgets birthdays and friend catch-ups.
	•	JTBD: “Help me maintain my relationships without needing to remember everything.”
	2.	The Network-Builder
	•	Consultant, freelancer, or founder.
	•	JTBD: “Help me stay warm with my network and never miss key moments.”
	3.	The Relationship-Guardian
	•	Values family and long-term friendships.
	•	JTBD: “Help me be more intentional: remember milestones, check in, and schedule time together.”

⸻

2.3 Roadmap – Phases & Scope

Phase 0 – Discovery & Foundations
	•	10–20 user interviews across the personas.
	•	Map out privacy red lines and must-haves.
	•	Decide initial platforms (likely: web + iOS, then Android).
	•	Design core user flows:
	•	Onboarding
	•	“Today” screen
	•	Contact profile
	•	Draft-and-send flow

Deliverables:
	•	UX prototypes (Figma or similar)
	•	Prioritized backlog
	•	Data protection impact assessment outline

⸻

Phase 1 – MVP: “Never Miss Birthdays & Check-Ins”
Goal: Deliver a lean product that:
	•	Imports contacts (phone + Google)
	•	Detects birthdays & key dates
	•	Provides simple stay-in-touch reminders
	•	Drafts messages but does not auto-send

Included features:
	•	Basic onboarding:
	•	Connect contacts & one calendar
	•	Create core circles (Family, Friends, Work)
	•	Birthday & custom date tracking
	•	Manual frequency settings per circle (e.g., “Family – every 2 weeks”)
	•	Daily “People to contact today” view
	•	AI-generated drafts for:
	•	Birthday messages
	•	Generic check-in messages
	•	Manual send via:
	•	Copy & paste into messaging app
	•	Email integration (send from your email)
	•	Core privacy controls:
	•	Clear permissions
	•	Easy revocation / disconnect

Success criteria (MVP):
	•	% of onboarded users who connect at least one data source.
	•	% of daily active users who send at least one message/week via CircleAI.
	•	User qualitative feedback: “This actually helped me remember and reach out.”

⸻

Phase 2 – V1: Smart Cadence & Light Automation
Goal: Make CircleAI more proactive and useful while still trust-first.

New capabilities:
	•	Per-contact frequency tuning based on behavior
	•	Insights dashboard:
	•	“Who you’re losing touch with”
	•	“Your week in relationships”
	•	Scheduling suggestions for calls/meetings:
	•	Integrate with calendars to propose slots
	•	Deeper integrations:
	•	Gmail/Outlook for interaction logging
	•	Saved templates & custom tones
	•	Optional auto-send for birthdays for selected contacts (very explicit opt-in with safety rails)
	•	Weekly email summary & plan

⸻

Phase 3 – Pro Features & “Circles of Life”
Goal: Move towards a premium offering and more advanced use cases.

New capabilities:
	•	Advanced analytics:
	•	Relationship health score per circle
	•	“Top 10 most contacted vs least contacted”
	•	Call log integration (optional)
	•	SMS / WhatsApp integration for:
	•	One-tap send from inside the app
	•	(Where allowed) sending via the app using connected account
	•	Group events:
	•	Group scheduling suggestions
	•	Poll links for meetup times
	•	More nuanced AI:
	•	Gift idea suggestions (where data supports)
	•	Conversation prompts based on shared interests or previous chats
	•	Work mode:
	•	Light CRM features: leads, clients, “deal stage” tags

Monetization options:
	•	Free tier: birthdays, basic reminders, limited AI drafts.
	•	Pro tier: multiple integrations, advanced analytics, auto-send, group features.

⸻

2.4 Technical Architecture (High-Level)

Frontend:
	•	Mobile: React Native or Flutter for cross-platform.
	•	Web: React/Next.js.

Backend:
	•	API: Node.js (TypeScript) or Python (FastAPI).
	•	Database: PostgreSQL for relational data; Redis for caching.
	•	Background jobs: queue system (e.g., BullMQ, Celery, etc.) for:
	•	Daily digests
	•	Syncing integrations
	•	Reminder generation

AI Layer:
	•	Use LLM API (e.g., OpenAI GPT-5.x) with:
	•	Prompt templates per use case (birthday, check-in, sympathy, etc.)
	•	Guardrails for safety and tone
	•	Optionally add fine-tuning or structured prompt libraries for consistent messaging.

Integrations:
	•	Google Workspace APIs (Calendar, People, Gmail)
	•	Microsoft Graph (Calendar, People, Email)
	•	Device contacts & call logs (through native permissions)
	•	Messaging APIs (WhatsApp, Telegram, Twilio SMS, email providers)

⸻

2.5 Team & Roles
	•	Product Lead / Founder
	•	Vision, roadmap, prioritization, stakeholder management.
	•	Tech Lead / Architect
	•	Technical decisions, integration strategies, security.
	•	Backend Engineer(s)
	•	APIs, data model, integrations, job queues.
	•	Mobile / Frontend Engineer(s)
	•	iOS/Android apps, web dashboard.
	•	AI / Prompt Engineer
	•	Message templates, safety filters, personalization strategies.
	•	Designer (UX / UI)
	•	Flows, visual identity, interaction design.
	•	Privacy & Legal Advisor
	•	Consent flows, data processing agreements, policies.
	•	Customer Success / Support
	•	Early user onboarding, feedback loops.

⸻

2.6 Metrics & Analytics

Core metrics:
	•	Activation:
	•	% of new users connecting ≥1 integration.
	•	% completing onboarding (creating circles, selecting frequencies).
	•	Engagement:
	•	Daily/weekly active users.
	•	of messages drafted per user per week.
	•	of nudges acted on vs ignored.
	•	Outcome-focused:
	•	Increase in number of distinct contacts reached per month.
	•	Reduced “involuntary drift” (contacts with long gaps).
	•	Satisfaction:
	•	NPS / in-app rating
	•	“Did this message feel like you?” quick surveys
	•	Trust:
	•	Opt-outs, revocations of permissions.
	•	Support tickets related to privacy concerns.

⸻

2.7 Risks & Mitigations
	1.	Privacy / Security Concerns
	•	Mitigation: privacy-first branding; clear consent; minimal data access by default; strong encryption; easily accessible privacy controls.
	2.	Platform Dependency (APIs changing)
	•	Mitigation: abstraction layer for integrations; regular monitoring; fallbacks and graceful degradation.
	3.	AI Hallucinations / Inappropriate Messaging
	•	Mitigation:
	•	Manual review by default.
	•	Filters for tone, language, and sensitive topics.
	•	“Never auto-send without explicit per-contact opt-in.”
	4.	Notification Fatigue
	•	Mitigation:
	•	Tunable frequency.
	•	“I’m overwhelmed” control to auto-reduce nudges.
	•	Smart batching into daily digest instead of constant pushes.
	5.	Over-Automation / Feeling Inauthentic
	•	Mitigation:
	•	Emphasize co-writing: AI drafts, user finalizes.
	•	Personalization sliders (more/less formal, length).
	•	Encouraging user to add a personal line before sending.

⸻

2.8 Immediate Next Steps
	1.	Refine Product Narrative & Naming
	•	Lock the name, tagline, and how you describe it in one sentence.
	2.	Design Core User Flows
	•	Onboarding
	•	“Today” screen
	•	Contact profile
	•	Draft & send flow
	3.	Pick Initial Integrations
	•	E.g., Start with Google Calendar + Google Contacts + Gmail (very common combo).
	4.	Define an MVP Experiment
	•	Choose 1–2 personas.
	•	Build a narrow but delightful flow:
“Never forget birthdays again, and send thoughtful, AI-assisted messages in 10 seconds.”
	5.	User Testing
	•	Put Figma prototypes in front of 5–10 target users.
	•	Confirm that the reminders + AI drafts actually feel helpful, not creepy.