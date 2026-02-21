# Skill: Generate Social Post

**ID:** SKILL_GenerateSocialPost
**Tier:** Silver
**Status:** Active

---

## 📋 Description

This skill defines how Qwen generates professional social media posts (LinkedIn, Twitter, etc.) for business updates, announcements, and thought leadership content. Posts are created as drafts for user review before manual publishing.

---

## 🎯 Supported Platforms

| Platform | File Prefix | Character Limit | Hashtags |
|----------|-------------|-----------------|----------|
| LinkedIn | `LINKEDIN_POST_` | 3,000 (optimal: 1,000-1,300) | 3-5 |
| Twitter/X | `TWITTER_POST_` | 280 per tweet | 2-3 |
| General | `SOCIAL_POST_` | Varies | Varies |

---

## 🔄 Workflow

### Step 1: Receive Request

Request comes from:
- **Time-based trigger** (e.g., Monday 9 AM LinkedIn reminder)
- **User prompt** ("Generate LinkedIn post about new product")
- **Plan approval** (marketing campaign execution)

### Step 2: Gather Context

Read relevant files for content:

```
read_file("Company_Handbook.md")     # Company info, mission, values
read_file("Dashboard.md")            # Recent achievements, metrics
read_file("Done/")                   # Completed projects (optional)
```

**Extract:**
- Company name and description
- Recent milestones or achievements
- Product/service updates
- Industry positioning

### Step 3: Determine Post Type

| Type | Purpose | Tone | Example |
|------|---------|------|---------|
| **Announcement** | New product, hire, milestone | Professional, excited | "We're thrilled to announce..." |
| **Thought Leadership** | Industry insights, trends | Authoritative, helpful | "Here's what we're seeing in..." |
| **Company Culture** | Team events, values | Warm, authentic | "Our team believes..." |
| **Educational** | Tips, how-tos, best practices | Helpful, expert | "5 ways to improve..." |
| **Celebration** | Achievements, milestones | Grateful, proud | "We just hit..." |

### Step 4: Generate Post Content

**Write to:** `Plans/[PREFIX]_[timestamp].md`

**Structure:**

```markdown
# [Platform] Post Draft

**Created:** [timestamp]
**Topic:** [Brief description]
**Type:** [Announcement/Thought Leadership/etc.]
**Status:** Draft - Ready for Review

---

## Post Content

[Write the actual post here]

---

## Hashtags

#[Hashtag1] #[Hashtag2] #[Hashtag3]

---

## Visual Suggestions (Optional)

[Describe image/graphic that would complement the post]

---

## Posting Instructions

1. Copy the post content above
2. Go to [Platform URL]
3. [Platform-specific steps]
4. Paste content
5. Add image (if applicable)
6. Review and post

---

## Approval

To approve and post:
- [ ] Ready to publish

*Note: This is a draft. Manual copy-paste required.*
```

---

## 📝 Platform Guidelines

### LinkedIn

**Optimal Format:**
- Length: 1,000-1,300 characters
- Paragraphs: 2-4 short paragraphs
- Opening: Hook in first 150 characters (before "see more")
- Hashtags: 3-5 relevant tags
- Emoji: 2-3 max, professional context

**Example:**

```
🚀 Exciting news! We're thrilled to announce the launch of our new 
AI-powered employee management system.

After months of development, we've created a solution that helps 
businesses automate file processing, email management, and approval 
workflows - all while maintaining human oversight.

Key features:
✅ Intelligent file monitoring
✅ Gmail and WhatsApp integration  
✅ Human-in-the-loop approval system
✅ Comprehensive audit logging

We're already seeing amazing results with our early adopters. 
Ready to transform your workflow? Let's connect!

#AI #Automation #BusinessEfficiency #Innovation #TechStartup
```

### Twitter/X

**Optimal Format:**
- Length: 250-270 characters (leave room for engagement)
- Hashtags: 2-3 max
- Thread: For longer content (number tweets 1/X)

**Example:**

```
🧵 1/3 Big news! We just launched our AI Employee system that 
automates your workflow while keeping you in control. Here's how 
it works 👇

2/3 Drop files → Auto-processed → Smart approvals → Done
No more manual sorting. No more missed emails. Just results.

3/3 Want to see it in action? Drop us a message! 

#AI #Productivity
```

---

## ✅ Quality Checklist

Before finalizing post:

- [ ] Clear, compelling opening hook
- [ ] Value proposition clear
- [ ] Appropriate tone for platform
- [ ] Character count within optimal range
- [ ] Hashtags relevant (not spammy)
- [ ] Call-to-action included (if applicable)
- [ ] No typos or grammatical errors
- [ ] Company info accurate

---

## 🚫 Content Restrictions

**Do NOT generate:**
- False or misleading claims
- Confidential information
- Controversial political/religious content
- Competitor comparisons (unless factual, professional)
- Financial advice or guarantees
- Medical/legal advice (unless qualified)

