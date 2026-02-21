"""
WhatsApp Watcher for Personal AI Employee - Silver Tier

Monitors WhatsApp Web for unread messages with priority keywords.
Creates .md files in Needs_Action/ for matching messages.

⚠️ IMPORTANT: WhatsApp Terms of Service Warning ⚠️
===================================================
Automating WhatsApp Web may violate WhatsApp's Terms of Service.
This could result in:
- Temporary or permanent account suspension
- Phone number ban from WhatsApp

Use at your own risk. Recommended only for:
- Business accounts with API access
- Testing/development environments
- Personal use with full understanding of risks

For production use, consider official WhatsApp Business API instead.

Setup Instructions:
===================
1. Install Playwright:
   pip install playwright
   playwright install chromium

2. First run (to scan QR code - MUST be non-headless):
   - Set HEADLESS=False in this script (line below)
   - Run: python whatsapp_watcher.py
   - Browser opens → Scan QR code with WhatsApp mobile app
   - Session saved to ./whatsapp_session/
   - Close with Ctrl+C

3. Subsequent runs (automated with saved session):
   - Set HEADLESS=True for background operation
   - Run: python whatsapp_watcher.py
   - Session loads from ./whatsapp_session/

4. If session expires:
   - Delete ./whatsapp_session/ folder
   - Repeat step 2 to re-authenticate
"""

import time
import re
from pathlib import Path
from datetime import datetime
from typing import Set, List, Optional

from playwright.sync_api import sync_playwright, Page, BrowserContext


# Configuration
CHECK_INTERVAL = 60  # Seconds between checks
HEADLESS = False  # Set to False for first run (QR scan), True for automated
SESSION_PATH = './whatsapp_session'  # Persistent session storage

# Keywords that indicate high-priority messages
PRIORITY_KEYWORDS = [
    'urgent',
    'invoice',
    'payment',
    'asap',
    'emergency',
    'important',
    'deadline',
    'reply',
    'call',
    'meeting'
]

# WhatsApp Web selectors (may change - update if needed)
SELECTORS = {
    'chat_list': 'div[role="row"]',
    'chat_name': 'div[role="row"] div[aria-level="3"]',
    'unread_indicator': 'span[aria-label*="unread"]',
    'message_preview': 'div[role="row"] span[title*=":"]',
    'last_message_time': 'div[role="row"] time',
}


