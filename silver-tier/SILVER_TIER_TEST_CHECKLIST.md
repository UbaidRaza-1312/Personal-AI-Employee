# Silver Tier Final Test Checklist

**Version:** 1.0
**Date:** 2026-02-18

Use this checklist to verify all Silver Tier features are working correctly.

---

## Pre-Test Setup

### 1. Dependencies Installed

- [ ] `pip install watchdog`
- [ ] `pip install google-api-python-client google-auth-oauthlib google-auth-httplib2`
- [ ] `pip install playwright`
- [ ] `playwright install chromium`
- [ ] `pip install python-dotenv`

### 2. Credentials Configured

- [ ] `.env` file created from `.env.example`
- [ ] `GMAIL_EMAIL` set in `.env`
- [ ] `GMAIL_APP_PASSWORD` set (16-char app password, not regular password)
- [ ] `DRY_RUN=true` for testing

### 3. Google Cloud Setup (Gmail Watcher)

- [ ] Google Cloud project created
- [ ] Gmail API enabled
- [ ] OAuth consent screen configured
- [ ] `credentials.json` downloaded to project root
- [ ] First run completed, `token.json` generated

### 4. WhatsApp Setup (Optional)

- [ ] First run completed (non-headless)
- [ ] QR code scanned
- [ ] `whatsapp_session/` folder created

### 5. Folder Structure

- [ ] All folders exist:
  - Inbox/
  - Needs_Action/
  - Pending_Approval/
  - Approved/
  - Rejected/
  - Done/
  - Plans/
  - Logs/

---

## Test Sequence

### Test 1: File Watcher (Bronze Tier Baseline)

**Goal:** Verify Bronze Tier still works

**Steps:**
1. Start Terminal 1: `python watchers/filesystem_watcher.py`
2. Create test file: `test.txt` with content "Hello World"
3. Drop file into `Inbox/`

**Expected Results:**
- [ ] Watcher prints: "Processed: test.txt → FILE_..."
- [ ] File copied to `Needs_Action/FILE_*_test.txt`
- [ ] Metadata created: `Needs_Action/FILE_*_test.txt.md`
- [ ] Both files visible in folder

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

### Test 2: Orchestrator Detection

**Goal:** Verify orchestrator detects new files

**Steps:**
1. Start Terminal 2: `python src/orchestrator.py`
2. Wait for next poll (30 seconds)
3. Check output

**Expected Results:**
- [ ] Orchestrator starts successfully
- [ ] Shows folder paths
- [ ] Detects files in Needs_Action/
- [ ] Prints Qwen processing prompt

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

### Test 3: Qwen Processing

**Goal:** Verify Qwen processes files correctly

**Steps:**
1. Copy prompt from orchestrator output
2. Paste SYSTEM_PROMPT_Silver.md into Qwen
3. Paste processing prompt
4. Wait for Qwen response

**Expected Results:**
- [ ] Qwen lists files in Needs_Action/
- [ ] Qwen reads metadata
- [ ] Qwen creates plan in Plans/
- [ ] Qwen describes Dashboard updates
- [ ] Qwen describes file moves to Done/
- [ ] Response ends with `<TASK_COMPLETE>`

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

### Test 4: Manual File Moves

**Goal:** Verify manual execution of Qwen's instructions

**Steps:**
1. Follow Qwen's file move instructions
2. Move files from Needs_Action/ to Done/
3. Update Dashboard.md as described
4. Update plan status to "Completed"

**Expected Results:**
- [ ] Files moved successfully
- [ ] Dashboard.md updated
- [ ] Plan marked completed
- [ ] Needs_Action/ queue cleared

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

### Test 5: Gmail Watcher

**Goal:** Verify Gmail monitoring works

**Steps:**
1. Start Terminal 3: `python watchers/gmail_watcher.py`
2. Send yourself an email from another account
3. Subject: "URGENT: Silver Tier Test"
4. Mark as Important (star it)
5. Leave unread
6. Wait up to 120 seconds

**Expected Results:**
- [ ] gmail_watcher.py starts successfully
- [ ] Connects to Gmail API
- [ ] Detects new email within 120s
- [ ] Creates `Needs_Action/EMAIL_*.md`
- [ ] YAML frontmatter includes from, subject, priority: high
- [ ] Email content included
- [ ] Suggested actions with checkboxes

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

### Test 6: Email Processing

**Goal:** Verify Qwen processes EMAIL_* files

**Steps:**
1. Copy orchestrator prompt for EMAIL_* file
2. Paste into Qwen (after system prompt)
3. Wait for response

