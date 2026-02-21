# Time-Based Triggers & Social Post Generation

**Tier:** Silver
**Version:** 1.0

---

## Overview

The Silver Tier orchestrator includes time-based triggers that automatically prompt Qwen to generate recurring content like daily briefings, LinkedIn posts, and end-of-day summaries.

---

## Time-Based Triggers

| Trigger | Schedule | Description | Output |
|---------|----------|-------------|--------|
| **Daily Briefing** | 8:00-8:04 AM | Morning status overview | `Plans/Daily_Briefing_YYYYMMDD.md` |
| **LinkedIn Post** | Monday 9:00-9:04 AM | Weekly LinkedIn content | `Plans/LINKEDIN_POST_YYYYMMDD.md` |
| **EOD Summary** | 5:00-5:04 PM | End-of-day recap | `Plans/EOD_Summary_YYYYMMDD.md` |

---

## How It Works

### 1. Orchestrator Checks Time

Every 30 seconds, orchestrator calls `check_time_based_triggers()`:

```python
def check_time_based_triggers() -> list:
    now = datetime.now()
    
    # Daily Briefing at 8 AM
    if current_time.hour == 8 and current_time.minute < 5:
        if LAST_DAILY_BRIEFING != today:
            triggers.append('daily_briefing')
    
    # LinkedIn Post Monday 9 AM
    if now.weekday() == 0 and current_time.hour == 9:
        triggers.append('linkedin_reminder')
    
    # EOD Summary at 5 PM
    if current_time.hour == 17 and current_time.minute < 5:
        triggers.append('end_of_day_summary')
    
    return triggers
```

### 2. Trigger Activates

When trigger matches, orchestrator prints Qwen prompt:

```
⏰ Time trigger: Daily Briefing (8 AM)

============================================================
📊 Generating Daily Briefing...
============================================================

📋 Paste the following prompt into Qwen chat:

---
📊 **Daily Briefing Request**
**Date:** 2026-02-18 08:00

Please create a daily briefing document...
```

### 3. User Pastes Prompt

User copies prompt and pastes into Qwen chat.

### 4. Qwen Generates Content

Qwen creates the requested file in `Plans/` folder.

---

## Daily Briefing (8 AM)

### Purpose
Start each day with clear overview of priorities, pending items, and suggested actions.

### Output File
`Plans/Daily_Briefing_YYYYMMDD.md`

### Content Structure

```markdown
# Daily Briefing - February 18, 2026

## 📈 Status Overview
- Items in Queue: 3
- Pending Approvals: 2
- Completed Yesterday: 5

## 🎯 Priority Items
- EMAIL_12345.md - Client inquiry (High priority)
- SendEmail_67890.md - Awaiting approval

## 📅 Scheduled/Deadlines
- Vendor payment due: Feb 20
- Team meeting: Feb 19, 2 PM

## 📝 Recent Activity Summary
- Processed 5 files yesterday
- Sent 2 client emails
- Completed vendor onboarding

## ⏳ Pending Approvals
- SendEmail_67890.md - Reply to client
- ProcessPayment_11111.md - Vendor invoice

## 💡 Suggestions
1. Approve client reply email
2. Review vendor payment
3. Process queue items before noon
```

### Qwen Prompt Template

```markdown
---
📊 **Daily Briefing Request**
**Date:** 2026-02-18 08:00

Please create a daily briefing document in `Plans/Daily_Briefing_20260218.md`

## Your Tasks

### 1. Review Dashboard
Read `Dashboard.md` to understand:
- Current queue status
- Recent processing activity
- Pending approvals

### 2. Review Recent Completed Items
Check `Done/` folder for recently processed files

### 3. Create Daily Briefing
[Use structure above]

### 4. Update Dashboard
Add briefing created to Dashboard.md processing log

---

End with: `<TASK_COMPLETE>`
```

---

## LinkedIn Post Generator (Monday 9 AM)

### Purpose
Generate professional LinkedIn content weekly for business growth and thought leadership.

### Output File
`Plans/LINKEDIN_POST_YYYYMMDD.md`

### Content Structure

```markdown
# LinkedIn Post Draft

**Created:** 2026-02-18T09:00:00
**Topic:** Business Update
**Type:** Product Announcement
**Status:** Draft - Ready for Review

---

## Post Content

🚀 Exciting news! We're thrilled to announce...

[Full post content - 1,000-1,300 characters]

---

## Hashtags

#AI #Automation #Productivity #Innovation #Business

---

## Visual Suggestions

Consider adding: Product screenshot or team photo

---

## Posting Instructions

1. Copy the post content above
2. Go to LinkedIn.com
3. Click "Start a post"
4. Paste content
5. Add image (optional)
6. Review and post

---

## Approval

- [ ] Ready to publish on LinkedIn

*Note: Manual copy-paste to LinkedIn required.*
```

### Qwen Prompt Template

```markdown
---
💼 **LinkedIn Post Generation Request**
**Date:** 2026-02-18 09:00

Please generate a professional LinkedIn post draft.

## Your Tasks

### 1. Review Context
- Read `Company_Handbook.md` for company info
- Check `Dashboard.md` for recent achievements
- Review `Done/` for completed projects

### 2. Generate LinkedIn Post
Create `Plans/LINKEDIN_POST_20260218.md` with:
- Professional, engaging content
- 1,000-1,300 characters optimal
- 3-5 relevant hashtags
- 2-3 emoji max

### 3. Post Guidelines
- Hook in first 150 characters
- Clear value proposition
- Call-to-action if applicable
- No typos or errors

---

End with: `<TASK_COMPLETE>`
```

