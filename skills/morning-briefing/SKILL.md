# Morning Briefing Skill

**Purpose:** One command → full situational awareness. Weather + news + unread email count + priority flag.  
**Setup required:** Gmail app password (for email count). Weather and news work without it.

## Trigger phrases

- "Good morning"
- "Morning briefing"
- "What's my morning look like?"
- "Start my day"
- "Brief me"

## What it delivers

```
☀️ MORNING BRIEFING — Saturday, March 7, 2026

WEATHER
Miami, FL — 79°F, Clear
Feels like 81°F | Humidity 68%
Today: High 86°F / Low 75°F — Sunny

NEWS
1. Fed holds rates steady amid inflation uncertainty · Reuters · 2h
2. OpenAI announces new reasoning model · TechCrunch · 4h
3. Housing market shows signs of cooling · Bloomberg · 5h
4. SpaceX launches 24 Starlink satellites · The Verge · 6h
5. Local sports team wins · ESPN · 8h

EMAIL
📬 14 unread messages
⚠️  Priority: Urgent subject line from known sender (2h ago)
```

## How it works

Adam runs this sequence:
1. Calls `scripts/weather.py` with your home city
2. Calls `scripts/news.py` for top 5 general headlines  
3. Calls `email_search` (native tool) — grabs last 20, counts unread, flags any urgent sender
4. Assembles everything into one clean briefing
5. Voices it via TTS and sends to Telegram if configured

## Configuration

In your vault or `openclaw.json`:

```
Home city: Your City, ST
Morning briefing news categories: general, tech
Urgent email senders: configure in known_entities.json
```

## Dependencies

- `weather` skill (included in this repo)
- `news-headlines` skill (included in this repo)
- Email plugin (for unread count — optional but recommended)
- Python 3.x

## Running standalone

```bash
python "scripts/morning_briefing.py" "Your City, ST"
```

This runs weather + news locally (no email). Add `--email` flag to include email count if you have credentials configured.

## Notes

- Designed to be spoken aloud via TTS — short, punchy, no fluff
- If email plugin isn't configured, the email section is skipped gracefully
- Configure urgent senders in `known_entities.json` to flag priority emails
