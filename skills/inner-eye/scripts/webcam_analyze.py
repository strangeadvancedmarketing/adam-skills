#!/usr/bin/env python3
"""
Glance Bridge — Webcam Capture + Gemini Vision Analysis
Captures one frame from the webcam and sends to Gemini for analysis.
"""

import sys
import os
import base64
import json
import subprocess
import urllib.request
from pathlib import Path

SCRIPT_DIR  = Path(__file__).parent
VAULT_ROOT  = Path(os.environ.get("VAULT_PATH", r"C:\AdamsVault"))
VISION_DIR  = VAULT_ROOT / "workspace" / "vision"
WEBCAM_PATH = VISION_DIR / "webcam.png"
GEMINI_KEY  = os.environ.get("GEMINI_API_KEY", "")

if not GEMINI_KEY:
    print("[Glance] ERROR: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
    print("[Glance] Set it in your OpenClaw config or shell environment.", file=sys.stderr)
    sys.exit(1)

def capture_webcam():
    capture_script = SCRIPT_DIR / "webcam_capture.py"
    result = subprocess.run(["python", str(capture_script)], capture_output=True, text=True)
    embed_link = None
    for line in result.stdout.split("\n"):
        if line.startswith("EMBED_LINK:"):
            embed_link = line.replace("EMBED_LINK:", "").strip()
    return embed_link

def analyze_with_gemini(prompt):
    if not WEBCAM_PATH.exists():
        return "ERROR: No webcam image found. Capture may have failed."

    with open(WEBCAM_PATH, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/png", "data": image_data}}
            ]
        }]
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        if "candidates" in result and result["candidates"]:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        return "No analysis generated."
    except Exception as e:
        return f"ERROR during analysis: {e}"

def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else \
        "Describe what you see. Note the person, their expression, surroundings, and anything notable."

    print("Capturing webcam...")
    embed_link = capture_webcam()
    if not embed_link:
        print("ERROR: Capture failed")
        return 1

    print(f"Archive: {embed_link}")
    print("\nAnalyzing...")
    analysis = analyze_with_gemini(prompt)
    print("\n--- ANALYSIS ---")
    print(analysis)
    print(f"\nEmbed link: ![[{embed_link}]]")
    return 0

if __name__ == "__main__":
    sys.exit(main())
