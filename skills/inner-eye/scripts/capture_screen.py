# capture_screen.py - Adam's Inner Eye (Multi-Monitor Edition)
# Captures one or all monitors and saves to the vault.
#
# Monitor layout (adjust to match your setup):
#   Index 1 = Primary monitor (default)
#   Index 2 = Secondary monitor
#   Index 3 = Third monitor
#   "all"   = Full panoramic stitch of all monitors
#
# Usage:
#   python capture_screen.py        -> defaults to monitor 1 (primary)
#   python capture_screen.py 1      -> monitor 1
#   python capture_screen.py 2      -> monitor 2
#   python capture_screen.py all    -> all monitors stitched
#
# Output files (path set via VAULT_PATH env var or default):
#   <vault>/workspace/vision/screen.png
#   <vault>/workspace/vision/screen.b64

import mss
import mss.tools
import os
import sys
import base64
from datetime import datetime

VAULT_ROOT   = os.environ.get("VAULT_PATH", r"C:\AdamsVault")
OUTPUT_PATH  = os.path.join(VAULT_ROOT, "workspace", "vision", "screen.png")
B64_PATH     = os.path.join(VAULT_ROOT, "workspace", "vision", "screen.b64")

def capture(monitor_arg="1"):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with mss.mss() as sct:
        total_monitors = len(sct.monitors) - 1

        if str(monitor_arg).strip().lower() == "all":
            index = 0
        else:
            try:
                index = int(monitor_arg)
            except ValueError:
                print(f"[Inner Eye] WARNING: Invalid argument '{monitor_arg}'. Defaulting to monitor 1.", file=sys.stderr)
                index = 1

        if index != 0 and index > total_monitors:
            print(f"[Inner Eye] WARNING: Monitor {index} not found ({total_monitors} connected). Defaulting to monitor 1.", file=sys.stderr)
            index = 1

        monitor = sct.monitors[index]
        screenshot = sct.grab(monitor)
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=OUTPUT_PATH)

    with open(OUTPUT_PATH, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("utf-8")
    with open(B64_PATH, "w") as f:
        f.write(b64_data)

    size_kb   = os.path.getsize(OUTPUT_PATH) // 1024
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    label     = "All Monitors (Panoramic)" if index == 0 else f"Monitor {index}"

    print(f"[Inner Eye] Captured: {label}")
    print(f"[Inner Eye] Timestamp: {timestamp}")
    print(f"[Inner Eye] Saved to: {OUTPUT_PATH} ({size_kb} KB)")
    print(f"[Inner Eye] Resolution: {screenshot.width}x{screenshot.height}")
    print(f"[Inner Eye] Base64 ready: {B64_PATH}")
    return OUTPUT_PATH, b64_data

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "1"
    try:
        capture(arg)
        sys.exit(0)
    except Exception as e:
        print(f"[Inner Eye] ERROR: {e}", file=sys.stderr)
        sys.exit(1)
