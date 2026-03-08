# inner-eye — Adam's Screen Vision Skill (Multi-Monitor Edition)

## What This Is
This skill gives Adam the ability to capture any monitor on demand,
or grab a full panoramic stitch of all screens at once, then analyze via Gemini vision.

## Monitor Layout
Configure to match your setup. Default mapping:
| Argument | Position |
|----------|----------|
| `1` | Primary monitor — DEFAULT |
| `2` | Secondary monitor |
| `3` | Third monitor |
| `all` | Panoramic stitch of all monitors |

Update this section in your local copy after installation to reflect your actual layout.

## Trigger Phrases & Argument Mapping
| What you say | Argument to pass |
|-------------|-----------------|
| "Look at my screen" / "Check this out" | `1` (default) |
| "Look at my left screen" | `3` |
| "Look at my right screen" | `2` |
| "Look at my main screen" / "laptop" | `1` |
| "Look at all my screens" / "see everything" | `all` |
| No monitor specified | `1` (default) |

## Tool Name
`capture_screen`

## How To Use It

### Option A — Capture only
```bash
python "scripts/capture_screen.py" [1|2|3|all]
```
Saves PNG to `<vault>/workspace/vision/screen.png`  
Saves base64 to `<vault>/workspace/vision/screen.b64`

### Option B — Full pipeline (capture + Gemini analysis)
```bash
python "scripts/vision_analyze.py" "Your prompt here" [1|2|3|all]
```

Example:
```bash
python "scripts/vision_analyze.py" "Describe what is on this screen. Note any open applications, content, or anything worth flagging." 2
```

**NOTE:** Do NOT use `mcporter call gemini.gemini_analyze_image` with a file path — it requires
base64 passed as a shell argument which breaks with large images. Use vision_analyze.py instead.

### Respond
Deliver the visual analysis conversationally. Be specific. Describe what is actually there.

## The Glance — Webcam Sight

Captures one frame from the built-in webcam, archives it, and runs Gemini vision analysis.
Camera light turns off immediately after capture.

```bash
python "scripts/webcam_analyze.py" "prompt here"
```

**Output files:**
- `<vault>/workspace/vision/webcam.png` — always current
- `<vault>/workspace/vision/archives/YYYY-MM-DD_HH-MM-SS_Webcam.png` — timestamped archive

**Scripts:**
- `webcam_capture.py` — raw capture only
- `webcam_analyze.py` — capture + Gemini analysis (use this one)

---

## Housekeeping — Archive Cleanup

Deletes archived screenshots older than 14 days.

```bash
python "scripts/vault_housekeeping.py"
```

---

## Output Files
- `<vault>/workspace/vision/screen.png` — raw screenshot (always overwritten)
- `<vault>/workspace/vision/screen.b64` — base64 encoded version

## Error Handling
- If a monitor index doesn't exist, script auto-falls back to monitor 1
- Adam will notify you if fallback occurs

## Configuration

Paths are set via the `VAULT_PATH` environment variable:
```
VAULT_PATH=C:\YourVault
```
Default if not set: `C:\AdamsVault`

Set `GEMINI_API_KEY` in your environment or OpenClaw config.

## Dependencies
- `mss` — screen capture (`pip install mss`)
- `cv2` — webcam capture (`pip install opencv-python`)
- `urllib` / `json` / `base64` — stdlib (Gemini API calls)
