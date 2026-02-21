# Time Triggers & Social Posts - Quick Reference

## ⏰ Scheduled Triggers

| Time | Day | Trigger | Output |
|------|-----|---------|--------|
| 8:00 AM | Daily | Daily Briefing | `Plans/Daily_Briefing_YYYYMMDD.md` |
| 9:00 AM | Monday | LinkedIn Post | `Plans/LINKEDIN_POST_YYYYMMDD.md` |
| 5:00 PM | Daily | EOD Summary | `Plans/EOD_Summary_YYYYMMDD.md` |

---

## 📊 Daily Briefing (8 AM)

**When:** Every morning at 8:00 AM

**Orchestrator shows:**
```
⏰ Time trigger: Daily Briefing (8 AM)
📋 Paste the following prompt into Qwen chat:
```

**Qwen creates:** `Plans/Daily_Briefing_20260218.md`

**Contains:**
- Status overview (queue, approvals, completed)
- Priority items for today
- Scheduled deadlines
- Recent activity summary
- Pending approvals list
- Suggestions for the day

---

## 💼 LinkedIn Post (Monday 9 AM)

**When:** Every Monday at 9:00 AM

**Orchestrator shows:**
```
⏰ Time trigger: LinkedIn Post Reminder (Monday 9 AM)
📋 Paste the following prompt into Qwen chat:
```

**Qwen creates:** `Plans/LINKEDIN_POST_20260218.md`

**Contains:**
- Full post content (1,000-1,300 chars)
- Hashtags (3-5)
- Visual suggestions
- Posting instructions
- Approval checkbox

**To publish:**
1. Open file in Plans/
2. Copy post content
3. Go to LinkedIn.com
4. Click "Start a post"
5. Paste content
6. Add image (optional)
7. Post

---

## 🌆 End of Day Summary (5 PM)

**When:** Every day at 5:00 PM

**Orchestrator shows:**
```
⏰ Time trigger: End of Day Summary (5 PM)
📋 Paste the following prompt into Qwen chat:
```

**Qwen creates:** `Plans/EOD_Summary_20260218.md`

**Contains:**
- Table of completed items
- Statistics (files, emails, approvals)
- Pending items for tomorrow
- Notes/observations

---

## 📝 Social Post Templates

### Product Announcement

```
🚀 Exciting news! [Announcement]

We're proud to introduce [Product] - [value prop].

Solves:
- Pain point 1
- Pain point 2

Result: [Specific outcome]

[CTA]

#Industry #Innovation #Solution
```

### Thought Leadership

```
[Observation about trend]

Here's what we're seeing:

1️⃣ [Insight 1]
2️⃣ [Insight 2]
3️⃣ [Insight 3]

What this means: [Analysis]

Recommendation: [Advice]

What trends are you watching? 👇

#Leadership #Trends #Business
```

### Milestone Celebration

```
🎊 [Milestone]!

[Timeframe] ago, we set out to [goal].

Today: [Achievement]

Thanks to:
🙏 Our team
🙏 Our partners
🙏 Our customers

This is just the beginning! 🚀

#Milestone #Growth #Gratitude
```

---

## 🎯 Post Guidelines

| Platform | Length | Hashtags | Emoji | Best Time |
|----------|--------|----------|-------|-----------|
| LinkedIn | 1,000-1,300 chars | 3-5 | 2-3 | Tue-Thu 9-11 AM |
| Twitter | 250-270 chars | 2-3 | 1-2 | Daily 12-3 PM |

---

## 🔧 Customize Triggers

### Add New Trigger

Edit `orchestrator.py`:

```python
# Add to check_time_based_triggers()

# Example: Weekly report Friday 4 PM
if now.weekday() == 4 and current_time.hour == 16:
    triggers.append('weekly_report')
```

### Change Time

```python
# Change daily briefing from 8 AM to 9 AM
if current_time.hour == 9 and current_time.minute < 5:
```

### Change Day

```python
# LinkedIn post Wednesday instead of Monday
if now.weekday() == 2 and current_time.hour == 9:  # 2 = Wednesday
```

---

## 📁 File Locations

```
Plans/
├── Daily_Briefing_20260218.md
├── LINKEDIN_POST_20260218.md
├── EOD_Summary_20260218.md
└── ...

Pending_Approval/
└── LINKEDIN_POST_20260218.md  (if using approval workflow)
```

---

## ✅ Quick Checklist

### Morning (8 AM)
- [ ] Check Daily Briefing created
- [ ] Review priority items
- [ ] Note pending approvals

### Monday Morning (9 AM)
- [ ] Review LinkedIn post draft
- [ ] Edit if needed
- [ ] Post to LinkedIn
- [ ] Mark file as "Posted"

### Evening (5 PM)
- [ ] Check EOD Summary created
- [ ] Review today's accomplishments
- [ ] Note carry-over items

---

## 🚨 Troubleshooting

| Issue | Fix |
|-------|-----|
| Trigger didn't fire | Ensure orchestrator running at trigger time |
| Multiple briefings | Restart orchestrator, check LAST_DAILY_BRIEFING |
| Post too long | Ask Qwen to shorten to 1,300 characters |
| Wrong company info | Update Company_Handbook.md |

---

## 💡 Tips

1. **Keep orchestrator running** - Triggers only fire when active
2. **Review before posting** - Always check AI-generated content
3. **Save all briefings** - Historical reference in Plans/
4. **Track engagement** - Note which posts perform best
5. **Customize templates** - Adapt for your brand voice

---

*Quick Reference - Time Triggers & Social Posts*
