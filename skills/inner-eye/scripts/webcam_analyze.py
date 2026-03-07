#!/usr/bin/env python3
"""
Glance Bridge — Webcam Capture + Gemini Vision Analysis
One command to capture from webcam and analyze via Gemini.
"""

import sys
import os
import base64
from pathlib import Path
import subprocess

# Get script directory
SCRIPT_DIR = Path(__file__).parent
VAULT_ROOT = Path("C:/Adam's Vault")
VISION_DIR = VAULT_ROOT / "workspace" / "vision"
WEBCAM_PATH = VISION_DIR / "webcam.png"

def capture_webcam():
    """Run the capture script."""
    capture_script = SCRIPT_DIR / "webcam_capture.py"
    result = subprocess.run(
        ["python", str(capture_script)],
        capture_output=True,
        text=True
    )
    
    # Extract embed link from output
    embed_link = None
    for line in result.stdout.split('\n'):
        if line.startswith("EMBED_LINK:"):
            embed_link = line.replace("EMBED_LINK:", "").strip()
    
    return embed_link

def analyze_with_gemini(prompt):
    """Send webcam image to Gemini for analysis."""
    
    if not WEBCAM_PATH.exists():
        return "ERROR: No webcam image found. Capture may have failed."
    
    # Read and encode image
    with open(WEBCAM_PATH, "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')
    
    # Call Gemini via mcporter
    import urllib.request
    import json
    
    # Get API key from mcporter config
    api_key = "***REMOVED***"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": image_data
                    }
                }
            ]
        }]
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            
        # Extract text response
        if 'candidates' in result and result['candidates']:
            text = result['candidates'][0]['content']['parts'][0]['text']
            return text
        else:
            return "No analysis generated."
            
    except Exception as e:
        return f"ERROR during analysis: {str(e)}"

def main():
    prompt = "Describe what you see. Note the person, their expression, surroundings, and anything notable."
    
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    
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
    exit(main())
