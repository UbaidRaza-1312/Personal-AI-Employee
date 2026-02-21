# SKILL: ProcessFile

## Purpose
Process a file that has been placed in `Needs_Action/` by the watcher system. This skill defines the standard workflow for handling incoming tasks.

---

## Trigger
A file appears in `Needs_Action/` with an accompanying `.md` metadata file.

---

## Workflow

### Step 1: Read Metadata
Locate and read the metadata file associated with the input file.
- Metadata filename pattern: `<original_filename>.md`
- Extract: timestamp, source, initial classification, any notes

### Step 2: Read the Input File
Open and understand the content of the file requiring action.
- Identify the core request or task
- Note any attachments, references, or context
- Determine the expected output format

### Step 3: Think & Analyze
Pause to reason about the best approach:
- What is the user actually asking for?
- What information do I have? What's missing?
- What are possible solution approaches?
- Which approach is best given the constraints?

### Step 4: Create a Plan
Write a new plan file in `Plans/`:
- **Filename:** `PLAN_YYYYMMDD_<BriefDescription>.md`
- **Content:**
  - Objective
  - Analysis of the request
  - Step-by-step approach
  - Expected outcome
  - Any assumptions or open questions

### Step 5: Execute the Plan
Carry out the work described in your plan:
- Write code, documents, or other deliverables
- Save outputs to appropriate locations
- Test or verify your work if applicable

### Step 6: Update Dashboard
Edit `Dashboard.md` to reflect the completed work:
- Add entry to "Recent Activity" table
- Update status counts
- Update "Last Updated" timestamp

### Step 7: Move to Done
Relocate processed files:
- Move original file from `Needs_Action/` → `Done/`
- Move metadata file from `Needs_Action/` → `Done/`
- Keep them together for reference

---

## Output Checklist

- [ ] Metadata read and understood
- [ ] Input file analyzed
- [ ] Plan created in `Plans/`
- [ ] Work executed per plan
- [ ] Dashboard updated
- [ ] Files moved to `Done/`

---

## Example

**Input:** `Needs_Action/meeting_notes.txt` + `Needs_Action/meeting_notes.txt.md`

**Plan Created:** `Plans/PLAN_20250219_SummarizeMeeting.md`

**Output:** Summary document saved to `Done/`

**Dashboard:** Activity row added, counts updated

---

*Skill Version: 1.0 | Tier: Bronze*
