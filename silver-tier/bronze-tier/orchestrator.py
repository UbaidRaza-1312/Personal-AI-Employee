"""
Orchestrator for Bronze Tier AI Employee
Checks Needs_Action/ every 30 seconds and prompts user to engage Qwen.
"""

import time
from pathlib import Path


def get_pending_files(needs_action_path: Path) -> list:
    """Get list of metadata files indicating pending work."""
    metadata_files = []
    
    if not needs_action_path.exists():
        return metadata_files
    
    for f in needs_action_path.iterdir():
        if f.is_file() and f.suffix == '.md' and not f.name.startswith('~'):
            metadata_files.append(f)
    
    return sorted(metadata_files, key=lambda x: x.stat().st_mtime)


def generate_qwen_prompt(metadata_files: list) -> str:
    """Generate the full prompt to paste into Qwen chat."""
    
    file_list = "\n".join([f"  - {f.name}" for f in metadata_files])
    
    prompt = f"""
================================================================================
QWEN PROCESSING PROMPT
================================================================================

You are the AI Employee (Bronze Tier) operating in VS Code + Qwen mode.

There are new files in Needs_Action/ requiring processing.

**Files to Process:**
{file_list}

---

## Your Task

Process each file using the SKILL_ProcessFile workflow:

### Step 1: Read Metadata
For each `.md` file listed above, read its contents to understand:
- Original filename
- Timestamp
- File size
- Type classification

### Step 2: Read Associated Files
For each metadata file, find the matching `FILE_*.original` file in Needs_Action/ and read its content if needed to understand the task.

### Step 3: Think & Analyze
For each file:
- What is the user requesting?
- What information is available?
- What is the best approach?

### Step 4: Create Plans
For each file requiring action, create a plan file in `Plans/`:
- **Naming:** `PLAN_YYYYMMDD_<BriefDescription>.md`
- **Include:** Objective, Analysis, Step-by-step approach, Expected outcome

### Step 5: Execute & Create Outputs
Carry out the work described in each plan.

### Step 6: Update Dashboard
Edit `Dashboard.md`:
- Add a row to the "Recent Activity" table with: Date, File name, Status, Notes
- Update the status counts at the top
- Update "Last Updated" timestamp to current time

### Step 7: Move to Done
Move all processed files from `Needs_Action/` to `Done/`:
- The original FILE_*.original file
- The accompanying .md metadata file

---

## Output Format

Respond with:
1. Summary of files found
2. Your analysis of each
3. Plans created (list filenames)
4. Actions taken
5. Dashboard updates made
6. Files moved to Done/
7. End with: `<TASK_COMPLETE>`

---

Begin processing now.
================================================================================
"""
    return prompt


def main():
    """Run the orchestrator loop."""
    root_path = Path('.')
    needs_action_path = root_path / 'Needs_Action'
    
    check_interval = 30  # seconds
    
    print("=" * 60)
    print("ORCHESTRATOR STARTED")
    print("=" * 60)
    print(f"Checking Needs_Action/ every {check_interval} seconds...")
    print(f"Path: {needs_action_path.absolute()}")
    print("\nWhen files are detected, you'll see a prompt to copy-paste into Qwen.")
    print("Press Ctrl+C to stop\n")
    print("-" * 60)
    
    last_check_count = 0
    
    try:
        while True:
            pending_files = get_pending_files(needs_action_path)
            current_count = len(pending_files)
            
            if current_count > 0:
                # New files detected since last check
                if current_count != last_check_count:
                    print(f"\n[!] New files detected! ({current_count} pending)")
                    print("\n" + "=" * 60)
                    print("ACTION REQUIRED")
                    print("=" * 60)
                    print("\nPaste the following prompt into Qwen chat:\n")
                    
                    prompt = generate_qwen_prompt(pending_files)
                    print(prompt)
                    
                    last_check_count = current_count
                else:
                    print(f"\n[*] {current_count} file(s) still pending in Needs_Action/")
                    print("    (Waiting for Qwen processing to complete...)")
            else:
                print(f"[*] No pending files. Next check in {check_interval}s...")
                last_check_count = 0
            
            time.sleep(check_interval)
            
    except KeyboardInterrupt:
        print("\n\nStopping orchestrator...")
    
    print("Orchestrator stopped.")


if __name__ == "__main__":
    main()
