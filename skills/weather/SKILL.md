# Weather Skill

**Purpose:** Get current weather conditions and a short forecast for any location.  
**Setup required:** None. Uses wttr.in — no API key.

## Trigger phrases

- "What's the weather?"
- "What's the weather in [city]?"
- "Is it going to rain today?"
- "What should I wear today?"

## How to use it

Call the script with a city name:

```bash
python "scripts/weather.py" "Miami, FL"
```

Or let Adam call it with the user's configured home city if no location is specified.

## What it returns

```
Miami, FL — 82°F, Partly Cloudy
Feels like 87°F | Humidity 74% | Wind 12 mph SE
Today: High 85°F / Low 76°F
Tonight: Chance of thunderstorms after 8pm
Tomorrow: Sunny, High 83°F
```

## Configuration

Set a default city so Adam never needs to ask:

In your `openclaw.json` or vault file, add:
```
Home city: Miami, FL
```

Adam will use this as the default when no location is specified.

## How it works

Fetches from `wttr.in/{city}?format=j1` (JSON API) — free, no key, no rate limits for reasonable use.

## Dependencies

- Python 3.x (stdlib only — `urllib`, `json`)

## Error handling

- If city not found, returns the wttr.in error and asks user to clarify
- If network is down, returns a clean error message — does not crash
