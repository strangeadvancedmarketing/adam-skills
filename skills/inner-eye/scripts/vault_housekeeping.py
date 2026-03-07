# vault_housekeeping.py - Adam's Visual Archive Cleaner
# Scans the vision archives folder and deletes .png files older than 14 days.
# Safe to run at any time — only removes files past the retention threshold.
#
# Usage:
#   python vault_housekeeping.py

import os
import sys
from datetime import datetime, timedelta

ARCHIVE_DIR    = r"C:\AdamsVault\workspace\vision\archives"
RETENTION_DAYS = 14

def housekeeping():
    if not os.path.exists(ARCHIVE_DIR):
        print(f"[Housekeeping] Archive directory not found: {ARCHIVE_DIR}")
        print("[Housekeeping] Nothing to clean.")
        return

    cutoff   = datetime.now() - timedelta(days=RETENTION_DAYS)
    all_png  = [f for f in os.listdir(ARCHIVE_DIR) if f.lower().endswith(".png")]
    deleted  = []
    errors   = []

    for filename in all_png:
        filepath = os.path.join(ARCHIVE_DIR, filename)
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if mtime < cutoff:
                os.remove(filepath)
                deleted.append(filename)
        except Exception as e:
            errors.append(f"{filename}: {e}")

    remaining = len([f for f in os.listdir(ARCHIVE_DIR) if f.lower().endswith(".png")])

    print(f"[Housekeeping] Retention policy : {RETENTION_DAYS} days")
    print(f"[Housekeeping] Cutoff date       : {cutoff.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[Housekeeping] Scanned           : {len(all_png)} file(s)")

    if deleted:
        print(f"[Housekeeping] Deleted {len(deleted)} old screenshot(s):")
        for f in deleted:
            print(f"  - {f}")
    else:
        print("[Housekeeping] No files old enough to delete.")

    if errors:
        for e in errors:
            print(f"[Housekeeping] ERROR: {e}", file=sys.stderr)

    print(f"[Housekeeping] Complete. Deleted: {len(deleted)} | Remaining: {remaining}")

if __name__ == "__main__":
    try:
        housekeeping()
        sys.exit(0)
    except Exception as e:
        print(f"[Housekeeping] FATAL: {e}", file=sys.stderr)
        sys.exit(1)
