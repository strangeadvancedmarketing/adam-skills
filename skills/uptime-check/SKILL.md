# Uptime Check Skill

**Purpose:** Ping a list of URLs and report which are up or down. Instantly know if any of your live endpoints have gone dark.
**Setup required:** None. Pure Python stdlib.

## Setup

No setup required. Edit `config/urls.txt` to add your URLs (one per line).

## Trigger phrases

- "Check my sites"
- "Are my sites up?"
- "Run uptime check"
- "Is [site] down?"
- "Check endpoints"

## What it returns

```
🌐 UPTIME CHECK — 3/8/2026 2:14 PM

✅  https://yoursite.com              200  (312ms)
✅  https://another-site.github.io    200  (541ms)
⚠️  https://api.yourservice.com       403  (88ms)
🚨  https://dashboard.example.com     TIMEOUT
✅  https://yourshop.myshopify.com    200  (289ms)

4/5 up  |  1 timeout  |  0 errors
```

## Configuration

Edit `config/urls.txt` — one URL per line. Blank lines and `#` comments are ignored:

```
# My live sites
https://mysite.com
https://myapp.github.io

# APIs I depend on
https://api.example.com/health

# Skip this one for now
# https://staging.example.com
```

## How to use it

```bash
python scripts/uptime_check.py                  # Check all URLs in config
python scripts/uptime_check.py https://url.com  # Check a single URL
python scripts/uptime_check.py --json           # JSON output
python scripts/uptime_check.py --fail-only      # Only show failures
```

## Status codes

| Icon | Meaning |
|------|---------|
| ✅ | 2xx response — up |
| ⚠️ | 3xx/4xx — reachable but not healthy |
| 🚨 | Timeout or connection error — down |

## Proactive monitoring

Add to SENTINEL or a cron job to alert on failures:

```powershell
python "C:\path\to\skills\uptime-check\scripts\uptime_check.py" --fail-only
# Outputs nothing if all up. Outputs failures if any down.
# Pipe to Telegram or log file as needed.
```

## Dependencies

- Python 3.x (stdlib only — `urllib`, `socket`, `concurrent.futures`)
