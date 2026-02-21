# Human-in-the-Loop (HITL) Approval Workflow

**Tier:** Silver
**Version:** 1.0

---

## Overview

The HITL approval workflow enables the AI Employee to request user approval before executing sensitive actions like sending emails, processing payments, or scheduling meetings.

---

## Folder Structure

```
AI_Employee_Project/
├── Pending_Approval/     # New approval requests (Qwen creates these)
├── Approved/             # User-approved actions (move here to approve)
├── Rejected/             # User-rejected actions (move here to reject)
├── Done/                 # Executed or rejected approvals (archived)
├── Logs/
│   └── approval_log.txt  # Approval workflow audit log
└── Plans/
    └── PLAN_*.md         # Plans reference approval files
```

---

## Workflow Steps

### Step 1: Qwen Creates Approval Request

When Qwen identifies a sensitive action (via SKILL_CreatePlan):

1. Creates `Pending_Approval/[Action]_[timestamp].md`
2. Includes full execution details (to, subject, body, etc.)
3. Orchestrator detects new file and notifies user

**Orchestrator output:**
```
⚠️  Approval needed: 1 file(s)
📋 SendEmail_EMAIL_12345.md
   Action: send_email
   To: client@example.com
   Subject: Re: Product Inquiry
   → Review: Pending_Approval/SendEmail_EMAIL_12345.md
   → To approve: Move to Approved/
   → To reject: Move to Rejected/
```

### Step 2: User Reviews Approval

User opens the file in `Pending_Approval/` and reviews:
- Action type (send_email, process_payment, etc.)
- Recipient/details
- Full content (email body, payment amount, etc.)

### Step 3a: User Approves

**To approve:** Move file to `Approved/` folder

```bash
# Windows Explorer: Drag file to Approved/
# Or command line:
move Pending_Approval\SendEmail_*.md Approved\
```

**Orchestrator detects and executes:**
```
✅ Approved actions ready: 1
📄 Processing approval: SendEmail_EMAIL_12345.md
📋 Action Type: send_email
   To: client@example.com
   Subject: Re: Product Inquiry
   ✅ SUCCESS: Email sent to client@example.com
   📧 Message ID: SENT_20260218103000
   📝 Logged: EXECUTED: SendEmail_EMAIL_12345.md → Email sent
```

**After execution:**
- File moved to `Done/`
- Log entry in `Logs/approval_log.txt`
- Plan updated to "Completed"

### Step 3b: User Rejects

**To reject:** Move file to `Rejected/` folder

```bash
# Windows Explorer: Drag file to Rejected/
# Or command line:
move Pending_Approval\SendEmail_*.md Rejected\
```

**Orchestrator processes rejection:**
```
❌ Rejected actions: 1
📄 Rejected: SendEmail_EMAIL_12345.md
📝 Logged: REJECTED: SendEmail_EMAIL_12345.md
```

**After rejection:**
- File renamed to `REJECTED_SendEmail_*.md`
- Moved to `Done/`
- Status updated to "Rejected by user"
- Plan updated accordingly

---

## Approval File Template

When Qwen creates an approval file, use this format:

```markdown
# Approval Required: [Action Name]

**Source Plan:** [PLAN_*.md link]
**Source File:** [original Needs_Action file]
**Created:** [timestamp]
**Status:** Awaiting Approval

---

## Action Details

**Action:** send_email

**What:** [Clear description]

**Why:** [Reason needed]

---

## Execution Details

**To:** recipient@example.com
**Subject:** Email Subject
**CC:** (optional)
**Attachment:** (optional path or "None")

**Body:**
> [Full email body text]

---

## Approval

To approve this action:
1. Review the details above
2. Move this file to `Approved/` folder
3. Orchestrator will send the email automatically

To reject:
1. Move this file to `Rejected/` folder
2. Add a note explaining why (optional)

- [ ] **User Approval:** [ ] Approved  [ ] Rejected

---

## Status

- [ ] Awaiting approval
- [ ] Approved - Ready to execute
- [ ] Executed successfully
- [ ] Rejected by user

---

*Created by SKILL_CreatePlan - Silver Tier Approval Workflow*
```

