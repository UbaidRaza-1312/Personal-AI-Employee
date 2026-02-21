# Silver Tier Approval Workflow - Quick Reference

## 📁 Folder Structure

```
Pending_Approval/  ← Qwen creates approval requests here
Approved/          ← Move files here to approve & execute
Rejected/          ← Move files here to reject & cancel
Done/              ← Executed/rejected files archived here
```

---

## 🔄 User Workflow

### When Orchestrator Shows:
```
⚠️  Approval needed: 1 file(s)
📋 SendEmail_EMAIL_12345.md
   Action: send_email
   To: client@example.com
   → Review: Pending_Approval/SendEmail_EMAIL_12345.md
   → To approve: Move to Approved/
   → To reject: Move to Rejected/
```

### To APPROVE:
1. Open `Pending_Approval/SendEmail_EMAIL_12345.md`
2. Review the email content
3. **Move file to `Approved/` folder**
4. Orchestrator will auto-execute (within 30 seconds)
5. Check `Logs/approval_log.txt` for confirmation

### To REJECT:
1. Open `Pending_Approval/SendEmail_EMAIL_12345.md`
2. (Optional) Add a note explaining why
3. **Move file to `Rejected/` folder**
4. Orchestrator will archive with "Rejected" status

---

## 📋 Approval File Format

```markdown
# Approval Required: [Action Name]

**Action:** send_email

**To:** recipient@example.com
**Subject:** Email Subject
**Body:**
> [Email content here]

---

## Approval

- [ ] **User Approval:** [ ] Approved  [ ] Rejected

**To approve:** Move to Approved/ folder
**To reject:** Move to Rejected/ folder
```

---

## 🎯 Supported Actions

| Action | Fields | Status |
|--------|--------|--------|
| `send_email` | to, subject, body, (cc, attachment) | ✅ Implemented |
| `send_message` | to, message | ⚠️ Requires WhatsApp Business API |
| `process_payment` | amount, recipient | ⚠️ Requires banking integration |
| `schedule_meeting` | date, time, attendees | ⚠️ Requires calendar API |

---

## 📊 Orchestrator Output Examples

### Approval Request Detected
```
⚠️  Approval needed: 1 file(s)
📋 SendEmail_EMAIL_12345.md
   Action: send_email
   To: client@example.com
   Subject: Re: Inquiry
   → Review: Pending_Approval/SendEmail_EMAIL_12345.md
   → To approve: Move to Approved/
   → To reject: Move to Rejected/
```

### Approved - Executing
```
✅ Approved actions ready: 1
📄 Processing approval: SendEmail_EMAIL_12345.md

📋 Action Type: send_email
   To: client@example.com
   Subject: Re: Inquiry
   ✅ SUCCESS: Email sent to client@example.com
   📧 Message ID: SENT_20260218103000
   📝 Logged: EXECUTED: SendEmail_EMAIL_12345.md
```

### Rejected
```
❌ Rejected actions: 1
📄 Rejected: SendEmail_EMAIL_12345.md
📝 Logged: REJECTED: SendEmail_EMAIL_12345.md
```

---

## 🔧 Quick Commands

### Windows Explorer
```
# Open folders
explorer Pending_Approval
explorer Approved
explorer Rejected

# Move files (drag & drop in Explorer)
```

### Command Line
```bash
# Approve
move Pending_Approval\SendEmail_*.md Approved\

# Reject
move Pending_Approval\SendEmail_*.md Rejected\

# View log
type Logs\approval_log.txt
```

---

## 📝 Audit Log

Location: `Logs/approval_log.txt`

```
[2026-02-18T10:30:00] EXECUTED: SendEmail_EMAIL_12345.md → Email sent
[2026-02-18T10:35:00] REJECTED: SendEmail_EMAIL_67890.md → User rejected
[2026-02-18T11:00:00] FAILED: SendEmail_EMAIL_11111.md → SMTP error
```

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| File not auto-executing | Check Approved/ folder, ensure email_mcp.py installed |
| "Email MCP not available" | Run: `pip install python-dotenv` |
| Email not sending | Check .env credentials, DRY_RUN=false |
| File stays in Approved/ | Check Logs/approval_log.txt for error |

---

## ✅ Checklist for Qwen

When creating approval requests, ensure:

- [ ] File created in `Pending_Approval/`
- [ ] Action type specified: `action: send_email`
- [ ] Recipient included: `to: email@example.com`
- [ ] Subject line: `subject: ...`
- [ ] Full body text in `Body:` section with `>` quotes
- [ ] Approval instructions included
- [ ] Source plan linked

---

*Quick Reference - Silver Tier HITL Approval*
