# Notes Skill

**Purpose:** Save notes, ideas, and reminders directly to your AdamsVault.  
**Setup required:** None. Writes to your local vault directory.

## Trigger phrases

- "Make a note: [text]"
- "Remember this: [text]"
- "Save this idea: [text]"
- "Add to my notes: [text]"
- "Note to self: [text]"
- "What are my notes?"
- "Show me my recent notes"

## How to use it

### Save a note
```bash
python "scripts/notes.py" save "Your note content here"
```

### List recent notes
```bash
python "scripts/notes.py" list
python "scripts/notes.py" list 10    # Show last 10
```

### Search notes
```bash
python "scripts/notes.py" search "shopify"
```

## Where notes are saved

`C:\AdamsVault\workspace\notes\YYYY-MM-DD.md`

Each day gets its own file. Notes are appended chronologically with timestamps.

```markdown
## 2:34 PM
Shopify order volume was up 23% this week. Consider restocking Barrel Vaults.

## 4:17 PM
Follow up with Carlos about the Davie turf job next Tuesday.
```

## Why this matters

Notes written here are automatically picked up by Adam's memory system (Layer 2 — memory-core plugin scans the vault). Write a note once. Adam remembers it forever.

## Dependencies

- Python 3.x (stdlib only)
- AdamsVault directory must exist at `C:\AdamsVault\workspace\notes\`

## Customization

Change the vault path in `scripts/notes.py` line 8 to match your vault location.