class BaseWatcher:
    """Base class for all watchers in the AI Employee system."""

    def __init__(self, needs_action_path: Path):
        self.needs_action_path = needs_action_path
        self.processed_ids: Set[str] = set()

    def check_for_new_items(self):
        """Check for new items to process. Override in subclass."""
        raise NotImplementedError

    def run(self, check_interval: int = CHECK_INTERVAL):
        """Run the watcher in an infinite loop."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.__class__.__name__} started...")
        print(f"Output to: {self.needs_action_path.absolute()}")
        print(f"Check interval: {check_interval} seconds")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                self.check_for_new_items()
                time.sleep(check_interval)
        except KeyboardInterrupt:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Stopping {self.__class__.__name__}...")

        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.__class__.__name__} stopped.")


class WhatsAppWatcher(BaseWatcher):
    """
    Watches WhatsApp Web for unread messages with priority keywords.
    Uses Playwright with persistent session storage.
    """

    def __init__(self, needs_action_path: Path, session_path: str = SESSION_PATH,
                 headless: bool = HEADLESS):
        super().__init__(needs_action_path)
        self.session_path = Path(session_path)
        self.headless = headless
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._connect()

    def _connect(self):
        """Launch browser and connect to WhatsApp Web with persistent session."""
        # Ensure session directory exists
        self.session_path.mkdir(parents=True, exist_ok=True)

        # Launch Playwright with persistent context using launch_persistent_context
        playwright = sync_playwright().start()
        
        # Use launch_persistent_context for persistent session
        self.context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.session_path.absolute()),
            headless=self.headless,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=1920,1080',
            ],
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='UTC'
        )

        self.page = self.context.pages[0]
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Browser launched (headless={self.headless})")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Session path: {self.session_path.absolute()}")

        # Navigate to WhatsApp Web
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Loading WhatsApp Web...")
        self.page.goto('https://web.whatsapp.com', wait_until='networkidle', timeout=120000)

        # Wait for page to load (check for chat list or QR code)
        self._wait_for_load()

    def _wait_for_load(self, timeout: int = 60):
        """Wait for WhatsApp to fully load (chat list or QR code)."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Waiting for WhatsApp to load...")

        try:
            # Try different selectors for WhatsApp Web
            selectors = [
                'div[role="row"]',  # Chat list
                '#qr',  # QR code container
                'div[data-testid="default-user"]',  # Default welcome screen
                'div[data-testid="intro"]',  # Intro screen
                '[class*="qr"]',  # Any QR-related element
            ]
            
            # Wait for any of the selectors with longer timeout
            for selector in selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=10000)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Found selector: {selector}")
                    break
                except:
                    continue
            
            # Take a screenshot for debugging
            screenshot_path = self.session_path / 'whatsapp_load.png'
            self.page.screenshot(path=str(screenshot_path))
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Screenshot saved: {screenshot_path}")
            
            # Check if QR code is present (needs manual scan)
            qr_selectors = ['#qr', '[class*="qr"]', 'img[alt*="QR"]']
            has_qr = False
            for qr_sel in qr_selectors:
                if self.page.is_visible(qr_sel):
                    has_qr = True
                    break

            if has_qr or not self.page.is_visible('div[role="row"]'):
                print("\n" + "=" * 60)
                print("⚠️  QR CODE DETECTED - MANUAL SCAN REQUIRED")
                print("=" * 60)
                print("1. A QR code should be visible in the browser")
                print("2. Open WhatsApp on your phone")
                print("3. Go to Settings → Linked Devices → Link a Device")
                print("4. Scan the QR code")
                print("5. Wait for chat list to load...")
                print("=" * 60)
                print(f"\n📸 Check screenshot: {screenshot_path}")
                print("\n💡 TIP: Set HEADLESS=False in whatsapp_watcher.py for first run to see QR code")

                # Wait for user to scan (max 5 minutes)
                try:
                    self.page.wait_for_selector('div[role="row"]', timeout=300000)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Authentication successful!")
                except Exception:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] QR scan timeout")
                    raise TimeoutError("QR code not scanned within 5 minutes")

            print(f"[{datetime.now().strftime('%H:%M:%S')}] WhatsApp Web loaded successfully")

        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error loading WhatsApp: {e}")
            print(f"\n💡 TIP: Delete whatsapp_session/ folder and try again")
            print(f"💡 TIP: Set HEADLESS=False to see what's happening in browser")
            raise

    def _get_unread_chats(self) -> List[dict]:
        """Get list of chats with unread messages."""
        unread_chats = []

        try:
            # Wait for chat list
            self.page.wait_for_selector(SELECTORS['chat_list'], timeout=10000)

            # Get all chat rows
            chat_rows = self.page.query_selector_all(SELECTORS['chat_list'])

            for idx, row in enumerate(chat_rows[:20]):  # Limit to first 20 chats
                try:
                    # Extract chat name
                    name_elem = row.query_selector(SELECTORS['chat_name'])
                    chat_name = name_elem.inner_text() if name_elem else f"Unknown_{idx}"

                    # Extract message preview
                    preview_elem = row.query_selector(SELECTORS['message_preview'])
                    preview_text = preview_elem.inner_text() if preview_elem else ""

                    # Extract timestamp
                    time_elem = row.query_selector(SELECTORS['last_message_time'])
                    timestamp = time_elem.get_attribute('datetime') if time_elem else datetime.now().isoformat()

                    # Check for unread indicator (various selectors)
                    is_unread = False
                    unread_indicators = [
                        'span[aria-label*="unread"]',
                        'span[aria-label*="message"]',
                        'div span[style*="background-color"]',
                    ]
                    for indicator in unread_indicators:
                        if row.query_selector(indicator):
                            is_unread = True
                            break

                    # Also check for unread badge class
                    if 'unread' in row.get_attribute('class') or 'unread' in str(row.evaluate('el => el.className')):
                        is_unread = True

                    if is_unread or self._contains_priority_keyword(preview_text):
                        unread_chats.append({
                            'name': chat_name,
                            'preview': preview_text,
                            'timestamp': timestamp,
                            'element': row,
                            'is_unread': is_unread
                        })

                except Exception as e:
                    print(f"Error processing chat row: {e}")
                    continue

        except Exception as e:
            print(f"Error getting unread chats: {e}")

        return unread_chats

    def _contains_priority_keyword(self, text: str) -> bool:
        """Check if text contains any priority keywords."""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in PRIORITY_KEYWORDS)

    def _generate_suggested_actions(self, chat_name: str, preview: str) -> List[str]:
        """Generate suggested action checkboxes based on message content."""
        actions = []
        preview_lower = preview.lower()

        # Action suggestions based on content patterns
        if any(word in preview_lower for word in ['invoice', 'payment', 'bill']):
            actions.append("- [ ] Process payment/invoice")
            actions.append("- [ ] Forward to accounting if needed")

        if any(word in preview_lower for word in ['urgent', 'asap', 'emergency']):
            actions.append("- [ ] Prioritize - marked as urgent")

        if any(word in preview_lower for word in ['meeting', 'schedule', 'call']):
            actions.append("- [ ] Review and respond to scheduling request")

        if any(word in preview_lower for word in ['deadline', 'due']):
            actions.append("- [ ] Note deadline and plan accordingly")

        if any(word in preview_lower for word in ['reply', 'response']):
            actions.append("- [ ] Draft and send reply")

        # Default actions if no specific patterns matched
        if not actions:
            actions.append("- [ ] Read full message in WhatsApp")
            actions.append("- [ ] Determine required response/action")
            actions.append("- [ ] Respond via WhatsApp or other channel")

        return actions

    def _create_message_file(self, chat: dict):
        """Create a .md file in Needs_Action/ for the WhatsApp message."""
        chat_name = chat['name']
        preview = chat['preview']
        timestamp = chat['timestamp']

        # Generate unique filename
        safe_name = "".join(c if c.isalnum() or c in ' -_' else '_' for c in chat_name[:20])
        file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"WHATSAPP_{file_timestamp}_{safe_name}.md"
        filepath = self.needs_action_path / filename

        # Generate suggested actions
        suggested_actions = self._generate_suggested_actions(chat_name, preview)

        # Determine priority based on keywords
        priority = 'high' if self._contains_priority_keyword(preview) else 'medium'

        # Create markdown content with YAML frontmatter
        content = f"""---
from: "{chat_name}"
received: "{timestamp}"
priority: {priority}
status: pending
source: whatsapp
chat_name: "{chat_name}"
---

# WhatsApp Message: {chat_name}

**From:** {chat_name}  
**Received:** {timestamp}  
**Priority:** {priority.capitalize()}  
**Status:** Pending  
**Source:** WhatsApp Web

---

## Message Preview

{preview}

---

## Suggested Actions

{chr(10).join(suggested_actions)}

---

## Processing Notes

- [ ] Message reviewed in WhatsApp
- [ ] Action taken
- [ ] Response sent (if needed)
- [ ] Moved to Done

---

*Processed by WhatsAppWatcher - Silver Tier*
⚠️ Note: Automation may violate WhatsApp ToS. Use responsibly.
"""

        filepath.write_text(content, encoding='utf-8')

        # Track processed chat to avoid duplicates (using name + timestamp as ID)
        chat_id = f"{chat_name}:{timestamp}"
        self.processed_ids.add(chat_id)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Created: {filename}")

    def check_for_new_items(self):
        """Check WhatsApp for new unread messages with priority keywords."""
        try:
            # Refresh page to get latest messages
            self.page.reload(wait_until='networkidle')
            time.sleep(3)  # Wait for messages to load

            # Get unread/priority chats
            chats = self._get_unread_chats()

            if not chats:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No new priority WhatsApp messages")
                return

            new_count = 0
            for chat in chats:
                chat_id = f"{chat['name']}:{chat['timestamp']}"
                if chat_id not in self.processed_ids:
                    # Only create file if unread or contains priority keyword
                    if chat['is_unread'] or self._contains_priority_keyword(chat['preview']):
                        self._create_message_file(chat)
                        new_count += 1

            if new_count > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Processed {new_count} new WhatsApp message(s)")

        except Exception as error:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] WhatsApp error: {error}")
            # Try to reconnect
            try:
                self._connect()
            except Exception as reconnect_error:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Reconnection failed: {reconnect_error}")

    def close(self):
        """Close browser and cleanup."""
        if self.context:
            self.context.close()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Browser closed")


def main():
    """Main function to start the WhatsApp watcher."""
    # Define paths
    root_path = Path('.')
    needs_action_path = root_path / 'Needs_Action'

    # Ensure directory exists
    needs_action_path.mkdir(exist_ok=True)

    # Print ToS warning
    print("=" * 60)
    print("⚠️  WHATSAPP TERMS OF SERVICE WARNING ⚠️")
    print("=" * 60)
    print("Automating WhatsApp Web may violate WhatsApp's ToS.")
    print("This could result in account suspension or ban.")
    print("Use at your own risk. Consider official WhatsApp Business API.")
    print("=" * 60)
    print()

    # Create and run watcher
    watcher = WhatsAppWatcher(needs_action_path)

    try:
        watcher.run(check_interval=CHECK_INTERVAL)
    finally:
        watcher.close()


if __name__ == "__main__":
    main()
