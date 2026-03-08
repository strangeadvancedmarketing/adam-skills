# Notes Skill

**Purpose:** Save notes, ideas, and reminders directly to your vault.  
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
python "scripts/notes.py" search "keyword"
```

## Where notes are saved

`<vault>/workspace/notes/YYYY-MM-DD.md`

Each day gets its own file. Notes are appended chronologically with timestamps.

```markdown
## 2:34 PM
Order volume was up 23% this week. Consider restocking inventory.

## 4:17 PM
Follow up with supplier about the pending order next Tuesday.
```

## Why this matters

Notes written here are automatically picked up by Adam's memory system (Layer 2 — memory-core plugin scans the vault). Write a note once. Adam remembers it forever.

## Configuration

Path defaults to `C:\AdamsVault\workspace\notes`. Override with the `VAULT_PATH` environment variable:
```
VAULT_PATH=C:\YourVault
```

## Dependencies

- Python 3.x (stdlib only)
