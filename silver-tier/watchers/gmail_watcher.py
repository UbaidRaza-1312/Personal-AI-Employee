"""
Gmail Watcher for Personal AI Employee - Silver Tier

Monitors Gmail for unread + important emails and creates .md files in Needs_Action/
with YAML frontmatter, email content, and suggested actions.

Setup Instructions:
===================
1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Create a new project (e.g., "AI Employee Gmail")
3. Enable Gmail API:
   - Go to "APIs & Services" → "Library"
   - Search for "Gmail API" and click Enable
4. Configure OAuth consent screen:
   - Go to "APIs & Services" → "OAuth consent screen"
   - Select "External" user type
   - Fill in app name, user support email, developer contact
   - Add scopes: Add "../auth/gmail.readonly" scope
   - Add test users (your Gmail address)
   - Click Save and Continue
5. Create credentials:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: "Desktop app"
   - Download the credentials.json file
   - Place it in this project directory
6. Install required packages:
   pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
7. Run the script once to authorize:
   python gmail_watcher.py
   - Browser will open for OAuth consent
   - Grant permissions
   - token.json will be created automatically
8. Script will now monitor Gmail every 120 seconds
"""

import time
import base64
from pathlib import Path
from datetime import datetime
from typing import Set, Optional
from email import message_from_bytes

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Gmail API OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Check interval in seconds
CHECK_INTERVAL = 120

# Query for unread + important emails
GMAIL_QUERY = 'is:unread is:important'


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


class GmailWatcher(BaseWatcher):
    """
    Watches Gmail for unread + important emails.
    Creates .md files in Needs_Action/ for each new email.
    """

    def __init__(self, needs_action_path: Path, credentials_path: str = 'credentials.json',
                 token_path: str = 'token.json'):
        super().__init__(needs_action_path)
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service: Optional[build] = None
        self._connect()

    def _connect(self):
        """Authenticate and connect to Gmail API."""
        creds = None

        # Load existing token if available
        token_path = Path(self.token_path)
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        # Refresh or obtain new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                credentials_file = Path(self.credentials_path)
                if not credentials_file.exists():
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_path}\n"
                        "Please follow setup instructions to create credentials.json"
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials for future use
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        # Build Gmail API service
        self.service = build('gmail', 'v1', credentials=creds)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Connected to Gmail API")

    def _decode_email_body(self, message: dict) -> str:
        """Decode the email body from base64url encoding."""
        try:
            # Try to get plain text body
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = part['body'].get('data', '')
                        if body:
                            decoded = base64.urlsafe_b64decode(body).decode('utf-8')
                            return decoded
            # Fallback to body if no parts
            body = message['payload']['body'].get('data', '')
            if body:
                decoded = base64.urlsafe_b64decode(body).decode('utf-8')
                return decoded
        except Exception as e:
            print(f"Error decoding email body: {e}")
        return "[Unable to decode email body]"

    def _get_email_headers(self, message: dict) -> dict:
        """Extract headers from email message."""
        headers = {}
        for header in message['payload']['headers']:
            name = header['name'].lower()
            value = header['value']
            if name in ['from', 'to', 'subject', 'date']:
                headers[name] = value
        return headers

    def _generate_suggested_actions(self, subject: str, snippet: str) -> list:
        """Generate suggested action checkboxes based on email content."""
        actions = []
        subject_lower = subject.lower()
        snippet_lower = snippet.lower()

        # Action suggestions based on content patterns
        if any(word in subject_lower for word in ['meeting', 'schedule', 'calendar']):
            actions.append("- [ ] Review meeting details and add to calendar")

        if any(word in subject_lower for word in ['invoice', 'payment', 'bill']):
            actions.append("- [ ] Process payment/invoice")
            actions.append("- [ ] Forward to accounting if needed")

        if any(word in subject_lower for word in ['urgent', 'asap', 'immediate']):
            actions.append("- [ ] Prioritize - marked as urgent")

        if 'attachment' in snippet_lower:
            actions.append("- [ ] Download and review attachments")

        if any(word in subject_lower for word in ['review', 'approve', 'feedback']):
            actions.append("- [ ] Provide review/feedback")

        # Default actions if no specific patterns matched
        if not actions:
            actions.append("- [ ] Read full email content")
            actions.append("- [ ] Determine required response/action")
            actions.append("- [ ] Respond or delegate as needed")

        return actions

    def _create_email_file(self, message: dict):
        """Create a .md file in Needs_Action/ for the email."""
        message_id = message['id']
        snippet = message.get('snippet', '')

        # Get full message details
        full_message = self.service.users().messages().get(
            userId='me',
            id=message_id,
            format='metadata',
            metadataHeaders=['From', 'To', 'Subject', 'Date']
        ).execute()

        # Extract headers
        headers = self._get_email_headers(full_message)
        from_addr = headers.get('from', 'Unknown')
        subject = headers.get('subject', 'No Subject')
        received_date = headers.get('date', datetime.now().isoformat())

        # Get full body
        full_message_body = self.service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()
        body = self._decode_email_body(full_message_body)

        # Generate filename
        # Sanitize subject for filename
        safe_subject = "".join(c if c.isalnum() or c in ' -_' else '_' for c in subject[:30])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"EMAIL_{message_id}_{safe_subject}.md"
        filepath = self.needs_action_path / filename

        # Generate suggested actions
        suggested_actions = self._generate_suggested_actions(subject, snippet)

        # Create markdown content with YAML frontmatter
        content = f"""---
from: "{from_addr}"
subject: "{subject}"
received: "{received_date}"
priority: high
status: pending
message_id: "{message_id}"
---

# Email: {subject}

**From:** {from_addr}  
**Received:** {received_date}  
**Priority:** High  
**Status:** Pending

---

## Email Content

{body}

---

## Suggested Actions

{chr(10).join(suggested_actions)}

---

## Processing Notes

- [ ] Email reviewed
- [ ] Action taken
- [ ] Response sent (if needed)
- [ ] Moved to Done

---

*Processed by GmailWatcher - Silver Tier*
"""

        filepath.write_text(content, encoding='utf-8')
        self.processed_ids.add(message_id)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Created: {filename}")

    def check_for_new_items(self):
        """Check Gmail for new unread + important emails."""
        if not self.service:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Not connected to Gmail API")
            return

        try:
            # Query for unread + important emails
            results = self.service.users().messages().list(
                userId='me',
                q=GMAIL_QUERY,
                maxResults=10
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No new unread+important emails")
                return

            new_count = 0
            for message in messages:
                if message['id'] not in self.processed_ids:
                    self._create_email_file(message)
                    new_count += 1

            if new_count > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Processed {new_count} new email(s)")

        except HttpError as error:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Gmail API error: {error}")
        except Exception as error:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {error}")


def main():
    """Main function to start the Gmail watcher."""
    # Define paths
    root_path = Path('.')
    needs_action_path = root_path / 'Needs_Action'

    # Ensure directory exists
    needs_action_path.mkdir(exist_ok=True)

    # Create and run watcher
    watcher = GmailWatcher(needs_action_path)
    watcher.run(check_interval=CHECK_INTERVAL)


if __name__ == "__main__":
    main()
