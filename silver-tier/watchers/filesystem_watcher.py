"""
Filesystem Watcher for Personal AI Employee - Bronze Tier

Monitors the Inbox/ folder and copies new files to Needs_Action/
with accompanying metadata files.
"""

import time
import shutil
from pathlib import Path
from datetime import datetime
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

        source_path = Path(event.src_path)
        self._process_file(source_path)

    def _process_file(self, source_path: Path):
        """Process a new file: copy to Needs_Action and create metadata."""
        # Wait briefly to ensure file is fully written
        time.sleep(0.1)

        # Generate unique filename with timestamp prefix
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"FILE_{timestamp}_{source_path.name}"
        dest_path = self.needs_action_path / new_filename
        metadata_path = self.needs_action_path / f"{new_filename}.md"

        # Copy the file to Needs_Action
        shutil.copy2(source_path, dest_path)

        # Get file metadata
        file_stat = dest_path.stat()
        size_bytes = file_stat.st_size
        created_time = datetime.fromtimestamp(file_stat.st_ctime).isoformat()

        # Create metadata file
        metadata_content = f"""# File Metadata

**Type:** file_drop
**Original Name:** {source_path.name}
**Size:** {size_bytes} bytes
**Created:** {created_time}
**Copied To Needs_Action:** {datetime.now().isoformat()}

---

## Description
New file dropped for processing

---

## Processing Status
- [ ] File analyzed
- [ ] Plan created
- [ ] Processed
- [ ] Moved to Done
"""

        metadata_path.write_text(metadata_content)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Processed: {source_path.name} → {new_filename}")


def main():
    """Main function to start the filesystem watcher."""
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
