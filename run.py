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
        print("Example: 25,30,30,15,11,17,20\n")

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


def update_worksheet(data, worksheet):
    """
    Receive list of integers to be inserted into a worksheet.
    Update relevant worksheet with the list provided.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet update successfully\n")


def calculate_leftover_data(delivery_row):
    """
    Collecting figure of leftover  from the dispatched items in the
    last supply.
    """
    print("Calculating leftover data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    leftover_data = []
    for stock, delivery in zip(stock_row, delivery_row):
        leftover = int(stock) - delivery
        leftover_data.append(leftover)

    return leftover_data


def get_last_3_entries_delivery():
    """
    Get columns of data from delivery worksheet, collecting the last 3
    entries for each fruit and returns the data as a list of lists.
    """
    delivery = SHEET.worksheet("delivery")

    columns = []
    for ind in range(1, 8):
        column = delivery.col_values(ind)
        columns.append(column[-3:])

    return columns


def calculate_stock_data(data):
    """
    Calculate average stock adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
  
    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_delivery_data()
    delivery_data = [int(num) for num in data]
    update_worksheet(delivery_data, "delivery")
    new_leftover_data = calculate_leftover_data(delivery_data)
    update_worksheet(new_leftover_data, "leftover")
    delivery_columns = get_last_3_entries_delivery()
    stock_data = calculate_stock_data(delivery_columns)
    update_worksheet(stock_data, "stock")


print("Welcome to Fruit Shop Net")
main()
