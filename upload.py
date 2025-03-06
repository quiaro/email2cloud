import os
import json
import dropbox

# Load configuration from config.json
CREDENTIALS_FILE = "credentials.json"

def load_config(config_file):
    """Loads configuration from a JSON file."""
    if not os.path.exists(config_file):
        print(f"Error: Configuration file {config_file} not found.")
        exit(1)

    with open(config_file, "r") as file:
        return json.load(file)

# Load Dropbox Access Token
config = load_config(CREDENTIALS_FILE)
DROPBOX_ACCESS_TOKEN = config.get("DROPBOX_ACCESS_TOKEN")

if not DROPBOX_ACCESS_TOKEN:
    print("Error: Missing DROPBOX_ACCESS_TOKEN in config.json")
    exit(1)

def upload_to_dropbox(local_file_path, dropbox_destination_path):
    """Uploads a file to Dropbox."""
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

        with open(local_file_path, "rb") as f:
            dbx.files_upload(f.read(), dropbox_destination_path, mode=dropbox.files.WriteMode("overwrite"))

        print(f"File uploaded to Dropbox: {dropbox_destination_path}")

    except Exception as e:
        print(f"Error uploading to Dropbox: {e}")

if __name__ == "__main__":
    local_file = "latest_email.txt"
    dropbox_path = f"/{local_file}"  # Root directory of your Dropbox account

    if not os.path.exists(local_file):
        print(f"Email content not found at {local_file}")
        exit(1)
    else:
        upload_to_dropbox(local_file, dropbox_path)
