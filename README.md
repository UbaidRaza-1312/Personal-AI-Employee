# Personal AI Employee

A multi-tier AI-powered employee system that automates file processing, email monitoring, WhatsApp messaging, and social media management using Qwen AI.

![Tier](https://img.shields.io/badge/Tiers-Bronze%20%7C%20Silver-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.7+-green)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tier Comparison](#tier-comparison)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Documentation](#documentation)
- [Security](#security)

---

## 🎯 Overview

The Personal AI Employee is an autonomous agent system designed to:

1. **Monitor** multiple input channels (files, emails, WhatsApp messages)
2. **Process** incoming tasks using Qwen AI reasoning
3. **Plan** actions with human-in-the-loop approval for sensitive operations
4. **Execute** approved actions automatically (email sending, etc.)
5. **Track** all activity through a centralized dashboard

### Key Features

- 📁 **File Processing** - Drop files, AI analyzes and executes tasks
- 📧 **Gmail Integration** - Monitor important emails, auto-reply with approval
- 📱 **WhatsApp Monitoring** - Track priority messages from key contacts
- ✅ **HITL Approval** - Human review for sensitive actions
- ⏰ **Time Triggers** - Scheduled daily briefings, social posts, EOD summaries
- 📊 **Dashboard** - Real-time status tracking and activity logs

---

## 🥉 Tier Comparison

| Feature | Bronze Tier | Silver Tier |
|---------|-------------|-------------|
| **File Monitoring** | ✅ | ✅ |
| **Gmail Monitoring** | ❌ | ✅ |
| **WhatsApp Monitoring** | ❌ | ✅ |
| **Email Sending** | ❌ | ✅ (with approval) |
| **HITL Approval Workflow** | ❌ | ✅ |
| **Daily Briefing (8 AM)** | ❌ | ✅ |
| **LinkedIn Posts (Mon 9 AM)** | ❌ | ✅ |
| **EOD Summary (5 PM)** | ❌ | ✅ |
| **Auto-Execution** | Manual | Rule-based + Approved |
| **Complexity** | Simple | Advanced |

### Which Tier to Use?

- **Bronze Tier**: Start here for basic file automation and AI task processing
- **Silver Tier**: Upgrade for full email/WhatsApp integration and scheduled automation

---

## 📁 Project Structure

```
Personal-AI-Employee/
├── bronze-tier/                    # Bronze Tier Implementation
│   ├── orchestrator.py             # Main orchestration loop
│   ├── filesystem_watcher.py       # Inbox monitoring service
│   ├── Dashboard.md                # Status overview
│   ├── Company_Handbook.md         # Operating principles
│   ├── README.md                   # Bronze-specific docs
│   ├── Inbox/                      # Drop zone for new files
│   ├── Needs_Action/               # Files awaiting AI processing
│   ├── Done/                       # Completed work
│   ├── Plans/                      # Action plans created by Qwen
│   ├── Skills/                     # Skill definitions
│   └── Logs/                       # System logs
│
├── silver-tier/                    # Silver Tier Implementation
│   ├── src/                        # Core source code
│   │   ├── orchestrator.py         # Main orchestrator (Silver)
│   │   ├── email_mcp.py            # Email sending via Gmail SMTP
│   │   └── reasoning_loop.py       # Automatic rule-based processing
│   ├── watchers/                   # Monitoring services
│   │   ├── filesystem_watcher.py   # File monitoring (Bronze)
│   │   ├── gmail_watcher.py        # Gmail monitoring (Silver)
│   │   └── whatsapp_watcher.py     # WhatsApp monitoring (Silver)
│   ├── .env.example                # Credential template
│   ├── credentials.json            # Gmail OAuth (user-provided)
│   ├── token.json                  # Gmail auth token (auto-generated)
│   ├── Skills/                     # Enhanced skill definitions
│   ├── Inbox/                      # Drop zone
│   ├── Needs_Action/               # Queue: Files/emails/messages
│   ├── Pending_Approval/           # Awaiting user approval
│   ├── Approved/                   # Approved for execution
│   ├── Rejected/                   # Rejected by user
│   ├── Done/                       # Completed items
│   ├── Plans/                      # Plans & briefings
│   ├── Logs/                       # System logs
│   └── Dashboard.md                # Silver dashboard
│
└── README.md                       # This file (root documentation)
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- Qwen AI access (via VS Code or other interface)
- Gmail account (for Silver Tier email features)

### Installation

#### Bronze Tier (Minimal Setup)

```bash
# Navigate to bronze-tier
cd bronze-tier

# Install dependencies
pip install watchdog

# Start the system
# Terminal 1: Filesystem Watcher
python filesystem_watcher.py

# Terminal 2: Orchestrator
python orchestrator.py
```

#### Silver Tier (Full Features)

```bash
# Navigate to silver-tier
cd silver-tier

# Install all dependencies
pip install watchdog google-api-python-client google-auth-oauthlib google-auth-httplib2
pip install playwright python-dotenv
playwright install chromium

# Configure credentials
copy .env.example .env
# Edit .env with your Gmail credentials

# Download credentials.json from Google Cloud Console (see documentation)

# Start all services
# Terminal 1: Orchestrator (required)
python src/orchestrator.py

# Terminal 2: File Watcher (optional)
python watchers/filesystem_watcher.py

# Terminal 3: Gmail Watcher (optional)
python watchers/gmail_watcher.py

# Terminal 4: WhatsApp Watcher (optional)
python watchers/whatsapp_watcher.py
```

### First Run

1. **Drop a test file** into `Inbox/` folder
2. **Watcher detects** and copies to `Needs_Action/` with metadata
3. **Orchestrator prints** a Qwen prompt every 30 seconds
4. **Copy prompt** into Qwen chat
5. **Qwen processes** the task and creates plans
6. **Dashboard updates** with completed work

---

## 🔄 How It Works

### File Processing Flow (Bronze & Silver)

```
User drops file → Inbox/
        ↓
filesystem_watcher.py detects (instant)
        ↓
Copies to Needs_Action/ + creates .md metadata
        ↓
orchestrator.py detects (every 30s)
        ↓
Prints Qwen prompt to console
        ↓
User pastes into Qwen chat
        ↓
Qwen analyzes → Creates plan → Executes → Updates Dashboard
        ↓
Files moved to Done/
```

### Email Flow (Silver Only)

```
Gmail receives email
        ↓
gmail_watcher.py polls (every 120s)
        ↓
Unread + Important detected
        ↓
Creates EMAIL_*.md in Needs_Action/
        ↓
orchestrator.py detects
        ↓
Qwen processes → Plan created
        ↓
If reply needed → Pending_Approval/
        ↓
User moves to Approved/
        ↓
email_mcp.py sends automatically → Done/
```

### Approval Workflow (Silver Only)

```
Qwen identifies sensitive action (email, payment, etc.)
        ↓
Creates Pending_Approval/<Action>.md
        ↓
orchestrator.py notifies user (every 30s)
        ↓
┌─────────────────┬──────────────────┐
│    Approve      │     Reject       │
├─────────────────┼──────────────────┤
│ Move to         │ Move to          │
│ Approved/       │ Rejected/        │
├─────────────────┼──────────────────┤
│ Auto-execute    │ Log & archive    │
│ (email sent)    │                  │
└─────────────────┴──────────────────┘
```

### Time-Based Triggers (Silver Only)

```
Orchestrator checks time every 30 seconds
        ↓
    ┌───┴───┬───────────┐
    ↓       ↓           ↓
8:00 AM  Mon 9 AM    5:00 PM
    ↓       ↓           ↓
Daily   LinkedIn      EOD
Briefing Post        Summary
    ↓       ↓           ↓
Qwen creates Plans/*.md files
```

---

## 📚 Documentation

### Bronze Tier Documentation

| File | Description |
|------|-------------|
| `bronze-tier/README.md` | Bronze Tier quick start and guide |
| `bronze-tier/Company_Handbook.md` | Core operating principles |
| `bronze-tier/Dashboard.md` | Status tracking template |

### Silver Tier Documentation

| File | Description |
|------|-------------|
| `silver-tier/README_Silver.md` | Silver Tier complete guide |
| `silver-tier/HITL_APPROVAL_WORKFLOW.md` | Human-in-the-loop approval workflow |
| `silver-tier/APPROVAL_QUICK_REF.md` | Quick approval reference |
| `silver-tier/EMAIL_MCP_INTEGRATION.md` | Gmail setup and integration |
| `silver-tier/TIME_TRIGGERS_SOCIAL_POST.md` | Scheduled triggers and social posts |
| `silver-tier/TIME_TRIGGERS_QUICK_REF.md` | Time triggers quick reference |
| `silver-tier/SILVER_TIER_SUMMARY.md` | Complete Silver Tier summary |
| `silver-tier/SILVER_TIER_COMPLETE.md` | Implementation checklist |

---

## 🔧 Configuration

### Gmail Setup (Silver Tier)

1. **Enable 2-Step Verification**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select: Mail → Other (Custom name: "AI Employee")
   - Copy 16-character password to `.env`

3. **Gmail API Credentials**
   - Go to https://console.cloud.google.com/
   - Create new project
   - Enable Gmail API
   - OAuth consent Screen → External
   - Add scope: `gmail.readonly`
   - Create credentials → OAuth client ID → Desktop app
   - Download `credentials.json` to `silver-tier/`

4. **First Run Authorization**
   ```bash
   python watchers/gmail_watcher.py
   # Follow browser authorization flow
   # token.json will be auto-generated
   ```

### Environment Variables

Create `silver-tier/.env` from `.env.example`:

```env
# Email MCP Configuration
GMAIL_EMAIL=your@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
DRY_RUN=true  # Set to 'false' for live email sending
```

---

## 📊 Dashboard

Both tiers include a `Dashboard.md` file that tracks:

- 📥 **Inbox Count** - Files waiting to be processed
- ⚠️ **Needs Action** - Files in processing queue
- ⏳ **Pending Approval** - Actions awaiting review (Silver)
- ✅ **Approved** - Ready for execution (Silver)
- ✅ **Done** - Completed items
- 📋 **Plans** - Active and completed action plans
- 📈 **Processing Log** - Activity history
- 📊 **Statistics** - Daily/weekly metrics

---

## 🔐 Security

### Best Practices

- ⚠️ **Never commit `.env`** - Contains sensitive credentials
- ⚠️ **Use App Password** - Not your regular Gmail password
- ⚠️ **WhatsApp ToS** - Automation may violate WhatsApp Terms of Service
- ✅ **Keep `DRY_RUN=true`** for testing email sending
- ✅ **Review all approvals** before executing sensitive actions
- ✅ **Logs stored** for audit trail in `Logs/` folder

### What's Protected

| File/Folder | Git Status | Reason |
|-------------|------------|--------|
| `.env` | Ignored | Contains passwords |
| `credentials.json` | Ignored | OAuth credentials |
| `token.json` | Ignored | Auth tokens |
| `whatsapp_session/` | Ignored | Session data |
| `Logs/` | Tracked | System logs (safe) |

---

## 🎯 Use Cases

### Bronze Tier Examples

- **Document Processing**: Drop meeting notes → AI summarizes → Archive
- **Task Management**: Drop task list → AI creates action plan → Execute
- **Content Analysis**: Drop article → AI extracts key points → Store insights
- **File Organization**: Drop files → AI categorizes → Move to appropriate folders

### Silver Tier Examples

- **Email Triage**: Important emails detected → AI drafts reply → User approves → Sent
- **Daily Briefing**: 8 AM trigger → AI generates morning summary → Review day's tasks
- **Social Media**: Monday 9 AM → AI creates LinkedIn post → User edits → Publish
- **WhatsApp Priority**: VIP message detected → AI alerts → Suggests response
- **EOD Summary**: 5 PM trigger → AI summarizes day's work → Archive for review

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Watcher not detecting files | Ensure file is created (not moved) in Inbox/ |
| Orchestrator shows 0 files | Check Needs_Action/ path, wait 30s |
| Email not sending | Check .env credentials, ensure DRY_RUN=false |
| Gmail watcher fails | Regenerate token.json, check credentials.json |
| WhatsApp session expired | Delete whatsapp_session/, re-scan QR |
| Approval not executing | Check Approved/ folder, view Logs/approval_log.txt |
| Time trigger didn't fire | Ensure orchestrator running at trigger time |

---

## 📈 Roadmap

### Future Tiers

| Tier | Planned Features |
|------|------------------|
| **Gold** | Calendar integration, payment APIs, web dashboard, analytics |
| **Platinum** | Multi-agent collaboration, advanced ML models, voice interface |

---

## 🤝 Contributing

This project is designed for incremental automation. Contributions welcome for:

- New skill definitions
- Additional monitoring integrations
- Improved approval workflows
- Dashboard enhancements
- Documentation improvements

---

## 📄 License

[Add your license here]

---

## 🙏 Acknowledgments

- Built for use with **Qwen AI**
- Inspired by autonomous agent architectures
- Designed for incremental automation and human-AI collaboration

---

*Personal AI Employee - Automating tasks with AI assistance*
*Last Updated: 2026-02-21*
