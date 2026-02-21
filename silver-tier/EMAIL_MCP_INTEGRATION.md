# Email MCP Integration Guide

**Tier:** Silver
**Version:** 1.0

---

## Overview

The Email MCP server enables the AI Employee to send emails via Gmail SMTP when actions are approved by the user.

---

## Setup Steps

### 1. Install Dependencies

```bash
pip install python-dotenv
```

### 2. Configure Credentials

```bash
# Copy the example file
copy .env.example .env

# Edit .env with your credentials
```

### 3. Get Gmail App Password

**Important:** Use App Password, NOT your regular Gmail password.

1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification** (if not already enabled)
3. Go to https://myaccount.google.com/apppasswords
4. Select app: **"Mail"**
5. Select device: **"Other (Custom name)"**
6. Enter name: **"AI Employee"** → Click **Generate**
7. Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)
8. Paste into `.env` (remove spaces or keep them - both work)

### 4. Test the Email Server

```bash
# Test in dry-run mode (default)
python email_mcp.py

# Check Logs/email_log.txt for output
```

### 5. Enable Live Sending

Edit `.env`:
```
DRY_RUN=false
```

---

## Integration with Orchestrator

The orchestrator calls `email_mcp.py` when an approved action requires sending email.

### Workflow

```
1. Qwen creates plan with "Send Email" step
2. Qwen creates Pending_Approval/SendEmail_*.md
3. User reviews and approves (checks box)
4. Orchestrator detects approval
5. Orchestrator calls email_mcp.send_email()
6. Email sent via Gmail SMTP
7. Log written to Logs/email_log.txt
8. Plan marked complete
```

### Code Integration

Add to `orchestrator.py`:

```python
from email_mcp import send_email

def process_approved_email(approval_file: Path):
    """Send email from approved approval file."""
    # Parse approval file for email details
    content = approval_file.read_text()

    # Extract: to, subject, body, attachment (parse from YAML frontmatter)
    # ... parsing logic ...

    # Send email
    result = send_email(
        to=to_address,
        subject=subject,
        body=body,
        attachment_path=attachment
    )

    # Log result
    if result['success']:
        print(f"Email sent: {result['message_id']}")
        # Move approval file to Done
        # Update plan status
    else:
        print(f"Email failed: {result['message']}")
        # Keep in Pending_Approval for review
```

---

## File Structure

```
AI_Employee_Project/
├── email_mcp.py           # Email MCP server
├── .env                   # Credentials (gitignore this!)
├── .env.example           # Template (commit this)
├── Logs/
│   └── email_log.txt      # Email send logs
├── Pending_Approval/
│   └── SendEmail_*.md     # Emails awaiting approval
└── Plans/
    └── PLAN_*.md          # Plans with email steps
```

---

## Approval File Format

When Qwen creates an approval file for email:

```markdown
# Approval Required: Send Email

**Source Plan:** PLAN_20260218_EMAIL_12345.md
**Created:** 2026-02-18T10:30:00
**Status:** Awaiting Approval

## What
Send reply email to client inquiry

## Why
Client asked about pricing, drafted response using company info

## Details
- **To:** client@example.com
- **Subject:** Re: Product Inquiry
- **Body:**
  > Dear Client,
  >
  > Thank you for your interest...
- **Attachment:** (optional) quotes.pdf

## Approval
To approve: Check box below or reply "approved"

- [ ] **User Approval:** [ ] Approved  [ ] Rejected

## Status
- [ ] Awaiting approval
- [ ] Approved - Ready to execute
- [ ] Executed successfully
- [ ] Rejected by user
```

---

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GMAIL_EMAIL` | Gmail address to send from | Yes | '' |
| `GMAIL_APP_PASSWORD` | 16-char app password | Yes | '' |
| `DRY_RUN` | If true, log but don't send | No | 'true' |

---

## Function Reference

### `send_email()`

```python
from email_mcp import send_email

result = send_email(
    to="recipient@example.com",      # Required
    subject="Email Subject",          # Required
    body="Email body text",           # Required
    attachment_path="/path/to/file",  # Optional
    cc="cc@example.com",              # Optional
    bcc="bcc@example.com"             # Optional
)

# Result:
{
    'success': True/False,
    'message': 'Description of result',
    'message_id': 'SENT_20260218103000',
    'dry_run': True/False
}
```

### `send_email_from_template()`

```python
from email_mcp import send_email_from_template

result = send_email_from_template(
    to="recipient@example.com",
    subject="Email Subject",
    template_path="Templates/reply.txt",
    attachment_path="/path/to/file"
)
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| SMTP Authentication failed | Wrong email/password | Check .env, regenerate app password |
| SMTP Connect failed | Network/firewall | Check internet, allow smtp.gmail.com:587 |
| Gmail credentials not configured | .env missing | Copy .env.example to .env |
| Recipient required | Empty 'to' field | Provide valid email |

---

## Security Notes

- ⚠️ **Never commit `.env`** - Add to `.gitignore`
- ⚠️ **Use App Password** - Never use regular Gmail password
- ⚠️ **Keep DRY_RUN=true** for testing
- ✅ Logs stored in `Logs/email_log.txt`
- ✅ Message IDs tracked for audit

---

## Testing Checklist

- [ ] `.env` file created with credentials
- [ ] `pip install python-dotenv` completed
- [ ] Dry run test: `python email_mcp.py`
- [ ] Check `Logs/email_log.txt` for output
- [ ] Set `DRY_RUN=false` for live test
- [ ] Send test email to yourself
- [ ] Verify email received
- [ ] Test with attachment

---

## Troubleshooting

### "Authentication failed"
1. Verify 2-Step Verification is enabled
2. Regenerate App Password
3. Ensure no extra spaces in password (or keep all spaces - both work)

### "Connection timeout"
1. Check internet connection
2. Verify firewall allows port 587
3. Try `telnet smtp.gmail.com 587`

### Emails going to spam
1. Use a descriptive subject line
2. Include signature in body
3. Don't send bulk emails (Gmail has limits)

### Gmail sending limits
- 500 emails/day for Gmail
- 100 recipients/day for new accounts
- Wait 24 hours if limit reached

---

*Email MCP Server - Silver Tier Integration*
