"""
Email MCP Server - Silver Tier

Simple Python MCP server for sending emails via Gmail SMTP.
Used by the orchestrator when actions are approved.

Setup:
======
1. Copy .env.example to .env
2. Fill in your Gmail credentials (use App Password, not regular password)
3. Install: pip install python-dotenv

Gmail App Password Setup:
=========================
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification (if not already enabled)
3. Go to https://myaccount.google.com/apppasswords
4. Select app: "Mail", Select device: "Other"
5. Generate password - copy the 16-character password
6. Paste into .env as GMAIL_APP_PASSWORD

Usage:
======
# Direct function call
from email_mcp import send_email
send_email("recipient@example.com", "Subject", "Body text")

# Run as script (test mode)
python email_mcp.py
"""

import os
import smtplib
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Configuration from environment
GMAIL_EMAIL = os.getenv('GMAIL_EMAIL', '')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
DRY_RUN = os.getenv('DRY_RUN', 'false').lower() == 'true'

# Logging setup
LOG_DIR = Path('Logs')
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'email_log.txt'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def send_email(
    to: str,
    subject: str,
    body: str,
    attachment_path: Optional[str] = None,
    cc: Optional[str] = None,
    bcc: Optional[str] = None
) -> dict:
    """
    Send an email via Gmail SMTP.

    Args:
        to: Recipient email address
        subject: Email subject line
        body: Email body text (plain text)
        attachment_path: Optional path to file attachment
        cc: Optional CC email address
        bcc: Optional BCC email address

    Returns:
        dict: {
            'success': bool,
            'message': str,
            'message_id': str (if sent),
            'dry_run': bool
        }
    """
    result = {
        'success': False,
        'message': '',
        'message_id': None,
        'dry_run': DRY_RUN
    }

    # Validate credentials
    if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
        error_msg = "Gmail credentials not configured. Check .env file."
        logger.error(error_msg)
        result['message'] = error_msg
        return result

    if not to:
        error_msg = "Recipient email address is required"
        logger.error(error_msg)
        result['message'] = error_msg
        return result

    timestamp = datetime.now().isoformat()

    # Dry run mode - just log and return
    if DRY_RUN:
        logger.info("=" * 60)
        logger.info("DRY RUN - Email not actually sent")
        logger.info("=" * 60)
        logger.info(f"To: {to}")
        if cc:
            logger.info(f"CC: {cc}")
        if bcc:
            logger.info(f"BCC: {bcc}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Body:\n{body}")
        if attachment_path:
            logger.info(f"Attachment: {attachment_path}")
        logger.info("=" * 60)

        result['success'] = True
        result['message'] = f"Dry run: Email would be sent to {to}"
        result['message_id'] = f"DRYRUN_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return result

    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = GMAIL_EMAIL
        msg['To'] = to
        msg['Subject'] = subject

        if cc:
            msg['Cc'] = cc

        # Add body
        msg.attach(MIMEText(body, 'plain'))

        # Add attachment if provided
        if attachment_path:
            attachment = Path(attachment_path)
            if attachment.exists():
                try:
                    with open(attachment, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())

                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{attachment.name}"'
                    )
                    msg.attach(part)
                    logger.info(f"Attached: {attachment.name}")
                except Exception as e:
                    logger.warning(f"Failed to attach {attachment_path}: {e}")
            else:
                logger.warning(f"Attachment not found: {attachment_path}")

        # Build recipient list
        recipients = [to]
        if cc:
            recipients.extend(cc.split(','))
        if bcc:
            recipients.extend(bcc.split(','))

        # Connect to SMTP server and send
        logger.info(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)

        # Send email
        text = msg.as_string()
        server.sendmail(GMAIL_EMAIL, recipients, text)
        server.quit()

        # Generate message ID
        message_id = f"SENT_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        logger.info(f"Email sent successfully to {to}")
        logger.info(f"Message ID: {message_id}")

        result['success'] = True
        result['message'] = f"Email sent to {to}"
        result['message_id'] = message_id

    except smtplib.SMTPAuthenticationError:
        error_msg = "SMTP Authentication failed. Check email and app password."
        logger.error(error_msg)
        result['message'] = error_msg

    except smtplib.SMTPConnectError:
        error_msg = f"Failed to connect to SMTP server {SMTP_SERVER}:{SMTP_PORT}"
        logger.error(error_msg)
        result['message'] = error_msg

    except smtplib.SMTPException as e:
        error_msg = f"SMTP error: {str(e)}"
        logger.error(error_msg)
        result['message'] = error_msg

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        result['message'] = error_msg

    return result


def send_email_from_template(
    to: str,
    subject: str,
    template_path: str,
    attachment_path: Optional[str] = None
) -> dict:
    """
    Send email using a template file for the body.

    Args:
        to: Recipient email address
        subject: Email subject line
        template_path: Path to text file containing email body
        attachment_path: Optional path to file attachment

    Returns:
        dict: Same as send_email()
    """
    template = Path(template_path)
    if not template.exists():
        error_msg = f"Template not found: {template_path}"
        logger.error(error_msg)
        return {
            'success': False,
            'message': error_msg,
            'message_id': None,
            'dry_run': DRY_RUN
        }

    body = template.read_text(encoding='utf-8')
    return send_email(to, subject, body, attachment_path)


# MCP-style tool definition (for reference)
MCP_TOOLS = {
    'send_email': {
        'description': 'Send an email via Gmail SMTP',
        'inputSchema': {
            'type': 'object',
            'properties': {
                'to': {
                    'type': 'string',
                    'description': 'Recipient email address'
                },
                'subject': {
                    'type': 'string',
                    'description': 'Email subject line'
                },
                'body': {
                    'type': 'string',
                    'description': 'Email body text (plain text)'
                },
                'attachment_path': {
                    'type': 'string',
                    'description': 'Optional path to file attachment'
                },
                'cc': {
                    'type': 'string',
                    'description': 'Optional CC email address'
                }
            },
            'required': ['to', 'subject', 'body']
        }
    }
}


def main():
    """Test the email functionality."""
    print("=" * 60)
    print("Email MCP Server - Test Mode")
    print("=" * 60)
    print(f"Gmail Email: {GMAIL_EMAIL}")
    print(f"DRY_RUN: {DRY_RUN}")
    print("=" * 60)

    if not GMAIL_EMAIL:
        print("\n⚠️  GMAIL_EMAIL not set in .env")
        print("Please copy .env.example to .env and configure credentials")
        return

    # Test email (dry run by default)
    test_result = send_email(
        to="test@example.com",
        subject="Test Email from MCP Server",
        body="This is a test email sent from the Email MCP Server.\n\nIf you receive this, the server is working correctly!",
        cc=None
    )

    print("\nTest Result:")
    print(f"  Success: {test_result['success']}")
    print(f"  Message: {test_result['message']}")
    print(f"  Message ID: {test_result['message_id']}")
    print(f"  Dry Run: {test_result['dry_run']}")

    print("\n" + "=" * 60)
    print(f"Check {LOG_FILE} for detailed logs")
    print("=" * 60)


if __name__ == "__main__":
    main()
