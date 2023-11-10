import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fruit_shop')


def get_delivery_data():
    """
    Get delivery figure input from user
    """
    while True:
        print("Get delivery data from  worksheet.")
        print("Data should be seven numbers separated by commas.")
        print("Example: 25,30,30,15,9,17,20\n")

        data_str = input("Enter your data here: ")

        delivery_data = data_str.split(",")

        if validate_data(delivery_data):
            print("Data is valid!")
            break

    return delivery_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings can not be converted into int,
    or if there aren't exactly 7 values.
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 7:
            raise ValueError(
                f"Exactly 7 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_delivery_worksheet(data):
    """
    Uppdate delivery worksheet
    """
    print("Updating delivery worksheet...\n")
    delivery_worksheet = SHEET.worksheet("delivery")
    delivery_worksheet.append_row(data)
    print("Delivery worksheet updated successfully\n")


def calculate_leftover_data(delivery_row):
    """
    Collecting figure of leftover  from the dispatched items in the
    last supply.
    """
    print("Calculating leftover data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    print(stock_row)


def main():
    """
    Run all program functions
    """
    data = get_delivery_data()
    delivery_data = [int(num) for num in data]
    update_delivery_worksheet(delivery_data)
    calculate_leftover_data(delivery_data)


print("Welcome to Fruit Shop Net")
main()
