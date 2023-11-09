import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fruit_shop')


def get_supply_data():
    """
    Get supply figure input from user
    """
    print("Get dispatch data from  worksheet.")
    print("Data should be seven numbers separated by commas.")
    print("Example: 25,30,30,15,9,17,20\n")

    data_str = input("Enter your data here: ")
    print(f"The data provided is {data_str}")


get_supply_data()
