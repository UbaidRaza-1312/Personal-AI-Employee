"""
Filesystem Watcher for Bronze Tier AI Employee
Monitors Inbox/ folder and moves new files to Needs_Action/ with metadata.
"""

import time
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class InboxHandler(FileSystemEventHandler):
    """Handles file system events in the Inbox folder."""

    def __init__(self, needs_action_path: Path):
        self.needs_action_path = needs_action_path

    def on_created(self, event):
        """Called when a file or directory is created."""
        if event.is_directory:
            return

        src_path = Path(event.src_path)

        # Skip hidden files and temporary files
        if src_path.name.startswith('.') or src_path.name.endswith('.tmp'):
            return

        # Wait briefly to ensure file is fully written
        time.sleep(0.1)

        # Generate unique filename with FILE_ prefix
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        new_filename = f"FILE_{timestamp}_{src_path.name}"
        dest_path = self.needs_action_path / new_filename
        metadata_path = self.needs_action_path / f"{new_filename}.md"

        try:
            # Copy file to Needs_Action/
            shutil.copy2(src_path, dest_path)

            # Get file metadata
            file_size = dest_path.stat().st_size
            created_time = time.strftime("%Y-%m-%d %H:%M:%S")

            # Create metadata file
            metadata_content = f"""---
type: file_drop
original_name: {src_path.name}
size: {file_size}
created_timestamp: {created_time}
---

# File Metadata

- **Type:** file_drop
- **Original Name:** {src_path.name}
- **Size:** {file_size} bytes
- **Created:** {created_time}
- **Stored As:** {new_filename}

## Description
New file dropped for processing.

## Status
- [ ] Pending review
- [ ] Ready for action
"""

            metadata_path.write_text(metadata_content, encoding='utf-8')

            print(f"[+] Processed: {src_path.name} → {new_filename}")

        except Exception as e:
            print(f"[-] Error processing {src_path.name}: {e}")


def main():
    """Start the filesystem watcher."""
    # Define paths relative to current directory
    root_path = Path('.')
    inbox_path = root_path / 'Inbox'
    needs_action_path = root_path / 'Needs_Action'

    # Ensure directories exist
    inbox_path.mkdir(exist_ok=True)
    needs_action_path.mkdir(exist_ok=True)

    # Create event handler and observer
    event_handler = InboxHandler(needs_action_path)
    observer = Observer()
    observer.schedule(event_handler, str(inbox_path), recursive=False)

    # Start watching
    print("Watcher started...")
    print(f"Monitoring: {inbox_path.absolute()}")
    print(f"Output to: {needs_action_path.absolute()}")
    print("Press Ctrl+C to stop\n")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        observer.stop()

    observer.join()
    print("Watcher stopped.")


if __name__ == "__main__":
    main()
