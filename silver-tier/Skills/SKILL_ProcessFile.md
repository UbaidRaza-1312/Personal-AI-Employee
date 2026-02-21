# Skill: Process File

**ID:** SKILL_ProcessFile  
**Tier:** Bronze  
**Status:** Active

---

## 📋 Description

This skill defines how Qwen processes a file from the Needs_Action folder. It includes reading metadata, analyzing the file, creating an action plan, updating the dashboard, and moving the file to Done.

---

## 🔄 Workflow

### Step 1: Read Metadata

Locate and read the `.md` metadata file associated with the target file in Needs_Action.

**Metadata contains:**
- `Original Filename:` The source file name
- `Date Received:` When the file was added
- `File Type:` e.g., .txt, .pdf, .md, .json
- `Initial Assessment:` Brief description of file contents
- `Priority:` Low / Medium / High

**Action:** Parse all metadata fields to understand context.

---

### Step 2: Read and Analyze the File

Open and read the actual file from Needs_Action.

**Consider:**
- What type of content is this?
- What is the user's intent?
- What actions are possible within Bronze Tier capabilities?
- Are there any blockers or limitations?

---

### Step 3: Think (Reasoning Phase)

Use Qwen's reasoning to determine:

1. **Purpose:** Why did the user provide this file?
2. **Actions:** What can be done with this file?
3. **Output:** What should the result look like?
4. **Plan:** What steps are needed to complete processing?

---

### Step 4: Create Plan

Write a new plan file to `Plans/` folder.

**Naming convention:** `PLAN_YYYYMMDD_OriginalFilename.md`

**Plan structure:**
```markdown
# Plan: [Brief Title]

**Source File:** [filename]
**Created:** [timestamp]
**Status:** In Progress

## Objective
[What we're trying to accomplish]

## Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output
[Expected result]

## Notes
[Any relevant observations]
```

---

### Step 5: Update Dashboard

Edit `Dashboard.md` to reflect the processing:

1. **Update Processing Log table:**
   - Add new row with timestamp, filename, action taken, and result

2. **Update Current Queue:**
   - Remove the processed file from the queue table

3. **Update counts** in Status Overview if applicable

---

### Step 6: Move File to Done

1. Move the original file from `Needs_Action/` to `Done/`
2. Move or archive the metadata file
3. Ensure no orphaned files remain in Needs_Action

---

### Step 7: Mark Plan Complete

Update the plan file in `Plans/`:
- Change **Status:** to `Completed`
- Add **Completed:** timestamp
- Add **Summary:** brief description of what was accomplished

---

## ✅ Success Criteria

A file is considered successfully processed when:

- [ ] Metadata was read and understood
- [ ] File content was analyzed
- [ ] A plan was created in Plans/
- [ ] Dashboard.md was updated
- [ ] File was moved to Done/
- [ ] Plan was marked as completed

---

## ⚠️ Error Handling

If processing fails at any step:

1. **Do not move the file** - leave it in Needs_Action
2. **Update metadata** with error details
3. **Add to Dashboard** notes explaining the block
4. **Wait for user intervention**

---

## 📝 Example

**Input:** `Needs_Action/notes.txt` + `Needs_Action/notes.txt.md`

**Processing:**
1. Read `notes.txt.md` → Priority: Medium, Type: Meeting notes
2. Read `notes.txt` → Contains action items from team meeting
3. Think → User wants action items extracted and organized
4. Create `Plans/PLAN_20250217_notes.md` with extraction steps
5. Update Dashboard.md log
6. Move `notes.txt` to `Done/`
7. Mark plan complete

**Output:** Organized action items, updated dashboard, clean queue

---

*This skill is the core processing engine of the Bronze Tier AI Employee.*
