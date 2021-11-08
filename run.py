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
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figure input from the user
    """

    while True:
        print("Please enter sales data from last market.")
        print("Data should be six numbers separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n")
        print(f'The data provided is {data_str}')

        sales_data = data_str.split(',')
        
        if validate_data(sales_data):
            print('Data is valid!')
            break
    return sales_data
    


def validate_data(values):
    """
    inside the try, converts data string to integers. 
    If the data cannot be converted to an integer, 
    or there are more than 6 values, 
    this function will return an error.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required. You provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False
    
    return True

def update_worksheet(data, worksheet):
    """
    Accepts datat and updates corresponding worksheet
    """

    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated succesfully.\n')

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus

    Surplus is defined as the sales subtracted from the stock
    -negative surplus indicates extra made when stock runs out
    -positive indicates waste
    """

    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def get_last_5_entries():
    """
    Collects collumns of data from sales worksheet, 
    collecting the last 5 entries for each sandwich 
    and returning them as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    collumns = []
    for ind in range(1, 7):
        collumn = sales.col_values(ind)
        collumns.append(collumn[-5:])
    return collumns 

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """

    print("Calculating stock data...\n")
    new_stock_data = []

    for collumn in data:
        int_collumn = [int(num) for num in collumn]
        average = sum(int_collumn) / len(int_collumn)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data


def main():
    """
    Run all program functions
    """

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_collumns = get_last_5_entries()
    stock_data = calculate_stock_data(sales_collumns)
    update_worksheet(stock_data, "stock")

print("Welcome to love sandwiches data automation! ")
main()
