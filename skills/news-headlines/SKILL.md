# News Headlines Skill

**Purpose:** Fetch top headlines from RSS feeds. No API key required.  
**Setup required:** None.

## Trigger phrases

- "What's in the news?"
- "Any news today?"
- "Top headlines"
- "What happened today?"
- "Tech news" / "Business news" / "Local news"

## How to use it

```bash
python "scripts/news.py"              # Top general headlines
python "scripts/news.py" tech         # Tech news
python "scripts/news.py" business     # Business news
python "scripts/news.py" us           # US news
```

## What it returns

```
📰 TOP HEADLINES — Sat Mar 7, 2026

1. Fed holds rates steady amid inflation uncertainty
   Reuters · 2 hours ago

2. OpenAI announces new reasoning model
   TechCrunch · 4 hours ago

3. Housing market shows signs of cooling
   Bloomberg · 5 hours ago

4. SpaceX launches 24 Starlink satellites
   The Verge · 6 hours ago

5. Miami Heat beat Celtics 112-104
   ESPN · 8 hours ago
```

## RSS Feed Sources

| Category | Source |
|----------|--------|
| General | Google News Top Stories |
| Tech | TechCrunch |
| Business | Reuters Business |
| US | AP News |
| World | BBC World |

## Dependencies

- Python 3.x (stdlib only — `urllib`, `xml.etree.ElementTree`, `html`)

## Customization

Edit `scripts/news.py` to add or swap RSS feeds. Any RSS 2.0 feed works.
