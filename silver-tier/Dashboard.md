# Personal AI Employee Dashboard

**Tier:** Silver
**Reasoning Engine:** Qwen
**Last Updated:** <!-- Qwen will update this -->

---

## 📊 Status Overview

| Folder | Count | Description |
|--------|-------|-------------|
| 📥 Inbox | `<!-- count -->` | Raw files dropped by user |
| ⚠️ Needs Action | `<!-- count -->` | Files awaiting processing |
| ⏳ Pending Approval | `<!-- count -->` | Actions awaiting user approval |
| ✅ Approved | `<!-- count -->` | Ready for execution |
| ✅ Done | `<!-- count -->` | Completed files |
| 📋 Plans | `<!-- count -->` | Generated action plans |

---

## 🔄 Current Queue

<!-- Qwen will populate this section with active items from Needs_Action -->

| File | Type | Priority | Status | Notes |
|------|------|----------|--------|-------|
| *No items in queue* | - | - | - | - |

---

## ⏳ Pending Approvals

<!-- Qwen will populate with items awaiting user approval -->

| Action | Source | Created | Status |
|--------|--------|---------|--------|
| *No pending approvals* | - | - | - |

---

## 📈 Processing Log

<!-- Qwen will append processing entries here -->

| Timestamp | File | Action | Result |
|-----------|------|--------|--------|
| 2026-02-18 18:20:00 | 10 EMAIL_*.md files | Batch Email Processing | All emails categorized - moved to Done/ |
| 2026-02-17 16:34:11 | FILE_20260217_163320_prject.md | Analyzed & Archived | Empty file - moved to Done/ |
| 2026-02-17 16:34:11 | FILE_20260217_163403_tes.txt | Analyzed & Archived | Empty file - moved to Done/ |

---

## 📧 Recent Emails Processed

<!-- Qwen will append email processing entries -->

| Timestamp | Message ID | From | Subject | Status |
|-----------|------------|------|---------|--------|

## 📱 Recent WhatsApp Messages

<!-- Qwen will append WhatsApp message entries -->

| Timestamp | Chat | Preview | Priority | Status |
|-----------|------|---------|----------|--------|
| *No messages processed yet* | - | - | - | - |

---

## 📊 Today's Statistics

<!-- Qwen will update daily stats -->

| Metric | Count |
|--------|-------|
| Files Processed | 10 |
| Emails Processed | 10 |
| WhatsApp Messages | 0 |
| Approvals Created | 0 |
| Approvals Executed | 0 |
| Emails Sent | 0 |
| Plans Created | 1 |

---

## 🕐 Time-Based Triggers

| Trigger | Last Run | Next Scheduled |
|---------|----------|----------------|
| Daily Briefing (8 AM) | - | Tomorrow 8:00 AM |
| LinkedIn Post (Mon 9 AM) | - | Next Monday 9:00 AM |
| EOD Summary (5 PM) | - | Today 5:00 PM |

---

## 🎯 Active Goals

1. Process all files in Needs_Action queue
2. Monitor Gmail for important emails
3. Monitor WhatsApp for priority messages
4. Generate daily briefings at 8 AM
5. Create LinkedIn posts on Monday 9 AM
6. Execute approved actions automatically

---

## 📁 Folder Structure

```
AI_Employee_Project/
├── Inbox/                    # Drop files here
├── Needs_Action/             # Files awaiting processing
│   ├── FILE_*.md            # Dropped files
│   ├── EMAIL_*.md           # Gmail messages
│   └── WHATSAPP_*.md        # WhatsApp messages
├── Pending_Approval/         # Actions awaiting approval
├── Approved/                 # Approved actions (auto-execute)
├── Rejected/                 # Rejected actions
├── Done/                     # Completed items
├── Plans/                    # Action plans & briefings
│   ├── PLAN_*.md            # Processing plans
│   ├── Daily_Briefing_*.md  # Daily briefings
│   ├── LINKEDIN_POST_*.md   # Social post drafts
│   └── EOD_Summary_*.md     # End-of-day summaries
├── Skills/                   # Agent skill definitions
├── Logs/                     # System logs
│   ├── email_log.txt        # Email send logs
│   └── approval_log.txt     # Approval workflow logs
├── src/                      # Core source code
│   ├── orchestrator.py       # Main orchestrator
│   ├── email_mcp.py          # Email sender (Silver)
│   └── reasoning_loop.py     # Automatic processing
├── watchers/                 # Monitoring services
│   ├── filesystem_watcher.py # File monitor (Bronze)
│   ├── gmail_watcher.py      # Gmail monitor (Silver)
│   └── whatsapp_watcher.py   # WhatsApp monitor (Silver)
├── Dashboard.md              # This file
└── Company_Handbook.md       # Company info
```

---

## 🔗 Quick Links

- [Pending Approvals](Pending_Approval/) - Review and approve actions
- [Approved Queue](Approved/) - Ready for execution
- [Processing Plans](Plans/) - Active and completed plans
- [Email Logs](Logs/email_log.txt) - Email send history
- [Approval Logs](Logs/approval_log.txt) - Approval audit trail

---

*This dashboard is automatically maintained by Qwen AI Employee - Silver Tier*


## Processing Log
- [2026-02-21 03:43] Reasoning Loop: Auto-processed files
- [2026-02-20 17:45] Reasoning Loop: Auto-processed files
- [2026-02-19 13:08] Reasoning Loop: Auto-processed files
