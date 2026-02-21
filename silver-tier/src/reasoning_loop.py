"""
Automatic Reasoning Loop for Personal AI Employee - Silver Tier

Processes files in Needs_Action/ folder using rule-based logic.
No AI/API required - fully automatic!

Usage:
    python reasoning_loop.py

Features:
- Automatically categorizes files (EMAIL, WHATSAPP, FILE)
- Generates Plans/*.md files
- Moves processed files to Done/
- Creates approval requests for sensitive actions
"""

import shutil
import sys
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Folder paths
FOLDER_NEEDS_ACTION = Path('Needs_Action')
FOLDER_DONE = Path('Done')
FOLDER_PLANS = Path('Plans')
FOLDER_LOGS = Path('Logs')
FOLDER_PENDING = Path('Pending_Approval')

# Ensure folders exist
for folder in [FOLDER_NEEDS_ACTION, FOLDER_DONE, FOLDER_PLANS, FOLDER_LOGS, FOLDER_PENDING]:
    folder.mkdir(exist_ok=True)

# Log file
REASONING_LOG = FOLDER_LOGS / 'reasoning_log.txt'

# Emoji replacements for Windows console compatibility
EMOJI = {
    'loop': '[LOOP]',
    'folder': '[DIR]',
    'file': '[FILE]',
    'check': '[OK]',
    'clock': '[WAIT]',
    'error': '[ERR]',
    'info': '[INFO]',
    'plan': '[PLAN]',
    'approval': '[APPROVE]',
    'done': '[DONE]',
    'dashboard': '[DASH]',
    'email': '[MAIL]',
    'msg': '[MSG]',
    'doc': '[DOC]',
    'tip': '[TIP]'
}