---

## End of Day Summary (5 PM)

### Purpose
Reflect on day's accomplishments, track metrics, and identify carry-over items.

### Output File
`Plans/EOD_Summary_YYYYMMDD.md`

### Content Structure

```markdown
# End of Day Summary - February 18, 2026

## ✅ Completed Today

| Item | Type | Action Taken |
|------|------|--------------|
| EMAIL_12345.md | Email | Replied to client |
| FILE_notes.txt | File | Extracted action items |
| SendEmail_67890 | Approval | Email sent |

## 📊 Statistics
- Files Processed: 8
- Emails Sent: 3
- Approvals Executed: 2
- Plans Created: 5

## ⏳ Pending (Carried to Tomorrow)
- WHATSAPP_11111.md - Waiting for response
- ProcessPayment_22222.md - Needs review

## 📝 Notes
- High volume day - all queue items cleared
- 2 approvals pending user action
- Tomorrow: Focus on vendor payments

```

### Qwen Prompt Template

```markdown
---
🌆 **End of Day Summary Request**
**Date:** 2026-02-18 17:00

Please create an end-of-day summary document.

## Your Tasks

### 1. Review Today's Activity
- Check `Dashboard.md` processing log
- Review `Done/` folder for items completed today
- Check `Logs/approval_log.txt` for executed approvals

### 2. Create Summary
Write to `Plans/EOD_Summary_20260218.md`:
- Table of completed items
- Statistics (files, emails, approvals)
- Pending items for tomorrow
- Notes/observations

---

End with: `<TASK_COMPLETE>`
```

---

## Social Post Workflow

### For LinkedIn Posts with Approval

When post requires approval before publishing:

```
1. Orchestrator trigger (Monday 9 AM)
   → Prints Qwen prompt

2. User pastes prompt into Qwen
   → Qwen generates post

3. Qwen creates: Plans/LINKEDIN_POST_20260218.md
   → Contains full post draft

4. User reviews post
   → Edit if needed

5. User manually posts to LinkedIn
   → Copy-paste content

6. Update plan status
   → Mark "Posted" with timestamp
```

### For Posts Requiring Approval Workflow

```
1. Qwen creates: Pending_Approval/LINKEDIN_POST_20260218.md
   → Includes full post content

2. Orchestrator notifies:
   ⚠️  Approval needed: LINKEDIN_POST_20260218.md
      → To approve: Move to Approved/

3. User reviews and moves to Approved/

4. Orchestrator logs approval
   → Note: Still requires manual posting

5. User posts to LinkedIn manually
   → Copy-paste from approved file

6. File moved to Done/
```

---

## Customization

### Add New Time-Based Trigger

Edit `orchestrator.py`:

```python
def check_time_based_triggers() -> list:
    # ... existing code ...
    
    # Custom trigger example: Weekly report Friday 4 PM
    if now.weekday() == 4 and current_time.hour == 16:
        triggers.append('weekly_report')
    
    return triggers
```

Add generator function:

```python
def generate_weekly_report_prompt() -> str:
    return f"""
---
📊 **Weekly Report Request**
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

Please create a weekly report...
"""
```

Add to main loop:

```python
if 'weekly_report' in triggers:
    prompt = generate_weekly_report_prompt()
    print(prompt)
```

### Adjust Trigger Times

Edit time checks:

```python
# Change daily briefing from 8 AM to 9 AM
if current_time.hour == 9 and current_time.minute < 5:  # Was 8
```

### Change Frequency

```python
# LinkedIn post every Wednesday instead of Monday
if now.weekday() == 2 and current_time.hour == 9:  # 2 = Wednesday
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Trigger didn't fire | Check orchestrator running, time window is 5 min |
| Multiple briefings same day | LAST_DAILY_BRIEFING tracks - restart if needed |
| Prompt not generating | Check function exists in orchestrator.py |
| Qwen doesn't create file | Ensure prompt includes write_file instruction |

---

## Best Practices

1. **Keep orchestrator running** - Triggers only fire if orchestrator active
2. **Review generated content** - Always review before posting
3. **Customize prompts** - Adjust for your business context
4. **Archive briefings** - Keep in Plans/ for historical reference
5. **Track engagement** - Note which posts perform well

---

## Example: Full LinkedIn Post Workflow

### Monday 9:00 AM

```
⏰ Time trigger: LinkedIn Post Reminder (Monday 9 AM)

============================================================
💼 LinkedIn Post Reminder (Monday)
============================================================

📋 Paste the following prompt into Qwen chat:

---
💼 **LinkedIn Post Generation Request**
**Date:** 2026-02-18 09:00

Please generate a professional LinkedIn post draft...
```

### User Pastes Prompt

Qwen responds:

```markdown
# LinkedIn Post Draft

**Created:** 2026-02-18T09:00:00
**Topic:** Silver Tier Launch

## Post Content

🚀 Exciting milestone! We're thrilled to announce Silver Tier...

[Full post - 1,200 characters]

---

## Hashtags

#AI #Automation #Productivity #Innovation
```

### User Reviews & Posts

1. Read post in `Plans/LINKEDIN_POST_20260218.md`
2. (Optional) Edit for refinement
3. Copy content
4. Go to LinkedIn.com
5. Paste and post
6. Update file: Change status to "Posted"

---

*Time-Based Triggers & Social Post Generation - Silver Tier*
