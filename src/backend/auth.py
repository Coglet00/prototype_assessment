import gspread
import json
import os
from google.oauth2 import service_account


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Get the JSON string from the environment variable
creds_json = os.getenv("GOOGLE_CREDENTIALS")

if creds_json:
    # Convert the string back into a dictionary
    creds_info = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
else:
    # Fallback for local development if you still have the file
    creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
client = gspread.authorize(creds)

spreadsheet = client.open("Prototype_data")

creator_data = spreadsheet.worksheet("Creator_data")
campaign_data = spreadsheet.worksheet("Campaign_data")


def get_creators():
    records = creator_data.get_all_records()

    return records


def get_campaigns():
    records = campaign_data.get_all_records()

    campaign_names = [records[i]["Campaign Name"] for i in range(len(records))]

    return campaign_names