def log_message(message: str):
    """Log messages to file and console."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    
    # Append to log file
    with open(REASONING_LOG, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    
    # Replace emojis for Windows console
    safe_message = message
    safe_message = safe_message.replace('✅', '[OK]').replace('⏸️', '[APPROVE]')
    safe_message = safe_message.replace('📄', '[FILE]').replace('📁', '[DIR]')
    safe_message = safe_message.replace('📊', '[DASH]').replace('📧', '[MAIL]')
    safe_message = safe_message.replace('ℹ️', '[INFO]').replace('💡', '[TIP]')
    safe_message = safe_message.replace('❌', '[ERR]').replace('🔄', '[LOOP]')
    safe_message = safe_message.replace('⚠️', '[WARN]').replace('🤖', '[AI]')
    safe_message = safe_message.replace('📝', '[LOG]').replace('📌', '[PIN]')
    
    print(safe_message)


def read_file_metadata(md_file: Path) -> dict:
    """Read YAML frontmatter from .md file."""
    content = md_file.read_text(encoding='utf-8')
    
    metadata = {
        'full_path': str(md_file),
        'content': content,
        'filename': md_file.stem,
        'type': 'unknown',
        'priority': 'normal',
        'from': '',
        'subject': '',
        'body': content
    }
    
    # Extract YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml_content = parts[1]
            metadata['body'] = parts[2]
            
            # Parse simple YAML
            for line in yaml_content.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
            
            # Determine type from filename
            if metadata['filename'].startswith('EMAIL_'):
                metadata['type'] = 'email'
            elif metadata['filename'].startswith('WHATSAPP_'):
                metadata['type'] = 'whatsapp'
            elif metadata['filename'].startswith('FILE_'):
                metadata['type'] = 'file'
    
    return metadata


def categorize_file(metadata: dict) -> dict:
    """Categorize file and determine required actions."""
    result = {
        'metadata': metadata,
        'category': 'general',
        'requires_approval': False,
        'action': 'archive',
        'priority': metadata.get('priority', 'normal').lower()
    }
    
    filename = metadata['filename'].upper()
    
    # EMAIL files - usually need approval for replies
    if metadata['type'] == 'email' or 'EMAIL' in filename:
        result['category'] = 'email'
        
        # Check if reply needed (look for keywords in content)
        content_lower = metadata['content'].lower()
        if any(word in content_lower for word in ['reply', 'respond', 'answer', 'question', 'urgent', 'asap']):
            result['requires_approval'] = True
            result['action'] = 'reply_email'
        else:
            result['action'] = 'archive'
        
        # High priority indicators
        if any(word in content_lower for word in ['urgent', 'emergency', 'asap', 'important']):
            result['priority'] = 'high'
    
    # WHATSAPP files - may need response
    elif metadata['type'] == 'whatsapp' or 'WHATSAPP' in filename:
        result['category'] = 'message'
        
        content_lower = metadata['content'].lower()
        if any(word in content_lower for word in ['reply', 'respond', 'answer', 'question', 'urgent']):
            result['requires_approval'] = True
            result['action'] = 'send_message'
        else:
            result['action'] = 'archive'
    
    # FILE files - general documents, no approval needed
    elif metadata['type'] == 'file' or 'FILE' in filename:
        result['category'] = 'document'
        result['action'] = 'archive'
        result['requires_approval'] = False
    
    return result


def create_plan_file(categorized_files: list) -> Path:
    """Create a Plan.md file summarizing all processing."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    plan_filename = f"PLAN_{timestamp}.md"
    plan_path = FOLDER_PLANS / plan_filename
    
    # Count categories
    emails = [f for f in categorized_files if f['category'] == 'email']
    messages = [f for f in categorized_files if f['category'] == 'message']
    documents = [f for f in categorized_files if f['category'] == 'document']
    
    approval_needed = [f for f in categorized_files if f['requires_approval']]
    
    content = f"""---
title: Auto-Generated Action Plan
created: {datetime.now().isoformat()}
files_processed: {len(categorized_files)}
status: Completed
---

# Action Plan - {timestamp}

## Summary

| Category | Count |
|----------|-------|
| Emails | {len(emails)} |
| Messages | {len(messages)} |
| Documents | {len(documents)} |
| **Total** | **{len(categorized_files)}** |

## Processing Results

"""
    
    for item in categorized_files:
        meta = item['metadata']
        status = "[APPROVE] Approval Needed" if item['requires_approval'] else "[OK] Auto-Processed"
        content += f"### {meta['filename']}\n"
        content += f"- **Type:** {item['category']}\n"
        content += f"- **Priority:** {item['priority']}\n"
        content += f"- **Status:** {status}\n"
        content += f"- **Action:** {item['action']}\n"
        
        if meta.get('subject'):
            content += f"- **Subject:** {meta['subject']}\n"
        if meta.get('from'):
            content += f"- **From:** {meta['from']}\n"
        
        content += "\n"
    
    # Approval section
    if approval_needed:
        content += """## [APPROVE] Approval Required

The following actions need human approval before execution:

"""
        for item in approval_needed:
            meta = item['metadata']
            content += f"- [ ] **{item['action']}**: {meta['filename']}\n"
            content += f"  -> Check `Pending_Approval/` folder for approval file\n"
    else:
        content += """## [OK] No Approval Needed

All actions were auto-processed. No human intervention required.

"""
    
    # Actions taken
    content += """## Actions Taken

"""
    for item in categorized_files:
        content += f"- [x] Processed `{item['metadata']['filename']}` -> {item['action']}\n"
    
    content += f"""
## Files Generated

- Plan: `Plans/{plan_filename}`
- Processed files moved to: `Done/`

---
*Generated by reasoning_loop.py (Rule-Based Auto-Processing)*
"""
    
    plan_path.write_text(content, encoding='utf-8')
    return plan_path


def create_approval_file(categorized_item: dict) -> Path:
    """Create approval file for actions needing human review."""
    meta = categorized_item['metadata']
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if categorized_item['category'] == 'email':
        approval_filename = f"SendEmail_{meta['filename']}_{timestamp}.md"
    else:
        approval_filename = f"SendMessage_{meta['filename']}_{timestamp}.md"
    
    approval_path = FOLDER_PENDING / approval_filename
    
    subject = meta.get('subject', 'No Subject')
    from_addr = meta.get('from', 'Unknown')
    
    content = f"""---
action_type: {categorized_item['action']}
original_file: {meta['filename']}
priority: {categorized_item['priority']}
created: {datetime.now().isoformat()}
status: Pending
---

# Approval Required: {categorized_item['action'].replace('_', ' ').title()}

## Original Item Details

| Field | Value |
|-------|-------|
| **File** | {meta['filename']} |
| **Type** | {categorized_item['category']} |
| **Priority** | {categorized_item['priority']} |
| **From** | {from_addr} |
| **Subject** | {subject} |

## Suggested Action

**Action Type:** `{categorized_item['action']}`

This item requires a response. Please review and approve the suggested action.

## Original Content

```
{meta['body'][:1500]}
```

## Approval Instructions

1. Review the content above
2. If approval is needed, move this file to `Approved/`
3. If rejected, move to `Rejected/`

---
*Auto-generated by reasoning_loop.py*
"""
    
    approval_path.write_text(content, encoding='utf-8')
    return approval_path


