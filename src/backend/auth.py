import gspread
from google.oauth2.service_account import Credentials


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("src/credentials.json", scopes=scope)
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