---

## Supported Action Types

| Action Type | Description | Fields Required |
|-------------|-------------|-----------------|
| `send_email` | Send via Gmail SMTP | to, subject, body, (optional: cc, attachment) |
| `send_message` | WhatsApp message | to, message (requires WhatsApp Business API) |
| `process_payment` | Financial transaction | amount, recipient, account (requires banking API) |
| `schedule_meeting` | Calendar event | date, time, attendees, subject (requires calendar API) |

---

## Orchestrator Polling

The orchestrator checks folders every 30 seconds:

1. **Approved/** - Execute actions immediately
2. **Rejected/** - Log and archive
3. **Pending_Approval/** - Notify user of new requests
4. **Needs_Action/** - Generate Qwen prompts

---

## Audit Log

All approval actions are logged to `Logs/approval_log.txt`:

```
[2026-02-18T10:30:00] EXECUTED: SendEmail_EMAIL_12345.md → Email sent to client@example.com
[2026-02-18T10:35:00] REJECTED: SendEmail_EMAIL_67890.md → User rejected
[2026-02-18T11:00:00] FAILED: SendEmail_EMAIL_11111.md → SMTP Authentication failed
```

---

## Example: Email Approval Flow

### 1. Qwen Creates Approval File

```markdown
# Approval Required: Send Email - Client Reply

**Source Plan:** PLAN_20260218_EMAIL_12345.md
**Created:** 2026-02-18T10:30:00

## Action Details
**Action:** send_email
**What:** Reply to client product inquiry
**Why:** Client asked about pricing

## Execution Details
**To:** client@example.com
**Subject:** Re: Product Inquiry
**Body:**
> Dear Client,
> Thank you for your interest...
```

### 2. User Reviews

User opens `Pending_Approval/SendEmail_EMAIL_12345.md`, reads content.

### 3. User Approves

User moves file to `Approved/`:
```bash
move Pending_Approval\SendEmail_EMAIL_12345.md Approved\
```

### 4. Orchestrator Executes

```
✅ Approved actions ready: 1
📄 Processing approval: SendEmail_EMAIL_12345.md
📧 Sending email to: client@example.com
   Subject: Re: Product Inquiry
   ✅ SUCCESS: Email sent!
   📧 Message ID: SENT_20260218103000
```

### 5. File Archived

- Moved to `Done/SendEmail_EMAIL_12345.md`
- Log entry created
- Plan marked complete

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "Email MCP not available" | python-dotenv not installed | `pip install python-dotenv` |
| "Recipient email not found" | Missing 'to:' field | Check approval file format |
| "Email body not found" | Missing body content | Ensure body is in correct format |
| "SMTP Authentication failed" | Wrong credentials | Check .env app password |
| "Action type unknown" | Invalid action field | Use: send_email, send_message, etc. |

---

## Best Practices

1. **Always review before approving** - Check recipient, subject, and body
2. **Use descriptive filenames** - Include action type and source
3. **Add notes for rejections** - Helps Qwen learn preferences
4. **Monitor approval_log.txt** - Audit trail for compliance
5. **Keep DRY_RUN=true** for testing - Prevents accidental sends

---

## Qwen Instructions

When creating approval requests, Qwen should:

1. **Use the template** - Consistent format helps parsing
2. **Include all fields** - action, to, subject, body
3. **Be specific in "What" and "Why"** - Context for user review
4. **Quote email body with `>`** - Distinguishes from metadata
5. **Link to source plan** - Traceability

---

## User Quick Reference

| Action | Command |
|--------|---------|
| View pending | Open `Pending_Approval/` in Explorer |
| Approve | Move file to `Approved/` |
| Reject | Move file to `Rejected/` |
| Check status | Look in `Logs/approval_log.txt` |
| View executed | Check `Done/` folder |

---

*HITL Approval Workflow - Silver Tier*
