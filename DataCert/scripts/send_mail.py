import base64
from pathlib import Path

from .utils import validate_email


class EmailSendError(Exception):
    pass


class EmailSender:
    def __init__(self, config):
        self.config = config
        self.backend = str(config.get("email_backend", "graph")).lower()
        self.from_address = config.get("email", {}).get("from")
        self.reply_to = config.get("email", {}).get("reply_to")
        self.graph_config = config.get("graph", {})
        self.outlook_config = config.get("outlook", {})
        self.shared_mailbox = self.graph_config.get("shared_mailbox") or self.outlook_config.get("shared_mailbox")

        if self.backend not in {"graph", "outlook"}:
            raise ValueError("Unsupported email backend. Use 'graph' or 'outlook'.")

    def send(self, recipient, subject, html_body, attachment_path=None):
        if not validate_email(recipient):
            raise EmailSendError(f"Invalid recipient email address: {recipient}")

        if self.backend == "graph":
            return self._send_graph(recipient, subject, html_body, attachment_path)

        return self._send_outlook(recipient, subject, html_body, attachment_path)

    def _send_graph(self, recipient, subject, html_body, attachment_path):
        try:
            import msal
            import requests
        except ImportError as exc:
            raise EmailSendError("Graph backend requires msal and requests packages.") from exc

        tenant_id = self.graph_config.get("tenant_id")
        client_id = self.graph_config.get("client_id")
        client_secret = self.graph_config.get("client_secret")
        mailbox = self.shared_mailbox or self.from_address

        if not all([tenant_id, client_id, client_secret, mailbox]):
            raise EmailSendError("Graph backend configuration is incomplete.")

        authority = f"https://login.microsoftonline.com/{tenant_id}"
        app = msal.ConfidentialClientApplication(
            client_id,
            authority=authority,
            client_credential=client_secret,
        )
        result = app.acquire_token_silent(["https://graph.microsoft.com/.default"], account=None)
        if not result:
            result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

        if "access_token" not in result:
            raise EmailSendError(f"Could not acquire Graph access token: {result.get('error_description') or result}")

        message = {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": html_body,
            },
            "toRecipients": [{"emailAddress": {"address": recipient}}],
        }

        if self.reply_to:
            message["replyTo"] = [{"emailAddress": {"address": self.reply_to}}]

        if attachment_path:
            attachment_path = Path(attachment_path)
            if not attachment_path.exists():
                raise EmailSendError(f"Attachment not found: {attachment_path}")
            raw_bytes = attachment_path.read_bytes()
            encoded = base64.b64encode(raw_bytes).decode("utf-8")
            message["attachments"] = [
                {
                    "@odata.type": "#microsoft.graph.fileAttachment",
                    "name": attachment_path.name,
                    "contentBytes": encoded,
                }
            ]

        payload = {"message": message}
        if self.from_address:
            payload["message"]["from"] = {"emailAddress": {"address": self.from_address}}

        send_url = f"https://graph.microsoft.com/v1.0/users/{mailbox}/sendMail"
        response = requests.post(
            send_url,
            headers={
                "Authorization": f"Bearer {result['access_token']}",
                "Content-Type": "application/json",
            },
            json=payload,
        )

        if response.status_code not in (200, 202):
            raise EmailSendError(
                f"Graph sendMail failed ({response.status_code}): {response.text}"
            )

        return response.json() if response.content else {"status": "sent"}

    def _send_outlook(self, recipient, subject, html_body, attachment_path):
        try:
            import win32com.client
        except ImportError as exc:
            raise EmailSendError("Outlook backend requires pywin32 and a locally installed Outlook client.") from exc

        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)
        mail.To = recipient
        mail.Subject = subject
        mail.HTMLBody = html_body

        if attachment_path:
            attachment_path = Path(attachment_path)
            mail.Attachments.Add(str(attachment_path))

        if self.shared_mailbox:
            mail.SentOnBehalfOfName = self.shared_mailbox

        try:
            mail.Send()
        except Exception as exc:
            raise EmailSendError(f"Outlook send failed: {exc}") from exc

        return {"status": "sent"}
