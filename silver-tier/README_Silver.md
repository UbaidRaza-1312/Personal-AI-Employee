# Personal AI Employee - Silver Tier

[![Tier](https://img.shields.io/badge/Tier-Silver-blue)](https://github.com)
[![Status](https://img.shields.io/badge/Status-Active-success)](https://github.com)

A personal AI employee that monitors files, emails, and messages, processes them with Qwen AI, and executes approved actions automatically.

---

## 🎯 Silver Tier Features

| Feature | Description | Status |
|---------|-------------|--------|
| **File Monitoring** | Watch Inbox/ for new files | ✅ Bronze |
| **Gmail Monitoring** | Watch for unread+important emails | ✅ Silver |
| **WhatsApp Monitoring** | Monitor priority WhatsApp messages | ✅ Silver |
| **Email Sending** | Send emails via Gmail SMTP | ✅ Silver |
| **HITL Approval** | Human-in-the-loop approval workflow | ✅ Silver |
| **Daily Briefing** | Auto-generate morning briefings at 8 AM | ✅ Silver |
| **LinkedIn Posts** | Generate social posts Monday 9 AM | ✅ Silver |
| **EOD Summary** | End-of-day summaries at 5 PM | ✅ Silver |

---

## 📁 Project Structure

```
AI_Employee_Project/
├── src/                      # Core source code
│   ├── orchestrator.py       # Main orchestrator (Silver Tier)
│   ├── email_mcp.py          # Email sending via Gmail SMTP (Silver)
│   └── reasoning_loop.py     # Automatic rule-based processing
│
├── watchers/                 # Monitoring services
│   ├── filesystem_watcher.py # File monitoring (Bronze)
│   ├── gmail_watcher.py      # Gmail monitoring (Silver)
│   └── whatsapp_watcher.py   # WhatsApp monitoring (Silver)
│
├── .env                      # Credentials (create from .env.example)
├── .env.example              # Credential template
├── credentials.json          # Gmail OAuth (download from Google)
├── token.json                # Gmail auth token (auto-generated)
│
├── Skills/
│   ├── SKILL_ProcessFile.md
│   ├── SKILL_CreatePlan.md
│   └── SKILL_GenerateSocialPost.md
│
├── Inbox/                    # Drop files here
├── Needs_Action/             # Queue: Files/emails/messages
├── Pending_Approval/         # Awaiting user approval
├── Approved/                 # Approved for execution
├── Rejected/                 # Rejected by user
├── Done/                     # Completed items
├── Plans/                    # Action plans & briefings
├── Logs/                     # System logs
│
├── Dashboard.md              # Status tracking
├── Company_Handbook.md       # Company info
└── README_Silver.md          # This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Bronze Tier
pip install watchdog

# Silver Tier
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
pip install playwright
playwright install chromium
pip install python-dotenv
```

### 2. Configure Credentials

```bash
# Email MCP (for sending emails)
copy .env.example .env
# Edit .env with your Gmail credentials

# Gmail Watcher (for monitoring)
# Download credentials.json from Google Cloud Console
# See gmail_watcher.py for setup instructions
```

### 3. Start Services

**Option A: Full Silver Tier (all watchers + orchestrator)**

```bash
# Terminal 1: Orchestrator (required)
python src/orchestrator.py

# Terminal 2: File Watcher (optional)
python watchers/filesystem_watcher.py

# Terminal 3: Gmail Watcher (optional)
python watchers/gmail_watcher.py

# Terminal 4: WhatsApp Watcher (optional)
python watchers/whatsapp_watcher.py
```

**Option B: Minimal (orchestrator only)**

```bash
python src/orchestrator.py
```

**Option C: Automatic Processing (no AI, rule-based)**

```bash
# Run reasoning loop once
python src/reasoning_loop.py
```

---

## 🔄 How It Works

### File Flow (Bronze)

```
User drops file → Inbox/
     ↓
filesystem_watcher.py detects
     ↓
Copies to Needs_Action/ + creates .md metadata
     ↓
orchestrator.py detects (30s)
     ↓
Prints Qwen prompt
     ↓
User pastes into Qwen
     ↓
Qwen processes → Plans/ created → Files moved to Done/
```

### Email Flow (Silver)

```
Gmail receives email
     ↓
gmail_watcher.py polls (120s)
     ↓
Unread + Important detected
     ↓
Creates EMAIL_*.md in Needs_Action/
     ↓
orchestrator.py detects
     ↓
Qwen processes → Plan created
     ↓
If email reply needed → Pending_Approval/
     ↓
User moves to Approved/
     ↓
email_mcp.py sends automatically
```

### WhatsApp Flow (Silver)

```
WhatsApp message received
     ↓
whatsapp_watcher.py polls (60s)
     ↓
Unread + Priority keyword detected
     ↓
Creates WHATSAPP_*.md in Needs_Action/
     ↓
orchestrator.py detects
     ↓
Qwen processes → Plan created
     ↓
If reply needed → Pending_Approval/
     ↓
User reviews → Manual reply (API not implemented)
```

### Approval Flow (Silver)

```
Qwen identifies sensitive action
     ↓
Creates Pending_Approval/<Action>.md
     ↓
orchestrator.py notifies user
     ↓
User reviews file
     ↓
┌─────────────┬──────────────┐
│   Approve   │    Reject    │
├─────────────┼──────────────┤
│ Move to     │ Move to      │
│ Approved/   │ Rejected/    │
├─────────────┼──────────────┤
│ Auto-execute│ Log & archive│
│ (email sent)│              │
└─────────────┴──────────────┘
```

### Time-Based Triggers (Silver)

```
┌─────────────────────────────────────────────┐
│  Orchestrator checks time every 30 seconds  │
└─────────────────────────────────────────────┘
                    ↓
        ┌───────────┼───────────┐
        ↓           ↓           ↓
   8:00 AM    Monday 9 AM   5:00 PM
        ↓           ↓           ↓
   Daily       LinkedIn      EOD
   Briefing    Post         Summary
        ↓           ↓           ↓
   Qwen creates Plans/*.md files
```

---

## 📋 Test Flow: Complete Silver Tier

### Prerequisites

- [ ] All dependencies installed
- [ ] `.env` configured with Gmail credentials
- [ ] `credentials.json` downloaded (Gmail Watcher)
- [ ] `token.json` generated (first Gmail run)
- [ ] WhatsApp QR scanned (first WhatsApp run)

### Test Sequence

#### Step 1: Start All Services

```bash
# Terminal 1
python orchestrator.py

# Terminal 2
python filesystem_watcher.py

# Terminal 3
python gmail_watcher.py
```

#### Step 2: Test File Drop (Bronze)

1. Create test file: `test.txt` with content "Hello World"
2. Drop into `Inbox/`
3. **Expected:** Watcher prints "Processed: test.txt"
4. **Check:** `Needs_Action/FILE_*_test.txt` and `.md` created
5. **Orchestrator:** Detects and prints Qwen prompt
6. **User:** Paste prompt into Qwen
7. **Qwen:** Creates plan, updates Dashboard, moves to Done/

#### Step 3: Test Gmail (Silver)

1. Send yourself an email with subject "URGENT: Test Email"
2. Mark as Important (star it)
3. Leave unread
4. **Expected:** gmail_watcher.py detects within 120s
5. **Check:** `Needs_Action/EMAIL_*.md` created
6. **Orchestrator:** Detects and prints Qwen prompt
7. **User:** Paste into Qwen
8. **Qwen:** Analyzes email, creates plan

#### Step 4: Test Approval Workflow (Silver)

1. Qwen identifies "reply needed" action
2. **Qwen creates:** `Pending_Approval/SendEmail_*.md`
3. **Orchestrator notifies:**
   ```
   ⚠️  Approval needed: SendEmail_*.md
      → To approve: Move to Approved/
   ```
4. **User:** Open file, review email content
5. **User:** Move file to `Approved/`
6. **Orchestrator:** Detects within 30s
7. **Email MCP:** Sends email via Gmail SMTP
8. **Check:** `Logs/email_log.txt` shows success
9. **File:** Moved to `Done/`

#### Step 5: Test Time Trigger (Silver)

**Option A: Wait for scheduled time**
- Wait until 8 AM tomorrow for Daily Briefing
- Or wait until Monday 9 AM for LinkedIn Post

**Option B: Test immediately (modify orchestrator)**

Edit `orchestrator.py` temporarily:
```python
# Change this line in check_time_based_triggers()
if True:  # Was: if current_time.hour == 8
    triggers.append('daily_briefing')
```

Restart orchestrator:
```
⏰ Time trigger: Daily Briefing (8 AM)
📋 Paste the following prompt into Qwen chat:
...
```

**User:** Paste into Qwen
**Qwen:** Creates `Plans/Daily_Briefing_YYYYMMDD.md`

---

## 🔧 Configuration

### .env File

```env
# Email MCP
GMAIL_EMAIL=your@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
DRY_RUN=true  # Set to 'false' for live sending
```

### Getting Gmail App Password

1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Go to https://myaccount.google.com/apppasswords
4. Select: Mail → Other (Custom name)
5. Name: "AI Employee"
6. Copy 16-char password to `.env`

### Gmail Watcher Setup

1. https://console.cloud.google.com/
2. Create new project
3. Enable Gmail API
4. OAuth consent screen → External
5. Add scope: `gmail.readonly`
6. Create credentials → OAuth client ID → Desktop app
7. Download `credentials.json`
8. First run: `python gmail_watcher.py` → Authorize

---

## 📊 Dashboard

View `Dashboard.md` for:
- Current queue status
- Pending approvals
- Processing history
- Today's statistics
- Time trigger status

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Watcher not detecting files | Ensure file is created (not moved) in Inbox/ |
| Orchestrator shows 0 files | Check Needs_Action/ path, wait 30s |
| Email not sending | Check .env credentials, DRY_RUN=false |
| Gmail watcher fails | Regenerate token.json, check credentials.json |
| WhatsApp session expired | Delete whatsapp_session/, re-scan QR |
| Approval not executing | Check Approved/ folder, view Logs/approval_log.txt |
| Time trigger didn't fire | Ensure orchestrator running at trigger time |

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| `HITL_APPROVAL_WORKFLOW.md` | Approval workflow guide |
| `APPROVAL_QUICK_REF.md` | Quick approval reference |
| `EMAIL_MCP_INTEGRATION.md` | Email setup guide |
| `TIME_TRIGGERS_SOCIAL_POST.md` | Time triggers & social posts |
| `TIME_TRIGGERS_QUICK_REF.md` | Quick triggers reference |
| `SILVER_TIER_SUMMARY.md` | Complete Silver Tier summary |

---

## 🎯 Silver Tier Checklist

Before considering Silver Tier complete:

- [ ] File watcher working (Bronze)
- [ ] Gmail watcher working
- [ ] WhatsApp watcher working (or skipped)
- [ ] Email MCP configured
- [ ] Test email sent successfully
- [ ] Approval workflow tested
- [ ] Daily briefing triggered
- [ ] Dashboard.md updated with Silver sections
- [ ] All documentation reviewed

---

## 🔐 Security Notes

- ⚠️ Never commit `.env` - contains credentials
- ⚠️ Use App Password - not regular Gmail password
- ⚠️ WhatsApp automation may violate ToS
- ✅ Keep `DRY_RUN=true` for testing
- ✅ Review all approvals before executing
- ✅ Logs stored for audit trail

---

## 📞 Support

For issues or questions:
1. Check `Logs/` for error messages
2. Review documentation files
3. Verify all dependencies installed
4. Ensure credentials configured correctly

---

*Personal AI Employee - Silver Tier*
*Last Updated: 2026-02-18*
