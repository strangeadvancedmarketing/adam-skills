#!/usr/bin/env python3
"""
Glance — Webcam Capture for Adam
Snaps one frame from built-in webcam, archives it, and releases immediately.
Camera light turns off as soon as script exits.
"""

import cv2
import os
from datetime import datetime
from pathlib import Path

# Paths
VAULT_ROOT = Path("C:/Adam's Vault")
VISION_DIR = VAULT_ROOT / "workspace" / "vision"
ARCHIVE_DIR = VISION_DIR / "archives"
OUTPUT_PATH = VISION_DIR / "webcam.png"

def capture_webcam():
    """Capture single frame from default webcam."""
    
    # Ensure directories exist
    VISION_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Open camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW for Windows stability
    
    if not cap.isOpened():
        print("ERROR: Could not open webcam")
        return None
    
    # Wait for auto-focus/exposure warmup
    for _ in range(10):
        cap.read()
    
    # Capture one frame
    ret, frame = cap.read()
    
    # Release immediately — camera light goes off
    cap.release()
    
    if not ret:
        print("ERROR: Could not capture frame")
        return None
    
    # Save current frame
    cv2.imwrite(str(OUTPUT_PATH), frame)
    
    # Archive with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_name = f"{timestamp}_Webcam.png"
    archive_path = ARCHIVE_DIR / archive_name
    cv2.imwrite(str(archive_path), frame)
    
    print(f"Captured: {OUTPUT_PATH}")
    print(f"Archived: {archive_path}")
    print(f"Obsidian embed: ![[{archive_name}]]")
    
    return str(archive_name)

if __name__ == "__main__":
    result = capture_webcam()
    if result:
        print(f"EMBED_LINK:{result}")