---

## 📊 Post Templates

### Template 1: Product Announcement

```markdown
# LinkedIn Post Draft

**Topic:** Product Launch

## Post Content

🎉 [Exciting news opening]!

We're proud to introduce [Product Name] - [one-line value prop].

[Problem it solves]:
- Pain point 1
- Pain point 2
- Pain point 3

[Key benefit/outcome]: [Specific result]

[Call-to-action]: [What should readers do?]

## Hashtags

#[Industry] #[Solution] #[Benefit] #[Innovation]
```

### Template 2: Thought Leadership

```markdown
# LinkedIn Post Draft

**Topic:** Industry Insight

## Post Content

[Observation about industry trend]

Here's what we're seeing in [industry] right now:

1️⃣ [Trend/insight #1]
2️⃣ [Trend/insight #2]
3️⃣ [Trend/insight #3]

[Analysis/implication]: What this means for businesses...

[Recommendation]: How to adapt/thrive...

What trends are you watching? Share below! 👇

## Hashtags

#[Industry] #[Leadership] #[Trends] #[Business]
```

### Template 3: Company Milestone

```markdown
# LinkedIn Post Draft

**Topic:** Milestone Celebration

## Post Content

🎊 [Milestone announcement]!

[Timeframe] ago, we set out to [mission/goal].

Today, we're [achievement] - and we couldn't have done it without:

🙏 Our amazing team
🙏 Our supportive partners
🙏 Our incredible customers

This is just the beginning. Here's to [future goal]! 🚀

## Hashtags

#[Milestone] #[Growth] #[Gratitude] #[Team]
```

---

## 🔄 Approval Workflow

For posts requiring approval before publishing:

1. **Qwen creates:** `Plans/LINKEDIN_POST_YYYYMMDD.md`
2. **User reviews:** Read post content
3. **To approve:** Move to `Approved/` folder
4. **Orchestrator logs:** Approval recorded (manual posting still required)
5. **User posts:** Manually copy-paste to LinkedIn
6. **Mark complete:** Update plan status

**Note:** Unlike emails, social posts cannot be auto-published without API 
integration. Approval workflow is for tracking/record-keeping only.

---

## 📈 Performance Tips

**Best Practices:**

| Factor | Recommendation |
|--------|----------------|
| **Timing** | Tue-Thu 9-11 AM for LinkedIn |
| **Frequency** | 2-3x/week for LinkedIn |
| **Engagement** | Respond to comments within 24hrs |
| **Visuals** | Posts with images get 2x engagement |
| **Length** | 1,000-1,300 chars optimal for LinkedIn |
| **Hashtags** | 3-5 relevant tags, not generic |

---

## 📝 Example Output

**Input:** "Generate LinkedIn post about our new AI Employee Silver Tier"

**Output:** `Plans/LINKEDIN_POST_20260218.md`

```markdown
# LinkedIn Post Draft

**Created:** 2026-02-18T09:00:00
**Topic:** Silver Tier Launch
**Type:** Product Announcement
**Status:** Draft - Ready for Review

---

## Post Content

🚀 Exciting milestone! We're thrilled to announce Silver Tier of our 
Personal AI Employee system.

Building on our Bronze Tier foundation, Silver adds:

✅ Gmail API integration - Auto-process important emails
✅ WhatsApp monitoring - Never miss urgent messages
✅ Human-in-the-loop approvals - AI suggests, you decide
✅ Email sending via SMTP - Approved emails sent automatically
✅ Time-based triggers - Daily briefings at 8 AM

The result? A smarter, more connected AI employee that handles your 
inbox while keeping you in control.

Early users are saving 10+ hours/week on email and file management. 
Ready to see what AI can do for your workflow?

Let's connect! 👋

---

## Hashtags

#AI #Automation #Productivity #BusinessEfficiency #Innovation

---

## Posting Instructions

1. Copy post content above
2. Go to LinkedIn.com
3. Click "Start a post"
4. Paste content
5. Add product screenshot (optional)
6. Review and post

---

*Generated by SKILL_GenerateSocialPost - Silver Tier*
```

---

## 🔗 Integration Points

**Triggers:**
- Orchestrator time-based (Monday 9 AM LinkedIn reminder)
- User prompt via orchestrator
- Plan execution (marketing campaign)

**Outputs:**
- `Plans/LINKEDIN_POST_*.md` - LinkedIn drafts
- `Plans/TWITTER_POST_*.md` - Twitter drafts
- `Plans/SOCIAL_POST_*.md` - Generic drafts

**Related Skills:**
- SKILL_CreatePlan - For marketing campaign planning
- SKILL_ProcessFile - For processing social media requests

---

*This skill enables the Silver Tier AI Employee to generate professional, 
on-brand social media content for business growth and engagement.*
