"""
Orchestrator for Personal AI Employee - Silver Tier

Polls Needs_Action/ folder every 30 seconds.
When files are detected, prompts user to process them with Qwen.
Handles Human-in-the-Loop (HITL) approval workflow.
"""

import time
import shutil
from pathlib import Path
from datetime import datetime

try:
    from email_mcp import send_email
    EMAIL_MCP_AVAILABLE = True
except ImportError:
    EMAIL_MCP_AVAILABLE = False
    print("⚠️  email_mcp not available. Install: pip install python-dotenv")


# Folder paths
FOLDER_PENDING = Path('Pending_Approval')
FOLDER_APPROVED = Path('Approved')
FOLDER_REJECTED = Path('Rejected')
FOLDER_DONE = Path('Done')
FOLDER_NEEDS_ACTION = Path('Needs_Action')
FOLDER_LOGS = Path('Logs')
FOLDER_PLANS = Path('Plans')

# Ensure all folders exist
for folder in [FOLDER_PENDING, FOLDER_APPROVED, FOLDER_REJECTED, FOLDER_DONE,
               FOLDER_NEEDS_ACTION, FOLDER_LOGS, FOLDER_PLANS]:
    folder.mkdir(exist_ok=True)

# Approval log file
APPROVAL_LOG = FOLDER_LOGS / 'approval_log.txt'

# Time-based triggers
LAST_DAILY_BRIEFING = None  # Track to avoid duplicate briefings


def log_approval_action(message: str):
    """Log approval workflow actions to file."""
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {message}\n"
    APPROVAL_LOG.write_text(log_entry, encoding='utf-8')
    print(f"   📝 Logged: {message}")


def check_time_based_triggers() -> list:
    """
    Check for time-based triggers (daily briefing, etc.).
    
    Returns list of triggers to execute.
    """
    global LAST_DAILY_BRIEFING
    
    triggers = []
    now = datetime.now()
    current_time = now.time()
    today = now.date()
    
    # Daily Briefing at 8:00 AM
    if current_time.hour == 8 and current_time.minute < 5:  # 8:00-8:04 AM window
        if LAST_DAILY_BRIEFING != today:
            triggers.append('daily_briefing')
            LAST_DAILY_BRIEFING = today
            print(f"\n⏰ Time trigger: Daily Briefing (8 AM)")

    # End of Day Summary at 5:00 PM
    if current_time.hour == 17 and current_time.minute < 5:  # 5:00-5:04 PM
        triggers.append('end_of_day_summary')
        print(f"\n⏰ Time trigger: End of Day Summary (5 PM)")
    
    return triggers


def generate_daily_briefing_prompt() -> str:
    """Generate prompt for Qwen to create daily briefing."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    return f"""
---
📊 **Daily Briefing Request**
**Date:** {timestamp}

Please create a daily briefing document in `Plans/Daily_Briefing_{datetime.now().strftime("%Y%m%d")}.md`

## Your Tasks

### 1. Review Dashboard
Read `Dashboard.md` to understand:
- Current queue status
- Recent processing activity
- Pending approvals

### 2. Review Recent Completed Items
Check `Done/` folder for recently processed files (last 24 hours if timestamps available)

### 3. Create Daily Briefing
Write to `Plans/Daily_Briefing_{datetime.now().strftime("%Y%m%d")}.md` with:

```markdown
# Daily Briefing - {datetime.now().strftime("%B %d, %Y")}

## 📈 Status Overview
- Items in Queue: X
- Pending Approvals: Y
- Completed Yesterday: Z

## 🎯 Priority Items
[List high-priority items needing attention]

## 📅 Scheduled/Deadlines
[Any time-sensitive items]

## 📝 Recent Activity Summary
[Brief summary of what was processed]

## ⏳ Pending Approvals
[List items awaiting user approval]

## 💡 Suggestions
[Any recommended actions for the day]
```

### 4. Update Dashboard
Add briefing created to Dashboard.md processing log

---

End with: `<TASK_COMPLETE>`
"""


def generate_end_of_day_summary_prompt() -> str:
    """Generate prompt for Qwen to create end-of-day summary."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    return f"""
---
🌆 **End of Day Summary Request**
**Date:** {timestamp}

