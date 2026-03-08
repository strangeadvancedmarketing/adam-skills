# Adam — Full Capability Map

This document describes what a fully-configured Adam installation can do.
Skills in this repo add to or unlock these capabilities.

---

## Memory System (4 Layers)

| Layer | What it does |
|-------|-------------|
| Layer 1: Vault Injection | Markdown files from your vault injected at every session start via SENTINEL |
| Layer 2: memory-core | Active mid-session search via `memory_search` / `memory_get` |
| Layer 3: Neural Graph | Associative recall — 7,000+ neurons, 29,000+ synapses, Hebbian learning |
| Layer 4: Nightly Reconcile | Gemini-powered consolidation into `Adam_Core_Memory.md` every night |

---

## Native OpenClaw Tools (Always Available)

| Tool | Description |
|------|-------------|
| TTS | Text-to-speech — Edge TTS (cloud) + Kokoro-ONNX (local fallback), auto-voices every message |
| Telegram | Full bidirectional — Adam texts you, you text Adam. No mention required in group. |
| Email (10 tools) | Gmail via IMAP/SMTP: search, read, send, delete, move, flag, bulk ops, sender analysis |
| Web search | Via Firecrawl MCP (see below) |

---

## MCP Integrations (via mcporter)

| Server | Tools | Notes |
|--------|-------|-------|
| Firecrawl | Search, scrape, crawl, structured extract, browser sessions | Primary web tool |
| Gemini | Text gen, chat, vision, document analysis, grounded search, Veo 3 video, image-to-video | 9 tools |
| Notion | Full CRUD — pages, databases, blocks, comments | 22 tools |
| OpenRouter | Route to any model: DeepSeek, GPT-4o, Claude, O1, Llama | Model swarm backbone |
| Computer-use | Mouse, keyboard, window management, screen capture, clipboard | 23 tools — full Windows control |
| Neural-memory | Associative graph memory, spreading activation recall | Local SQLite |
| Zapier | 7,000+ app integrations | Needs re-auth |
| Desktop Commander | File system + terminal | |

---

## Skills (This Repo)

### Core Skills
| Skill | Capability |
|-------|-----------|
| weather | Current conditions + forecast — zero config |
| news-headlines | Top headlines from RSS — zero config |
| notes | Write notes to your vault |
| morning-briefing | Weather + news + unread email in one command |
| system-health | CPU, RAM, disk, top processes — proactive resource alerts |
| uptime-check | Ping your live endpoints, report up/down |

### Intelligence Skills
| Skill | Capability |
|-------|-----------|
| email-intelligence | Proactive triage, urgency scoring (1-10), relationship context, Telegram alerts |
| synthesis | Latent pattern recognition — connects micro to macro across domains |
| presence-pulse | Loads emotional resonance from previous session heartbeat |
| inner-eye | Screen vision (multi-monitor) + webcam capture + Gemini analysis |

### Action Skills
| Skill | Capability |
|-------|-----------|
| contractor-prospector | Lead gen (Firecrawl) → demo site (GitHub Pages) → email outreach |

---

## Community Skills (clawhub)

These install via `clawhub install <n>` and live in your skills directory:

| Skill | Capability |
|-------|-----------|
| browser-use | AI-native browser automation — navigate, fill forms, handle JS, run parallel agents |
| playwright-scraper | Stealth scraping for Cloudflare-protected and heavy JS sites |
| elite-longterm-memory | WAL + vector + git-notes + cloud backup memory layer |
| neural-memory | Biologically-inspired memory graph (also included in Layer 3 above) |

---

## Custom Infrastructure

| Component | What it does |
|-----------|-------------|
| SENTINEL.ps1 | Watchdog — monitors gateway + Kokoro every 30s, auto-restarts on death |
| reconcile_memory.py | Nightly Gemini consolidation of session memory into core vault |
| coherence_monitor.py | Test suite verifying all 4 memory layers are healthy |
| Emergency Reconstruction | One-click restore of all core files from verified snapshot |

---

## What a "good morning" looks like with everything installed

1. `morning-briefing` triggers
2. Weather for your city (wttr.in, no API key)
3. Top 5 news headlines (RSS)
4. Unread email count + top priority flag (email-intelligence)
5. `presence-pulse` loads yesterday's unresolved tension
6. `synthesis` scans for patterns across the context
7. Adam voices it all via TTS and sends to Telegram

One message. Full situational awareness.
