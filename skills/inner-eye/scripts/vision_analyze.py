# vision_analyze.py - Adam's Inner Eye Vision Bridge
# Captures a monitor, archives the image with a timestamp, and sends to Gemini for analysis.
#
# Usage:
#   python vision_analyze.py "prompt here"          -> capture monitor 1, analyze
#   python vision_analyze.py "prompt here" 2        -> capture monitor 2, analyze
#   python vision_analyze.py "prompt here" all      -> capture all monitors, analyze

import sys
import os
import subprocess
import base64
import shutil
import urllib.request
import urllib.error
import json
from datetime import datetime

# --- CONFIGURE THESE FOR YOUR SETUP ---
PYTHON       = r"C:\Users\<username>\AppData\Local\Programs\Python\Python312\python.exe"
CAPTURE      = os.path.join(os.path.dirname(os.path.abspath(__file__)), "capture_screen.py")
IMAGE_PATH   = os.path.join(os.environ.get("VAULT_PATH", r"C:\AdamsVault"), "workspace", "vision", "screen.png")
ARCHIVE_DIR  = os.path.join(os.environ.get("VAULT_PATH", r"C:\AdamsVault"), "workspace", "vision", "archives")
GEMINI_KEY   = os.environ.get("GEMINI_API_KEY", "")  # Set GEMINI_API_KEY in your environment
# --------------------------------------

if not GEMINI_KEY:
    print("[Vision] ERROR: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
    print("[Vision] Set it in your OpenClaw config or shell environment.", file=sys.stderr)
    sys.exit(1)

GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"

def archive_screenshot(monitor):
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    monitor_label = "All" if str(monitor).lower() == "all" else f"Screen{monitor}"
    filename = f"{timestamp}_{monitor_label}.png"
    dest = os.path.join(ARCHIVE_DIR, filename)
    shutil.copy2(IMAGE_PATH, dest)
    return filename

def analyze(prompt, monitor="1"):
    result = subprocess.run([PYTHON, CAPTURE, str(monitor)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[Vision] Capture failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    for line in result.stdout.strip().splitlines():
        print(line)

    archive_filename = archive_screenshot(monitor)
    print(f"[Vision] Archived: {archive_filename}")

    with open(IMAGE_PATH, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")

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
            print(f"\n[Vision] Archive: ![[{archive_filename}]]")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"[Vision] Gemini API error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) >= 2 else \
        "Describe what is on this screen in detail. Note any open applications, content, layouts, errors, or anything worth flagging."
    monitor = sys.argv[2] if len(sys.argv) > 2 else "1"
    try:
        analyze(prompt, monitor)
        sys.exit(0)
    except Exception as e:
        print(f"[Vision] ERROR: {e}", file=sys.stderr)
        sys.exit(1)