Please create an end-of-day summary document.

## Your Tasks

### 1. Review Today's Activity
- Check `Dashboard.md` processing log
- Review `Done/` folder for items completed today
- Check `Logs/approval_log.txt` for executed approvals

### 2. Create Summary
Write to `Plans/EOD_Summary_{datetime.now().strftime("%Y%m%d")}.md`:

```markdown
# End of Day Summary - {datetime.now().strftime("%B %d, %Y")}

## ✅ Completed Today

| Item | Type | Action Taken |
|------|------|--------------|
| ... | ... | ... |

## 📊 Statistics
- Files Processed: X
- Emails Sent: Y
- Approvals Executed: Z

## ⏳ Pending (Carried to Tomorrow)
[List any items not completed]

## 📝 Notes
[Any observations or follow-ups needed]
```

---

End with: `<TASK_COMPLETE>`
"""


def get_needs_action_files(needs_action_path: Path) -> list:
    """Get list of files in Needs_Action that need processing."""
    files = []
    metadata_files = []

    for item in needs_action_path.iterdir():
        if item.is_file():
            if item.suffix == '.md':
                metadata_files.append(item.name)
            else:
                files.append(item.name)

    # Return metadata_files as primary files if no attachment files exist
    # This handles email-only cases (no attachments)
    if not files and metadata_files:
        files = metadata_files
        metadata_files = []

    return files, metadata_files


def get_pending_approval_files(pending_path: Path) -> list:
    """Get list of NEW pending approval files (not yet notified)."""
    if not pending_path.exists():
        return []

    pending = []
    for item in pending_path.iterdir():
        if item.is_file() and item.suffix == '.md':
            # Check if this is a new file (not yet processed)
            content = item.read_text(encoding='utf-8')
            if 'NOTIFIED:' not in content:
                pending.append(item.name)
    return pending


def get_approved_files(approved_path: Path) -> list:
    """Get list of files in Approved/ folder ready for execution."""
    if not approved_path.exists():
        return []

    approved = []
    for item in approved_path.iterdir():
        if item.is_file() and item.suffix == '.md':
            approved.append(item.name)
    return approved


def parse_approval_file(approval_file: Path) -> dict:
    """
    Parse approval file to extract action details.

    Returns dict with:
    - action: send_email, send_message, process_payment, etc.
    - to, subject, body, attachment (for email)
    - metadata from YAML frontmatter
    """
    content = approval_file.read_text(encoding='utf-8')

    result = {
        'action': None,
        'to': None,
        'subject': None,
        'body': None,
        'attachment': None,
        'cc': None,
        'source_plan': None,
        'raw_content': content
    }
    
    lines = content.split('\n')
    in_body = False
    body_lines = []
    in_details = False
    
    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()
        
        # Extract action type from title or action field
        if line_lower.startswith('# approval required:') or line_lower.startswith('## action:'):
            if 'email' in line_lower:
                result['action'] = 'send_email'
            elif 'whatsapp' in line_lower or 'message' in line_lower:
                result['action'] = 'send_message'
            elif 'payment' in line_lower:
                result['action'] = 'process_payment'
            elif 'schedule' in line_lower or 'meeting' in line_lower:
                result['action'] = 'schedule_meeting'

        # Extract from YAML frontmatter
        if line_lower.startswith('action:'):
            result['action'] = line.split(':', 1)[1].strip()
        elif line_lower.startswith('to:'):
            result['to'] = line.split(':', 1)[1].strip().strip('"').strip()
        elif line_lower.startswith('subject:'):
            result['subject'] = line.split(':', 1)[1].strip().strip('"').strip()
        elif line_lower.startswith('attachment:'):
            attachment_val = line.split(':', 1)[1].strip()
            if attachment_val and attachment_val.lower() != 'none':
                result['attachment'] = attachment_val.strip('"').strip()
        elif line_lower.startswith('cc:'):
            result['cc'] = line.split(':', 1)[1].strip().strip('"').strip()
        elif line_lower.startswith('source plan:'):
            result['source_plan'] = line.split(':', 1)[1].strip().strip('"').strip()

        # Extract from structured content (markdown format)
        if line_lower.startswith('- **to:**') or (line_lower.startswith('- to:') and 'to:' in line_lower):
            result['to'] = line.split(':', 1)[1].strip().strip('"').strip()
        elif line_lower.startswith('- **subject:**') or (line_lower.startswith('- subject:') and 'subject:' in line_lower):
            result['subject'] = line.split(':', 1)[1].strip().strip('"').strip()
        elif line_lower.startswith('- **attachment:**') or (line_lower.startswith('- attachment:')):
            attachment_val = line.split(':', 1)[1].strip()
            if attachment_val and attachment_val.lower() != 'none':
                result['attachment'] = attachment_val.strip('"').strip()
        elif line_lower.startswith('- **body:**') or line_lower.startswith('- body:'):
            in_body = True
            body_start = line.split(':', 1)[1].strip()
            if body_start and body_start != '':
                body_lines.append(body_start.strip('"').strip('> ').strip())
        elif in_body:
            if line_stripped.startswith('## ') or line_stripped.startswith('---') or line_stripped.startswith('- [ ]'):
                in_body = False
            elif line_stripped:
                body_lines.append(line.strip('> ').rstrip())
    
    result['body'] = '\n'.join(body_lines) if body_lines else None
    
    return result


def execute_approved_action(approval_file: Path) -> dict:
    """
    Execute the action from an approved file.
    
    Returns:
        dict: {
            'success': bool,
            'message': str,
            'action': str,
            'details': dict
        }
    """
    parsed = parse_approval_file(approval_file)
    
    result = {
        'success': False,
        'message': '',
        'action': parsed['action'],
        'details': parsed
    }
    
    if not parsed['action']:
        result['message'] = "Could not determine action type from approval file"
        return result
    
    print(f"\n📋 Action Type: {parsed['action']}")
    
    # Execute based on action type
    if parsed['action'] == 'send_email':
        if not EMAIL_MCP_AVAILABLE:
            result['message'] = "Email MCP not available"
            return result
        
        if not parsed['to']:
            result['message'] = "Recipient email address not found"
            return result
        
        if not parsed['body']:
            result['message'] = "Email body not found"
            return result
        
        print(f"   To: {parsed['to']}")
        print(f"   Subject: {parsed['subject']}")
        if parsed['attachment']:
            print(f"   Attachment: {parsed['attachment']}")
        
        # Send email
        email_result = send_email(
            to=parsed['to'],
            subject=parsed['subject'] or "[No Subject]",
            body=parsed['body'],
            attachment_path=parsed['attachment'],
            cc=parsed['cc']
        )
        
        result['success'] = email_result['success']
        result['message'] = email_result['message']
        result['message_id'] = email_result.get('message_id')
        
    elif parsed['action'] == 'send_message':
        # WhatsApp messaging not implemented (requires WhatsApp Business API)
        result['message'] = "WhatsApp messaging requires WhatsApp Business API - manual action needed"
        result['success'] = False
        
    elif parsed['action'] == 'process_payment':
        # Payment processing not implemented (requires banking integration)
        result['message'] = "Payment processing requires banking integration - manual action needed"
        result['success'] = False
        
    elif parsed['action'] == 'schedule_meeting':
        # Calendar integration not implemented
        result['message'] = "Calendar scheduling requires integration - manual action needed"
        result['success'] = False

    else:
        result['message'] = f"Unknown action type: {parsed['action']}"
    
    return result


def generate_qwen_prompt(files: list, metadata_files: list) -> str:
    """Generate the prompt to paste into Qwen chat."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Detect if these are email files (EMAIL_*.md)
    is_email_mode = any(f.startswith('EMAIL_') and f.endswith('.md') for f in files)

    prompt = f"""
---
🤖 **Qwen AI Employee - Process Files Request**
**Timestamp:** {timestamp}
**Files in Needs_Action:** {len(files)}

## Files to Process

"""

    for i, f in enumerate(files, 1):
        matching_meta = [m for m in metadata_files if f in m]
        meta_status = "✓" if matching_meta else "✗"
        prompt += f"{i}. {meta_status} `{f}`\n"

    if is_email_mode:
        prompt += """
---

## Instructions (Email Processing Mode)

Please process all email files listed above from the Needs_Action/ folder:

1. **Read each EMAIL_*.md file** - Understand the email content and context
2. **Identify the action needed** for each email:
   - Reply required? → Draft response email
   - Task/Request? → Create action plan in Plans/
   - Information only? → Summarize and file
   - Approval needed? → Create approval request in Pending_Approval/
3. **Create Plan_*.md in Plans/** for emails requiring action
4. **For emails needing reply**: Create draft in Pending_Approval/ with:
   - YAML frontmatter (action: send_email, to:, subject:, body:)
   - Professional response draft
5. **Update Dashboard.md** - Append processing activity to the log
6. **Move processed files to Done/** - Clean up Needs_Action/
7. **Mark plans as completed** when done

End your response with: `<TASK_COMPLETE>`

---
"""
    else:
        prompt += """
---

## Instructions

Please process all files listed above from the Needs_Action/ folder:

1. **List files in Needs_Action/** - Confirm what you see
2. **Read each .md metadata file** - Understand the file context
3. **Read the corresponding FILE_*.original content** if needed for analysis
4. **Create a Plan_*.md in Plans/** for each file being processed
5. **Update Dashboard.md** - Append recent activity to the processing log
6. **Move processed files to Done/** - Clean up Needs_Action/
7. **Mark plans as completed** when done

End your response with: `<TASK_COMPLETE>`

---
"""
    return prompt


