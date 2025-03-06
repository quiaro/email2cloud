import os
import sys
import base64
import datetime
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

def parse_dates():
    """Parses command-line arguments for date range."""
    today = datetime.date.today()

    # Read arguments
    start_date = sys.argv[1] if len(sys.argv) > 1 else today.strftime("%Y-%m-%d")
    end_date = sys.argv[2] if len(sys.argv) > 2 else today.strftime("%Y-%m-%d")

    try:
        start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        print("Error: Dates must be in YYYY-MM-DD format.")
        sys.exit(1)

    if start_date_obj > end_date_obj:
        print("Error: Start date cannot be after end date.")
        sys.exit(1)

    return start_date_obj, end_date_obj

def get_emails_in_date_range(service, start_date, end_date):
    """Fetches emails within the specified date range."""
    query = f"after:{start_date} before:{(end_date + datetime.timedelta(days=1))}"  # End date inclusive
    results = service.users().messages().list(userId="me", q=query, maxResults=100).execute()
    messages = results.get("messages", [])

    if not messages:
        print(f"No emails found from {start_date} to {end_date}.")
        return []

    return messages

def get_email_details(service, message_id):
    """Fetches the email's subject and body using its ID."""
    email = service.users().messages().get(userId="me", id=message_id, format="full").execute()
    payload = email["payload"]
    headers = payload["headers"]
    subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
    body = get_email_body(payload)
    date = extract_email_date(headers)

    return date, subject, body

def get_email_body(payload):
    """Extracts the body of the email from its payload."""
    parts = payload.get("parts", [])
    if parts:
        for part in parts:
            if part["mimeType"] == "text/plain":
                return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")

    return "No body found."

def extract_email_date(headers):
    """Extracts and formats the email's date."""
    date_header = next((h["value"] for h in headers if h["name"] == "Date"), None)
    if date_header:
        try:
            trimmed_date = date_header[:16].strip()
            parsed_date = datetime.datetime.strptime(trimmed_date, "%a, %d %b %Y")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            return "unknown_date"
    return "unknown_date"

def save_email_to_file(date, unique_id, subject, body):
    """Saves email content to a text file with <date>-<id>.txt format."""
    filename = f"{date}-{unique_id}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Subject: {subject}\n\n{body}")

    print(f"Email saved as {filename}")

if __name__ == "__main__":
    # Parse date arguments
    start_date, end_date = parse_dates()

    # Authenticate and fetch emails
    service = authenticate_gmail()
    emails = get_emails_in_date_range(service, start_date, end_date)

    # Process and save emails
    unique_ids = {}
    for msg in emails:
        email_date, subject, body = get_email_details(service, msg["id"])

        # Generate a unique sequential ID per date
        if email_date not in unique_ids:
            unique_ids[email_date] = 1
        else:
            unique_ids[email_date] += 1

        save_email_to_file(email_date, unique_ids[email_date], subject, body)
