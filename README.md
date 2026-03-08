# adam-skills

The official skill library for the [Adam Framework](https://github.com/strangeadvancedmarketing/Adam).

Adam is a locally-hosted AI assistant with persistent memory. This repo extends him with real-world capabilities — web search, email intelligence, screen vision, lead generation, weather, news, system monitoring, and more.

---

## What's in here

Skills are organized into two tracks:

### 🟢 Core Skills — Zero or minimal setup. Works out of the box.

| Skill | What it does | Setup |
|-------|-------------|-------|
| [weather](skills/weather/) | Current conditions + forecast via wttr.in | None |
| [news-headlines](skills/news-headlines/) | Top headlines via RSS | None |
| [notes](skills/notes/) | Save notes to your vault | None |
| [morning-briefing](skills/morning-briefing/) | Weather + news + unread email count in one shot | Gmail app password |
| [system-health](skills/system-health/) | CPU, RAM, disk, top processes — proactive resource alerts | `pip install psutil` |
| [uptime-check](skills/uptime-check/) | Ping your live endpoints, flag anything down | None |

### 🔵 Intelligence Skills — Built on Adam's existing tools

| Skill | What it does | Setup |
|-------|-------------|-------|
| [email-intelligence](skills/email-intelligence/) | Proactive email triage — scores, categorizes, alerts | Gmail app password |
| [synthesis](skills/synthesis/) | Latent pattern recognition across domains | None |
| [presence-pulse](skills/presence-pulse/) | Loads session resonance from previous heartbeat | None |
| [inner-eye](skills/inner-eye/) | Screen + webcam vision via Gemini | Gemini API key |

### 🟠 Action Skills — Full automation pipelines

| Skill | What it does | Setup |
|-------|-------------|-------|
| [contractor-prospector](skills/contractor-prospector/) | Find leads → build demo sites → send outreach | Firecrawl, GitHub CLI, Gmail |

---

## Quick Install

### Windows (PowerShell)
```powershell
# Clone into your OpenClaw skills directory
cd C:\Users\<you>\.openclaw\workspace\skills
git clone https://github.com/strangeadvancedmarketing/adam-skills.git
cd adam-skills
.\install.ps1
```

---

## Relationship to Adam

These skills run **on top of** the Adam Framework. They assume:
- Adam is installed and running (see [Adam setup](https://github.com/strangeadvancedmarketing/Adam))
- OpenClaw gateway is live on `ws://127.0.0.1:18789`
- You have the email plugin configured (for email-based skills)

Skills that need external APIs will tell you exactly what keys are required and where to get them.

---

## Plugins vs Skills

**Plugins** (in `/plugins/`) are compiled OpenClaw extensions that give Adam new native tools. The email plugin is the primary one — 10 Gmail tools: search, read, send, delete, move, flag, bulk operations, and sender analysis.

**Skills** (in `/skills/`) are SKILL.md instruction files + optional Python/JS scripts that teach Adam *how to use* those tools in meaningful ways.

---

## What Adam can do (full capability map)

See [docs/CAPABILITIES.md](docs/CAPABILITIES.md) for the complete picture of what a fully-equipped Adam installation can do — memory layers, native tools, MCP integrations, and all skills combined.

---

## Contributing

PRs welcome. Each skill needs:
- `SKILL.md` — instructions Adam reads at runtime
- `scripts/` — any Python/JS helpers (optional)
- `README.md` — human-readable setup guide

---

Built by [Strange Advanced Marketing](https://github.com/strangeadvancedmarketing)
