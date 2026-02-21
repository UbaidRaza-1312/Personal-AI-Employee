# User Prompt: Process All Files in Needs_Action

**Version:** 2.1 (Silver Tier with HITL Approval)

Paste this into Qwen after the system prompt when orchestrator detects new files.

```markdown
---
🤖 **Process Files Request - Silver Tier**

Please process **all files currently in Needs_Action/** using the **SKILL_CreatePlan** workflow.

## Your Tasks

### 1. List Files
First, describe what files you see in Needs_Action/ to understand the current queue.
Identify file types: FILE_* (dropped), EMAIL_* (Gmail), WHATSAPP_* (WhatsApp)

### 2. Process Each File Using SKILL_CreatePlan

For each `.md` file found:

#### a. Read Metadata
```
read_file("Needs_Action/[filename].md")
```
Extract: source type, priority, from/sender, subject, status

#### b. Read Source Content (if applicable)
For FILE_* types, read the original file:
```
read_file("Needs_Action/FILE_*.original")
```

#### c. Analyze and Reason
- What type of task is this? (information/action/communication/financial)
- What is the user's intent?
- Is this sensitive? Does it need approval?
- What actions should be taken?

#### d. Create Plan with SKILL_CreatePlan
```
write_file("Plans/PLAN_[timestamp]_[name].md", """...plan content...""")
```

**Plan must include:**
- Clear objective
- Numbered steps with checkboxes `- [ ]`
- Auto-complete safe steps: `- [x]` (reading, analysis, summarization)
- Approval section for sensitive actions (sending, payments, external writes)
- Execution Log section

#### e. Create Approval File (If Needed)
If plan includes sensitive actions, use `write_file` to create approval request:

```
write_file("Pending_Approval/[ActionName]_[timestamp].md", """...approval content...""")
```

**Approval required for:**
- Sending emails/messages
- Financial transactions
- External API writes
- Data modifications/deletions
- Scheduling on user's calendar

**Approval File Format (use this template):**

```markdown
# Approval Required: [Action Name]

**Source Plan:** [PLAN_*.md link]
**Source File:** [original Needs_Action file]
**Created:** [timestamp]
**Status:** Awaiting Approval

---

## Action Details

**Action:** send_email

**What:** [Clear description of the action]

**Why:** [Reason this action is needed]

---

## Execution Details

**To:** recipient@example.com
**Subject:** Email Subject Line
**CC:** (optional)
**Attachment:** (optional path or "None")

**Body:**
> [Email body text - the actual content to send]

---

## Approval

To approve this action:
1. Review the details above
2. Move this file to `Approved/` folder
3. Orchestrator will execute automatically

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

**Important:** Include YAML-style fields at the top:
- `action:` send_email | send_message | process_payment | schedule_meeting
- `to:` email address
- `subject:` email subject
- `body:` email content
- `attachment:` path or None

#### f. Update Dashboard.md
```
read_file("Dashboard.md")  # Get current state
# Then describe the update:
# - Add to Processing Log table
# - Update Current Queue
# - Add to Pending Approvals (if applicable)
# - Adjust Status Overview counts
```

#### g. Execute Auto-Steps
Describe executing steps that don't need approval:
- Content analysis
- Information extraction
- Documentation creation
- File organization

#### h. Move Files to Done (After Completion)
```
# Describe the moves:
move_file("Needs_Action/[FILE_*.original]", "Done/[FILE_*.original]")
move_file("Needs_Action/[FILE_*.original].md", "Done/[FILE_*.original].md")
```

### 3. Update Plans to Complete
For each fully executed plan (or those awaiting approval):
- Update status to "Completed" or "Awaiting Approval"
- Add completion timestamp
- Add summary of what was accomplished

### 4. Summary
Provide a summary table:

| File | Plan Created | Auto-Steps Done | Approval Needed | Status |
|------|--------------|-----------------|-----------------|--------|
| EMAIL_123.md | ✅ | ✅ Read, Analyze | Send Reply | Awaiting |
| FILE_notes.txt | ✅ | ✅ All | None | Completed |

---

**Important:**
- You are describing file operations, not actually executing them
- I (the user) will manually perform moves and approve actions
- Be explicit about what requires approval vs. what you can auto-do
- Use SKILL_CreatePlan for ALL new items
- Iterate through multi-step plans until done or blocked

**When you have finished processing everything, end with exactly:** `<TASK_COMPLETE>`
```

---

## Test Procedure

### Prerequisites
- Both scripts installed: `pip install watchdog`
- Project folder created with all subfolders
- System prompt ready to paste into Qwen

### Step-by-Step Test

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open **Terminal 1**, navigate to project folder | `cd AI_Employee_Project` |
| 2 | Run watcher: `python filesystem_watcher.py` | "Watcher started..." message |
| 3 | Create a test file: `test.txt` with content "hello world" | File ready to drop |
| 4 | **Drop** `test.txt` into `Inbox/` folder | Watcher prints "Processed: test.txt → FILE_..." |
| 5 | Check `Needs_Action/` folder | See `FILE_YYYYMMDD_HHMMSS_test.txt` and `.md` file |
| 6 | Open **Terminal 2**, run orchestrator: `python orchestrator.py` | "Monitoring: ..." message |
| 7 | Wait up to 30 seconds | Orchestrator prints "New files detected!" + prompt |
| 8 | **Copy** the printed prompt from orchestrator | Prompt text in clipboard |
| 9 | Open Qwen chat, paste **system prompt** first, then **user prompt** | Qwen ready to process |
| 10 | Wait for Qwen's response | Qwen describes file operations step-by-step |
| 11 | **Manually perform** the file moves Qwen describes | Move files from Needs_Action/ to Done/ |
| 12 | **Manually update** Dashboard.md as Qwen describes | Processing log updated |
| 13 | Verify `Done/` folder contains processed files | Files moved successfully |
| 14 | Verify `Needs_Action/` is empty | Queue cleared |
| 15 | Press **Ctrl+C** in both terminals | Both scripts stop cleanly |

### Success Criteria

- ✅ Watcher detected file drop and created metadata
- ✅ Orchestrator detected files and printed prompt
- ✅ Qwen described complete processing workflow
- ✅ Files moved to Done/ manually
- ✅ Dashboard.md updated
- ✅ `<TASK_COMPLETE>` appeared at end of Qwen response

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Watcher doesn't detect file | Ensure file is created (not moved) in Inbox/, or use "Save As" |
| Orchestrator shows 0 files | Check Needs_Action/ path matches, wait for next poll |
| Qwen doesn't follow format | Re-paste system prompt at conversation start |
| Metadata file missing fields | Check watcher output for errors |

---

*This completes the Bronze Tier manual workflow test.*



App Password kaise lein:
     1. https://myaccount.google.com/security pe jayein
     2. 2-Step Verification enable karein
     3. https://myaccount.google.com/apppasswords pe jayein
     4. App: "Mail", Device: "Other" select karein
     5. 16-character password copy karke .env mein paste karein

    Gmail Watcher ke liye:

     1. https://console.cloud.google.com/ pe jayein
     2. Naya project banayein
     3. Gmail API enable karein
     4. OAuth consent screen setup karein
     5. Credentials download karein → credentials.json
     6. Project root mein save karein

    ---

    Step 3: Pehli Baar Setup