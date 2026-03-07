import sys
import os
from datetime import datetime

VAULT_NOTES = r"C:\AdamsVault\workspace\notes"

def get_today_file():
    os.makedirs(VAULT_NOTES, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(VAULT_NOTES, f"{today}.md")

def save_note(content):
    path = get_today_file()
    timestamp = datetime.now().strftime("%-I:%M %p") if sys.platform != "win32" else datetime.now().strftime("%I:%M %p").lstrip("0")
    entry = f"\n## {timestamp}\n{content.strip()}\n"
    
    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)
    
    print(f"✅ Note saved to {os.path.basename(path)}")

def list_notes(limit=5):
    if not os.path.exists(VAULT_NOTES):
        print("No notes yet.")
        return
    
    files = sorted([f for f in os.listdir(VAULT_NOTES) if f.endswith(".md")], reverse=True)
    if not files:
        print("No notes yet.")
        return
    
    count = 0
    for fname in files:
        if count >= limit:
            break
        fpath = os.path.join(VAULT_NOTES, fname)
        print(f"\n📅 {fname.replace('.md', '')}")
        with open(fpath, encoding="utf-8") as f:
            print(f.read().strip())
        count += 1

def search_notes(query):
    if not os.path.exists(VAULT_NOTES):
        print("No notes yet.")
        return
    
    files = sorted([f for f in os.listdir(VAULT_NOTES) if f.endswith(".md")], reverse=True)
    found = []
    
    for fname in files:
        fpath = os.path.join(VAULT_NOTES, fname)
        with open(fpath, encoding="utf-8") as f:
            content = f.read()
        if query.lower() in content.lower():
            found.append((fname, content))
    
    if not found:
        print(f"No notes found matching '{query}'")
        return
    
    for fname, content in found[:3]:
        print(f"\n📅 {fname.replace('.md', '')}")
        for line in content.split("\n"):
            if query.lower() in line.lower():
                print(f"  → {line.strip()}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "save" and len(sys.argv) > 2:
        save_note(" ".join(sys.argv[2:]))
    elif cmd == "list":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        list_notes(limit)
    elif cmd == "search" and len(sys.argv) > 2:
        search_notes(" ".join(sys.argv[2:]))
    else:
        print("Usage: notes.py [save <text>|list [n]|search <query>]")
