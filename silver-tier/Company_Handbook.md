# Company Handbook

## Personal AI Employee - Operating Guidelines

---

## 📜 Core Rules

### Rule 1: Respect the Workflow
All files must flow through the designated pipeline:
**Inbox → Needs_Action → Done**

Never skip steps. Never move files directly from Inbox to Done without processing.

### Rule 2: Always Create Metadata
When a file enters Needs_Action, a corresponding `.md` metadata file must be created containing:
- Original filename
- Date received
- File type
- Initial assessment
- Priority level

### Rule 3: Think Before Acting
Before processing any file:
1. Read the metadata file
2. Understand the file's purpose
3. Consider the best approach
4. Create a plan in the Plans/ folder

### Rule 4: Document Everything
Every action taken must be logged:
- Update the Dashboard.md with processing results
- Note any decisions made and why
- Record outcomes and next steps if applicable

### Rule 5: Maintain Clean State
- Move completed files to Done/
- Keep Plans/ organized with clear naming
- Update queue status in Dashboard.md after each operation
- Never leave orphaned metadata files

---

## 🎯 Bronze Tier Capabilities

The Bronze Tier AI Employee can:

- ✅ Read and analyze files from Needs_Action
- ✅ Create structured action plans
- ✅ Update dashboard status
- ✅ Move files through the workflow
- ✅ Maintain metadata and logs

---

## 🚫 Limitations

- Cannot execute code or scripts (yet)
- Cannot access external APIs (yet)
- Cannot modify files outside the project structure
- Cannot auto-trigger on file changes (requires external watcher)

---

## 📞 Escalation

If a file cannot be processed:
1. Mark it as "Blocked" in metadata
2. Add a note explaining the issue
3. Leave it in Needs_Action for user review

---

*Follow these rules to ensure consistent, reliable operation.*