def move_files_to_done(categorized_files: list):
    """Move processed files to Done/ folder."""
    for item in categorized_files:
        md_path = Path(item['metadata']['full_path'])
        if md_path.exists():
            dest_md = FOLDER_DONE / md_path.name
            shutil.move(str(md_path), str(dest_md))
            log_message(f"   [OK] Moved to Done/: {md_path.name}")


def update_dashboard():
    """Update Dashboard.md with processing stats."""
    dashboard_path = Path('Dashboard.md')
    if not dashboard_path.exists():
        log_message("   ℹ️  Dashboard.md not found, skipping update")
        return
    
    content = dashboard_path.read_text(encoding='utf-8')
    
    # Update processing log
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    new_entry = f"\n- [{timestamp}] Reasoning Loop: Auto-processed files"
    
    if '## Processing Log' in content:
        content = content.replace('## Processing Log', f'## Processing Log{new_entry}')
    else:
        content += f"\n\n## Processing Log{new_entry}\n"
    
    dashboard_path.write_text(content, encoding='utf-8')
    log_message("   [DASH] Dashboard updated")


def run_reasoning_loop():
    """Main reasoning loop function."""
    print("\n" + "=" * 60)
    print("[LOOP] REASONING LOOP - Automatic Processing")
    print("=" * 60)
    
    # Check for files in Needs_Action/
    md_files = list(FOLDER_NEEDS_ACTION.glob('*.md'))
    
    if not md_files:
        log_message("[INFO] No files in Needs_Action/ folder.")
        print("\n[TIP] Drop files in Inbox/ or wait for Gmail watcher")
        print("   Command: python reasoning_loop.py\n")
        return
    
    log_message(f"[DIR] Found {len(md_files)} file(s) in Needs_Action/")
    print()
    
    # Read and categorize all files
    categorized_files = []
    for md_file in md_files:
        try:
            metadata = read_file_metadata(md_file)
            categorized = categorize_file(metadata)
            categorized_files.append(categorized)
            
            status = "[APPROVE] Needs Approval" if categorized['requires_approval'] else "[OK] Auto"
            log_message(f"   [FILE] {md_file.name}")
            log_message(f"      Type: {categorized['category']}, Priority: {categorized['priority']}, Status: {status}")
        except Exception as e:
            log_message(f"   [ERR] Error reading {md_file.name}: {e}")
    
    if not categorized_files:
        log_message("[ERR] No valid files to process")
        return
    
    print()
    
    # Create approval files for items needing approval
    approval_items = [f for f in categorized_files if f['requires_approval']]
    for item in approval_items:
        approval_path = create_approval_file(item)
        log_message(f"   [APPROVE] Approval created: {approval_path.name}")
    
    # Create main plan file
    plan_path = create_plan_file(categorized_files)
    log_message(f"[FILE] Plan created: {plan_path.name}")
    
    # Move all files to Done/
    move_files_to_done(categorized_files)
    
    # Update Dashboard
    update_dashboard()
    
    # Print summary
    print("\n" + "=" * 60)
    print("[OK] REASONING LOOP COMPLETE")
    print("=" * 60)
    print(f"Files Processed: {len(categorized_files)}")
    print(f"  - Emails: {len([f for f in categorized_files if f['category'] == 'email'])}")
    print(f"  - Messages: {len([f for f in categorized_files if f['category'] == 'message'])}")
    print(f"  - Documents: {len([f for f in categorized_files if f['category'] == 'document'])}")
    print(f"Approval Needed: {len(approval_items)}")
    print(f"Plan Created: {plan_path.name}")
    print(f"Log File: {REASONING_LOG}")
    print("=" * 60)
    print("\n[TIP] Next: Check Pending_Approval/ folder if approval needed")
    print("   Or run again: python reasoning_loop.py\n")


if __name__ == '__main__':
    try:
        run_reasoning_loop()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