def main():
    """Main function to run the orchestrator loop with HITL approval workflow."""
    global LAST_DAILY_BRIEFING
    
    print("=" * 60)
    print("🤖 Personal AI Employee - Orchestrator (Silver Tier)")
    print("=" * 60)
    print(f"📁 Needs Action: {FOLDER_NEEDS_ACTION.absolute()}")
    print(f"⏳ Pending Approval: {FOLDER_PENDING.absolute()}")
    print(f"✅ Approved: {FOLDER_APPROVED.absolute()}")
    print(f"❌ Rejected: {FOLDER_REJECTED.absolute()}")
    print(f"💾 Done: {FOLDER_DONE.absolute()}")
    print(f"📋 Plans: {FOLDER_PLANS.absolute()}")
    print("Polling interval: 30 seconds")
    print("Time-based triggers: Daily Briefing (8 AM), EOD Summary (5 PM)")
    if EMAIL_MCP_AVAILABLE:
        print("📧 Email MCP: ✓ Available")
    else:
        print("📧 Email MCP: ✗ Not available (install python-dotenv)")
    print("Press Ctrl+C to stop\n")

    last_check_count = 0
    last_pending_count = 0

    try:
        while True:
            # Ensure directories exist
            for folder in [FOLDER_PENDING, FOLDER_APPROVED, FOLDER_REJECTED,
                          FOLDER_DONE, FOLDER_NEEDS_ACTION, FOLDER_PLANS]:
                if not folder.exists():
                    folder.mkdir(exist_ok=True)

            # =============================================
            # TIME-BASED TRIGGERS (Daily Briefing, etc.)
            # =============================================
            triggers = check_time_based_triggers()
            
            if 'daily_briefing' in triggers:
                print("\n" + "=" * 60)
                print("📊 Generating Daily Briefing...")
                print("=" * 60)
                print("\n📋 Paste the following prompt into Qwen chat:\n")
                print("-" * 60)
                
                prompt = generate_daily_briefing_prompt()
                print(prompt)
                
                print("-" * 60)
                print("\nWaiting for next check in 30 seconds...\n")

            if 'end_of_day_summary' in triggers:
                print("\n" + "=" * 60)
                print("🌆 Generating End of Day Summary...")
                print("=" * 60)
                print("\n📋 Paste the following prompt into Qwen chat:\n")
                print("-" * 60)
                
                prompt = generate_end_of_day_summary_prompt()
                print(prompt)
                
                print("-" * 60)
                print("\nWaiting for next check in 30 seconds...\n")

            # =============================================
            # HITL WORKFLOW: Check Approved/ for execution
            # =============================================
            approved_files = get_approved_files(FOLDER_APPROVED)
            
            if approved_files:
                print("\n" + "=" * 60)
                print(f"✅ Approved actions ready: {len(approved_files)}")
                print("=" * 60)

                for filename in approved_files:
                    filepath = FOLDER_APPROVED / filename
                    print(f"\n📄 Processing approval: {filename}")

                    # Execute the approved action
                    result = execute_approved_action(filepath)

                    if result['success']:
                        print(f"   ✅ SUCCESS: {result['message']}")
                        if result.get('message_id'):
                            print(f"   📧 Message ID: {result['message_id']}")
                        
                        # Move to Done/
                        done_path = FOLDER_DONE / filename
                        shutil.move(str(filepath), str(done_path))
                        log_approval_action(f"EXECUTED: {filename} → {result['message']}")
                        
                    else:
                        print(f"   ⚠️  {result['message']}")
                        # Keep in Approved/ for manual review
                        log_approval_action(f"FAILED: {filename} → {result['message']}")

                print("\n" + "-" * 60)

            # =============================================
            # HITL WORKFLOW: Check Rejected/ for logging
            # =============================================
            rejected_files = get_approved_files(FOLDER_REJECTED)
            
            if rejected_files:
                print("\n" + "=" * 60)
                print(f"❌ Rejected actions: {len(rejected_files)}")
                print("=" * 60)

                for filename in rejected_files:
                    filepath = FOLDER_REJECTED / filename
                    print(f"\n📄 Rejected: {filename}")
                    
                    # Update file with rejection timestamp
                    content = filepath.read_text(encoding='utf-8')
                    if 'Rejected by user' not in content:
                        content += f"\n\n**Rejected:** {datetime.now().isoformat()}\n**Status:** Rejected by user"
                        filepath.write_text(content, encoding='utf-8')
                    
                    # Move to Done/
                    done_path = FOLDER_DONE / f"REJECTED_{filename}"
                    shutil.move(str(filepath), str(done_path))
                    log_approval_action(f"REJECTED: {filename}")

                print("\n" + "-" * 60)

            # =============================================
            # Check Pending_Approval/ for new requests
            # =============================================
            pending_files = get_pending_approval_files(FOLDER_PENDING)
            
            if pending_files:
                print("\n" + "=" * 60)
                print(f"⚠️  Approval needed: {len(pending_files)} file(s)")
                print("=" * 60)

                for filename in pending_files:
                    filepath = FOLDER_PENDING / filename
                    print(f"\n📋 {filename}")
                    
                    # Parse to show action type
                    parsed = parse_approval_file(filepath)
                    action = parsed['action'] or 'Unknown'
                    to_addr = parsed['to'] or 'N/A'
                    subject = parsed['subject'] or 'N/A'
                    
                    print(f"   Action: {action}")
                    print(f"   To: {to_addr}")
                    print(f"   Subject: {subject}")
                    print(f"   → Review: Pending_Approval/{filename}")
                    print(f"   → To approve: Move to Approved/")
                    print(f"   → To reject: Move to Rejected/")
                    
                    # Mark as notified (so we don't show again)
                    content = filepath.read_text(encoding='utf-8')
                    content += f"\n\n**NOTIFIED:** {datetime.now().isoformat()}"
                    filepath.write_text(content, encoding='utf-8')

                print("\n" + "-" * 60)
                last_pending_count = len(pending_files)

            elif last_pending_count > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] All approvals processed")
                last_pending_count = 0

            # =============================================
            # Check Needs_Action/ for new files
            # =============================================
            files, metadata_files = get_needs_action_files(FOLDER_NEEDS_ACTION)
            current_count = len(files)

            if current_count > 0 and current_count != last_check_count:
                print("\n" + "=" * 60)
                print(f"⚠️  New files detected! ({current_count} files)")
                print("=" * 60)
                print("\n📋 Paste the following prompt into Qwen chat:\n")
                print("-" * 60)

                prompt = generate_qwen_prompt(files, metadata_files)
                print(prompt)

                print("-" * 60)
                print("\nWaiting for next check in 30 seconds...\n")
                last_check_count = current_count

            elif current_count == 0:
                if last_check_count > 0:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Queue is now empty")
                last_check_count = 0

            time.sleep(30)

    except KeyboardInterrupt:
        print("\n\nStopping orchestrator...")
        print("Orchestrator stopped.")

if __name__ == "__main__":
    main()
