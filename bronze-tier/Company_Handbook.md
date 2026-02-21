# Company Handbook

## AI Employee Operating Principles

### Rule 1: Always Read Metadata First
Before processing any file in `Needs_Action/`, read the accompanying `.md` metadata file. This contains critical context about when the file arrived, its source, and any initial classification.

### Rule 2: Think Before Acting
Never rush to execute. Always:
1. Understand the request fully
2. Consider multiple approaches
3. Choose the best course of action
4. Document your reasoning in a plan

### Rule 3: One File, One Plan
Each file requiring action gets its own plan file in `Plans/`. Name it clearly: `PLAN_YYYYMMDD_Description.md`.

### Rule 4: Update the Dashboard
After completing any task:
- Move the processed file to `Done/`
- Update `Dashboard.md` with the activity
- Keep the counts accurate

### Rule 5: Ask When Uncertain
If a request is ambiguous or you lack sufficient information:
- Create a plan noting the uncertainty
- Flag it for human review
- Do not guess or make assumptions

### Rule 6: Preserve Original Files
Never delete original input files. Move them to `Done/` with their metadata intact for audit trails.

### Rule 7: Work Sequentially
Process items in `Needs_Action/` in order of arrival (oldest first), unless priority is explicitly marked.

---

## Folder Structure Reference

```
AI_Employee_Project/
├── Inbox/           → Drop zone for new files
├── Needs_Action/    → Files awaiting processing
├── Done/            → Completed work
├── Plans/           → Action plans created by Qwen
├── Skills/          → Skill definitions
├── Logs/            → System logs (optional)
├── Dashboard.md     → Status overview
└── Company_Handbook.md → This file
```

---

*Version: 1.0 | Bronze Tier*
