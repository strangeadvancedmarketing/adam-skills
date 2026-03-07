# Email Plugin for OpenClaw

Gives Adam 10 native Gmail tools via IMAP/SMTP. No OAuth, no Google Cloud Console. Just a Gmail app password.

## What you get

| Tool | What it does |
|------|-------------|
| `email_search` | Search inbox by keyword, sender, or subject |
| `email_read` | Read full email body by UID |
| `email_send` | Send email via SMTP (supports reply threading) |
| `email_list_folders` | List all Gmail labels and folders |
| `email_delete` | Move to trash or permanently delete |
| `email_move` | Move emails between folders |
| `email_mark_read` | Mark as read or unread |
| `email_flag` | Star/flag emails |
| `email_bulk_operation` | Bulk delete/move/mark by sender, subject, or age |
| `email_analyze_senders` | Top 20 senders by volume (last 500 emails) |

## Setup (5 minutes)

### Step 1: Generate a Gmail App Password

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Security → 2-Step Verification (must be enabled)
3. At the bottom: **App passwords**
4. Select app: "Mail" → Select device: "Windows Computer"
5. Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)

### Step 2: Add to openclaw.json

```json
"plugins": {
  "allow": ["email"],
  "entries": {
    "email": {
      "enabled": true,
      "config": {
        "username": "your@gmail.com",
        "appPassword": "xxxx xxxx xxxx xxxx",
        "imapHost": "imap.gmail.com",
        "smtpHost": "smtp.gmail.com"
      }
    }
  }
}
```

### Step 3: Install the plugin

```powershell
# Copy plugin to your OpenClaw extensions directory
Copy-Item -Recurse "plugins/email" "C:\Users\<you>\.openclaw\extensions\email"
cd "C:\Users\<you>\.openclaw\extensions\email"
npm install
```

### Step 4: Restart OpenClaw

The plugin loads on startup. Restart your gateway and Adam will have all 10 email tools.

## Verification

Ask Adam: *"Check my email"* — he should return recent inbox items.

## Notes

- Works with any Gmail account (personal or Workspace)
- App password is separate from your Gmail password — revoking it doesn't affect your account
- IMAP must be enabled in Gmail settings (Settings → See all settings → Forwarding and POP/IMAP → Enable IMAP)
