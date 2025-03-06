import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def authenticate_gmail():
    """Authenticates and returns Gmail API service."""
    creds = None
    token_file = "token.json"

    # Load credentials if available
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file)

    # If credentials are invalid or don't exist, request new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next use
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def get_last_email(service):
    """Fetches the latest email from the Gmail inbox."""
    results = service.users().messages().list(userId="me", maxResults=1).execute()
    messages = results.get("messages", [])

    if not messages:
        print("No emails found.")
        return None

    message_id = messages[0]["id"]
    email = service.users().messages().get(userId="me", id=message_id, format="full").execute()

    payload = email["payload"]
    headers = payload["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
    
    body = get_email_body(payload)

    return subject, body

def get_email_body(payload):
    """Extracts the body of the email from its payload."""
    parts = payload.get("parts", [])
    if parts:
        for part in parts:
            if part["mimeType"] == "text/plain":
                return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")

    return "No body found."

def save_email_to_file(subject, body):
    """Saves email content to a text file."""
    filename = "latest_email.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Subject: {subject}\n\n{body}")

    print(f"Email saved to {filename}")


if __name__ == "__main__":
    local_file = "latest_email.txt"
    dropbox_path = f"/Apps/Migrador de Correos/{local_file}"  # Root directory of your Dropbox account

    service = authenticate_gmail()
    email_data = get_last_email(service)

    if email_data:
        save_email_to_file(*email_data)

