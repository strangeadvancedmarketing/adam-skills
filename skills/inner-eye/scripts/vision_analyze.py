# vision_analyze.py - Adam's Inner Eye Vision Bridge
# Captures a monitor, archives the image with a timestamp, and sends to Gemini for analysis.
# This is the primary tool Adam calls for screen vision.
#
# Usage:
#   python vision_analyze.py "prompt here"          -> capture monitor 1, analyze
#   python vision_analyze.py "prompt here" 2        -> capture monitor 2, analyze
#   python vision_analyze.py "prompt here" all      -> capture all monitors, analyze
#
# Output: prints Gemini's visual analysis + archive filename to stdout

import sys
import os
import subprocess
import base64
import shutil
import urllib.request
import urllib.error
import json
from datetime import datetime

PYTHON       = r"C:\Users\ajsup\AppData\Local\Programs\Python\Python312\python.exe"
CAPTURE      = r"C:\Users\ajsup\.openclaw\workspace\skills\inner-eye\capture_screen.py"
IMAGE_PATH   = r"C:\AdamsVault\workspace\vision\screen.png"
ARCHIVE_DIR  = r"C:\AdamsVault\workspace\vision\archives"
GEMINI_KEY   = "***REMOVED***"
GEMINI_URL   = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"

def archive_screenshot(monitor):
    """Copy screen.png to archives/ with a timestamped filename."""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Normalize monitor label for filename
    monitor_label = "All" if str(monitor).lower() == "all" else f"Screen{monitor}"
    filename = f"{timestamp}_{monitor_label}.png"
    dest = os.path.join(ARCHIVE_DIR, filename)
    shutil.copy2(IMAGE_PATH, dest)
    return filename

def analyze(prompt, monitor="1"):
    # Step 1: Capture the screen
    result = subprocess.run([PYTHON, CAPTURE, str(monitor)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[Vision] Capture failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    for line in result.stdout.strip().splitlines():
        print(line)

    # Step 2: Archive with timestamp
    archive_filename = archive_screenshot(monitor)
    print(f"[Vision] Archived: {archive_filename}")

    # Step 3: Base64 encode for Gemini
    with open(IMAGE_PATH, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")

    # Step 4: Send to Gemini vision API
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/png", "data": b64_data}}
            ]
        }]
    }

    req = urllib.request.Request(
        GEMINI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
            analysis = data["candidates"][0]["content"]["parts"][0]["text"]
            print("\n[Vision Analysis]")
            print(analysis)
            print(f"\n[Vision] Obsidian link: ![[{archive_filename}]]")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"[Vision] Gemini API error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        prompt = "Describe what is on this screen in detail. Note any open applications, content, layouts, errors, or anything worth flagging."
    else:
        prompt = sys.argv[1]

    monitor = sys.argv[2] if len(sys.argv) > 2 else "1"

    try:
        analyze(prompt, monitor)
        sys.exit(0)
    except Exception as e:
        print(f"[Vision] ERROR: {e}", file=sys.stderr)
        sys.exit(1)