**Expected Results:**
- [ ] Qwen reads email metadata
- [ ] Qwen analyzes email content
- [ ] Qwen creates plan in Plans/
- [ ] If reply needed: Creates Pending_Approval/
- [ ] Updates Dashboard.md

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

### Test 7: Approval Workflow

**Goal:** Verify HITL approval workflow

**Steps:**
1. Qwen creates `Pending_Approval/SendEmail_*.md`
2. Orchestrator notifies (within 30s):
   ```
   ⚠️  Approval needed: SendEmail_*.md
   ```
3. Open approval file, review content
4. Move file to `Approved/` folder
5. Wait for orchestrator to detect

**Expected Results:**
- [ ] Orchestrator notifies user
- [ ] Shows action type, to, subject
- [ ] After moving to Approved/:
  - Orchestrator detects within 30s
  - Prints "✅ Approved actions ready"
  - Executes email (if email_mcp available)
  - Moves file to Done/
  - Logs to Logs/approval_log.txt

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

### Test 8: Email MCP Execution

**Goal:** Verify email sending works

**Prerequisites:**
- [ ] `.env` configured with valid credentials
- [ ] `DRY_RUN=false` (for live test)

**Steps:**
1. Approve an email (move to Approved/)
2. Wait for orchestrator to execute
3. Check recipient inbox
4. Check Logs/email_log.txt

**Expected Results:**
- [ ] Orchestrator prints: "📧 Sending email to: ..."
- [ ] Email sent successfully
- [ ] Recipient receives email
- [ ] Log entry created
- [ ] File moved to Done/

**If DRY_RUN=true:**
- [ ] Email NOT sent (expected)
- [ ] Log shows "DRY RUN"
- [ ] No error

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

### Test 9: Time-Based Triggers

**Goal:** Verify scheduled triggers work

**Option A: Daily Briefing (8 AM)**

**Steps:**
1. Start orchestrator before 8:00 AM
2. Wait for 8:00 AM
3. Check output

**Expected Results:**
- [ ] At 8:00-8:04 AM: Trigger fires
- [ ] Prints: "⏰ Time trigger: Daily Briefing (8 AM)"
- [ ] Generates Qwen prompt for briefing
- [ ] User can paste into Qwen
- [ ] Qwen creates `Plans/Daily_Briefing_YYYYMMDD.md`

**Status:** ⬜ Pass ⬜ Fail

**Option B: Manual Test (Immediate)**

**Steps:**
1. Edit orchestrator.py temporarily:
   ```python
   # Change line to always trigger
   if True:  # Was: if current_time.hour == 8
       triggers.append('daily_briefing')
   ```
2. Restart orchestrator
3. Check output

**Expected Results:**
- [ ] Trigger fires immediately
- [ ] Prompt generated
- [ ] Same as 8 AM test

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

### Test 10: LinkedIn Post Generation

**Goal:** Verify social post generation

**Option A: Monday 9 AM**
- Wait for Monday 9:00 AM
- Check orchestrator output

**Option B: Manual Prompt**

**Steps:**
1. Use prompt from `QWEN_SILVER_PROCESSING_PROMPT.md`
2. Section: "LinkedIn Post Generation Request"
3. Paste into Qwen

**Expected Results:**
- [ ] Qwen reads Company_Handbook.md
- [ ] Creates `Plans/LINKEDIN_POST_YYYYMMDD.md`
- [ ] Post content 1,000-1,300 characters
- [ ] 3-5 hashtags included
- [ ] Posting instructions included
- [ ] Approval checkbox included

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

### Test 11: Dashboard Updates

**Goal:** Verify Dashboard.md has Silver Tier sections

**Steps:**
1. Open Dashboard.md
2. Review all sections

**Expected Sections:**
- [ ] Status Overview (with Pending Approval count)
- [ ] Current Queue
- [ ] Pending Approvals table
- [ ] Processing Log
- [ ] Recent Emails Processed table
- [ ] Recent WhatsApp Messages table
- [ ] Today's Statistics
- [ ] Time-Based Triggers table
- [ ] Updated folder structure

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

### Test 12: WhatsApp Watcher (Optional)

**Goal:** Verify WhatsApp monitoring (if configured)

**Steps:**
1. Start Terminal 4: `python whatsapp_watcher.py`
2. Send WhatsApp message with keyword "urgent" or "test"
3. Wait up to 60 seconds

**Expected Results:**
- [ ] whatsapp_watcher.py starts
- [ ] Browser launches (headless if configured)
- [ ] Session loads from whatsapp_session/
- [ ] Detects message with priority keyword
- [ ] Creates `Needs_Action/WHATSAPP_*.md`
- [ ] Includes chat name, preview, priority

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

