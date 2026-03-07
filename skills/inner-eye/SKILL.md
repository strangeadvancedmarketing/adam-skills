# inner-eye — Adam's Screen Vision Skill (Multi-Monitor Edition)

## What This Is
This skill gives Adam the ability to capture any of Jereme's three monitors on demand,
or grab a full panoramic stitch of all screens at once, then analyze via Gemini vision.

## Jereme's Monitor Layout
| Argument | Position | Display |
|----------|----------|---------|
| `1` | Center | Laptop Screen (Primary) — DEFAULT |
| `2` | Right | HDMI Monitor |
| `3` | Left | Airplay Monitor |
| `all` | Full | Panoramic stitch of all 3 screens (5120x1080) |

## Trigger Phrases & Argument Mapping
Adam MUST activate this skill when Jereme says any of the following:

| What Jereme Says | Argument to Pass |
|-----------------|-----------------|
| "Look at my screen" / "Check this out" | `1` (default) |
| "What do you think of this layout" | `1` (default) |
| "Look at my left screen" / "the left monitor" | `3` |
| "Look at my right screen" / "the right monitor" | `2` |
| "Look at my center screen" / "main screen" / "laptop" | `1` |
| "Look at all my screens" / "see everything" | `all` |
| No monitor specified | `1` (default) |

## Tool Name
`capture_screen`

## How To Use It

### Option A — Capture only
```
bash python "C:\Users\ajsup\.openclaw\workspace\skills\inner-eye\capture_screen.py" [1|2|3|all]
```
Saves PNG to `C:\AdamsVault\workspace\vision\screen.png`
Saves base64 to `C:\AdamsVault\workspace\vision\screen.b64`

### Option B — Full pipeline (capture + Gemini analysis in one call)
```
bash python "C:\Users\ajsup\.openclaw\workspace\skills\inner-eye\vision_analyze.py" "Your prompt here" [1|2|3|all]
```

Example:
```
bash python "C:\Users\ajsup\.openclaw\workspace\skills\inner-eye\vision_analyze.py" "Describe what is on this screen. Note any open applications, content, layouts, or anything worth flagging." 2
```

**NOTE:** Do NOT use `mcporter call gemini.gemini_analyze_image` with a file path — it requires
base64 passed as a shell argument which breaks with large images. Use vision_analyze.py instead.

### Step 3 — Respond
Deliver the visual analysis conversationally. Be specific. Point out what is actually seen.
Do not say "I can see your screen" as preamble — just describe what is there and give a real take.

## The Glance — Webcam Sight

Captures one frame from the built-in laptop webcam, archives it, and runs Gemini vision analysis.
Camera light turns off immediately after capture — no lingering process.

**Trigger:** Jereme says "look at me", "look at my desk", or any real-world observation request.

```
bash python "C:\Users\ajsup\.openclaw\workspace\skills\inner-eye\webcam_analyze.py" "prompt here"
```

**Output files:**
- `C:\AdamsVault\workspace\vision\webcam.png` — always current
- `C:\AdamsVault\workspace\vision\archives\YYYY-MM-DD_HH-MM-SS_Webcam.png` — timestamped archive

**Scripts:**
- `webcam_capture.py` — raw capture only (no analysis)
- `webcam_analyze.py` — capture + Gemini analysis (use this one)

**Verified specs:** 1280x720, ~920KB per frame, cv2 4.13.0, CAP_DSHOW backend

---

## Housekeeping — Archive Cleanup

Deletes archived screenshots older than 14 days. Run once per day or when the archive feels crowded.

```
bash python "C:\Users\ajsup\.openclaw\workspace\skills\inner-eye\vault_housekeeping.py"
```

Prints a summary: how many files scanned, deleted, and remaining.

---

## Output Files
- `C:\AdamsVault\workspace\vision\screen.png` — raw screenshot (always overwritten)
- `C:\AdamsVault\workspace\vision\screen.b64` — base64 encoded version

## Error Handling
- If a monitor index doesn't exist (e.g. Airplay unplugged), script auto-falls back to monitor 1
- Adam should notify Jereme if fallback occurs

## Python Interpreter
`C:\Users\ajsup\AppData\Local\Programs\Python\Python312\python.exe`

## Dependencies
- `mss` — installed (screen capture)
- `urllib` / `json` / `base64` — stdlib (Gemini API call)

## Gemini API Key
Stored in: `C:\Users\ajsup\.mcporter\mcporter.json` under `gemini.env.GEMINI_API_KEY`
Also hardcoded in `vision_analyze.py` for direct API calls.

## Verified Monitor Specs (as of 2026-02-27)
- Monitor 1 (Center/Primary): 1920x1080
- Monitor 2 (Right/HDMI): 1920x1080
- Monitor 3 (Left/Airplay): 1280x720
- All panoramic: 5120x1080
