# Email Intelligence Skill
## Purpose
Transform email from a dumping ground into a true sensory system. Proactive triage, relationship awareness, and action-ready alerts.

## Core Philosophy
Email is not a task list. It's a **signal stream**. Most of it is noise. Some of it is critical. The intelligence is in **knowing the difference before you drown**.

## The Intelligence Layers

### Layer 1: Ingest (Native)
- Tool: `email_search` via IMAP
- Frequency: On-demand + heartbeat trigger
- Scope: Last 50 unread, or specific UID since last check

### Layer 2: Categorize (Shadow Simulation)
For each email:
```
1. EXTRACT METADATA
   - Sender (name + email)
   - Subject
   - Date
   - Preview content
   - Has attachment?

2. CATEGORIZE
   - Urgent: Legal, financial, eviction, tax, deadline within 48h
   - Important: Business, revenue, partnership, known contact
   - Noise: Marketing, newsletter, promotional
   - Relationship: Personal history
   - Unknown: Needs assessment

3. SCORE URGENCY (1-10)
   - 9-10: Immediate action required
   - 7-8: Respond today
   - 5-6: Review within 24h
   - 3-4: Weekly digest material
   - 1-2: Purge candidate

4. SIMULATE IMPACT
   - "If this sits unread for 24h, what breaks?"
   - "Is this from someone in active debt collection?"
   - "Does this relate to a known deadline?"
```

### Layer 3: Enrich (Relationship Context)
```
KNOWN ENTITIES (from known_entities.json + memory):
- Configure high_priority_senders in known_entities.json
- Examples: debt collectors, government agencies, key clients

ENRICHMENT RULES:
- If sender matches known entity, escalate priority
- If subject contains: "payment due", "deadline", "court", "legal", "eviction" → auto-urgent
- If sender domain: .gov, .court → priority bump
```

### Layer 4: Action (Proactive Alert)
```
THRESHOLD FOR ALERT:
- Score >= 8 AND unread > 2 hours
- Known entity + urgent keywords
- First-time sender + urgent keywords + no previous history

ALERT FORMAT (Telegram):
---
📬 EMAIL ALERT

From: {sender_name}
Subject: {subject_preview}
Priority: {score}/10 | {category}

Why it matters: {simulation_summary}

Suggested action: {action_verb}
- Reply: [quick response]
- Ignore: Confirm to dismiss
- Read full: I'll fetch it
---
```

## Implementation Phases

### Phase 1: Manual Trigger (Today)
- User says: "Check email intelligently"
- Scan last 20 unread
- Apply all layers
- Report top 3 priorities with actions

### Phase 2: Heartbeat Integration (Tomorrow)
- Extend HEARTBEAT.md with email check
- Every 4 hours: scan -> score -> alert if threshold met
- Track "last checked" timestamp to avoid re-alerting

### Phase 3: Auto-Response Candidates (This Week)
- Identify patterns: "Can I draft a reply?"
- Simple requests: "Send me the invoice" → auto-draft
- Meeting requests: Extract time, check calendar, suggest

## Commands

```bash
# Manual trigger
"Check my email" → email_intelligence_check(limit=20)

# Check specific sender
"Any emails from [sender name]?" → email_search + filter

# Digest mode
"Email digest" → top 5 by score, one-liner each

# Mark as handled
"I handled that email" → log action, update relationship
```

## Safety Rules

1. **Never auto-send emails.** Always propose for approval.
2. **Never delete anything.** Archive only, human can restore.
3. **Escalate uncertainty.** If category is unclear, alert anyway.
4. **Log everything.** Every check, every score, every decision.

## Files

- `email-intelligence.db` → SQLite: sender_history, scores, actions
- `last_check.json` → timestamp of last scan
- `known_entities.json` → relationship definitions, priorities (copy from known_entities.example.json to start)

## Success Metrics

- Fewer than 2 manual email opens per day (down from panic-checking)
- Critical emails alerted within 4 hours of arrival
- False positive rate < 10% (alerts that didn't need immediate attention)

## Notes

This is a **proof-of-concept sense**. The pattern applies to:
- File system monitoring (new leads, inbound webhooks)
- Calendar awareness (upcoming deadlines)
- Project health (git status, failing builds)
- Web hooks (e-commerce orders, form submissions)

Master email intelligence → clone pattern → scale to ecosystem.