⚠️ **Warning:** WhatsApp automation may violate ToS. Use at own risk.

---

### Test 13: Multiple Watchers Concurrent

**Goal:** Verify all watchers can run simultaneously

**Steps:**
1. Start all watchers in separate terminals:
   - Terminal 1: `python orchestrator.py`
   - Terminal 2: `python filesystem_watcher.py`
   - Terminal 3: `python gmail_watcher.py`
   - Terminal 4: `python whatsapp_watcher.py` (optional)
2. Drop file into Inbox/
3. Send Gmail test email
4. Send WhatsApp message (optional)
5. Monitor all terminals

**Expected Results:**
- [ ] All processes run without conflicts
- [ ] File watcher detects file drop
- [ ] Gmail watcher detects email
- [ ] WhatsApp watcher detects message
- [ ] Orchestrator detects all new items
- [ ] No port conflicts or errors
- [ ] CPU/memory usage reasonable

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

### Test 14: End-to-End Flow

**Goal:** Complete Silver Tier workflow from start to finish

**Steps:**
1. Start all services
2. Drop file: `meeting_notes.txt`
3. Send email: "Meeting Follow-up"
4. Qwen processes both
5. Qwen creates approval for reply email
6. User approves (move to Approved/)
7. Email sent automatically
8. Daily briefing triggered (or manual)
9. LinkedIn post generated (or manual)
10. All files moved to Done/
11. Dashboard fully updated

**Expected Results:**
- [ ] File processed correctly
- [ ] Email processed correctly
- [ ] Approval workflow functional
- [ ] Email sent successfully
- [ ] Time triggers working
- [ ] Social post generated
- [ ] Dashboard reflects all activity
- [ ] Logs show all actions

**Status:** ⬜ Pass ⬜ Fail

**Notes:** _________________________________________

---

## Post-Test Verification

### Logs Review

**Check:** `Logs/email_log.txt`
- [ ] Entries for sent emails
- [ ] Success/failure status
- [ ] Message IDs recorded

**Check:** `Logs/approval_log.txt`
- [ ] Entries for executed approvals
- [ ] Entries for rejected items
- [ ] Timestamps accurate

### Folder Cleanup

**Check:**
- [ ] Needs_Action/ queue empty (or as expected)
- [ ] Done/ contains processed files
- [ ] Plans/ contains created plans
- [ ] Pending_Approval/ empty (or awaiting review)
- [ ] Approved/ empty (executed items moved)

### Documentation

**Verify:**
- [ ] README_Silver.md accurate
- [ ] All skill files present in Skills/
- [ ] Dashboard.md updated
- [ ] This checklist completed

---

## Final Sign-Off

### Silver Tier Features Verified

| Feature | Tested | Status |
|---------|--------|--------|
| File Monitoring (Bronze) | ⬜ | ⬜ Pass ⬜ Fail |
| Gmail Monitoring | ⬜ | ⬜ Pass ⬜ Fail |
| WhatsApp Monitoring | ⬜ | ⬜ Pass ⬜ Fail |
| Email Sending (MCP) | ⬜ | ⬜ Pass ⬜ Fail |
| HITL Approval Workflow | ⬜ | ⬜ Pass ⬜ Fail |
| Daily Briefing (8 AM) | ⬜ | ⬜ Pass ⬜ Fail |
| LinkedIn Post (Mon 9 AM) | ⬜ | ⬜ Pass ⬜ Fail |
| EOD Summary (5 PM) | ⬜ | ⬜ Pass ⬜ Fail |
| Dashboard Updates | ⬜ | ⬜ Pass ⬜ Fail |
| Documentation Complete | ⬜ | ⬜ Pass ⬜ Fail |

### Overall Status

**Silver Tier Status:** ⬜ Complete ⬜ Partial ⬜ Incomplete

**Tested By:** _________________________

**Date:** _________________________

**Issues Found:**
```
[List any issues or blockers]
```

**Next Steps:**
```
[List any follow-up tasks]
```

---

## Troubleshooting Reference

| Issue | Solution |
|-------|----------|
| Watcher not detecting | Ensure file created (not moved) in Inbox/ |
| Orchestrator shows 0 files | Wait 30s, check Needs_Action/ path |
| Email not sending | Check .env, verify app password, DRY_RUN=false |
| Gmail watcher fails | Regenerate token.json, check credentials.json |
| Approval not executing | Check Approved/ folder, view approval_log.txt |
| Time trigger didn't fire | Ensure orchestrator running at trigger time |
| WhatsApp session expired | Delete whatsapp_session/, re-scan QR |

---

*Silver Tier Final Test Checklist*
*Personal AI Employee Project*
