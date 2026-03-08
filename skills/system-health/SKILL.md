# System Health Skill

**Purpose:** Check CPU, RAM, disk usage, and top processes. Adam can proactively flag resource issues without being asked.
**Setup required:** One pip install (`psutil`). No API keys, no accounts.

## Setup

```powershell
pip install psutil
```

That's it.

## Trigger phrases

- "How's my system?"
- "Check system health"
- "Am I running low on disk?"
- "What's eating my RAM?"
- "System status"
- "How much disk do I have left?"

## What it returns

```
💻 SYSTEM HEALTH

CPU:    23% (8 cores)
RAM:    18.4 GB used / 32.0 GB total (57%)
Disk C: 48.2 GB free / 256.0 GB total (81% used)

TOP PROCESSES (by RAM)
  chrome.exe        2.1 GB
  python.exe        812 MB
  node.exe          644 MB
  Code.exe          521 MB
  openclaw.exe      287 MB

Status: ✅ Healthy
```

## Status thresholds

| Resource | Warning | Critical |
|----------|---------|----------|
| CPU | >70% | >90% |
| RAM | >80% | >95% |
| Disk | >85% | >95% |

Adam will flag with ⚠️ or 🚨 if any threshold is exceeded.

## How to use it

```bash
python scripts/system_health.py
python scripts/system_health.py --watch    # Check every 30s until Ctrl+C
python scripts/system_health.py --json     # JSON output for programmatic use
python scripts/system_health.py --threshold-only  # Exit code only, no output
```

## Proactive monitoring

Add to your SENTINEL boot sequence or heartbeat trigger:

```powershell
python "C:\path\to\skills\system-health\scripts\system_health.py" --threshold-only
# Exit 0 = healthy, 1 = warning, 2 = critical
```

SENTINEL can fire a Telegram alert when exit code is non-zero.

## Dependencies

- Python 3.x
- `psutil` (`pip install psutil`)
