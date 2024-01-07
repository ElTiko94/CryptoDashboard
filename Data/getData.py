import json
import os
import openpyxl
import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from get_cumulative_total_rewards import get_cumulative_total_rewards
from get_auto_invest_amount import get_auto_invest_amount
import xlwings as xw
import subprocess


green_sheets = []

def get_crypto_prices(symbols, api_key, session):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {'symbol': ','.join(symbols)}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}

    # Update the session headers for this request
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        if data.get('status', {}).get('error_code') != 0:
            print(f"Error in API response: {data.get('status', {}).get('error_message')}")
            return None
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None

    prices = {}
    for symbol in symbols:
        # Ensure the symbol exists in the response data
        if symbol in data.get("data", {}):
            prices[symbol] = data["data"][symbol]["quote"]["USD"]["price"]
        else:
            print(f"Price data for {symbol} not found in response.")

    return prices

def update_excel_file(file_name, token_prices,rewards, auto_invest):
    excel_file = openpyxl.load_workbook(file_name)

    # Update Star Atlas number of Stacking days
    sheet = excel_file['ATLAS']
    cell = sheet.cell(row=2, column=8)  # H2
    cell.value = int((today - starAtlasJ0).days)

    app = xw.App(visible=False)
    book = app.books.open(file_name)
    
    for token, price in token_prices.items():
        sheet = excel_file[str(token)]
        cell = sheet.cell(row=3, column=10)  # J3
        # Update Tokens prices
        cell.value = float(price)

        sheet_xw = book.sheets[token]

        if token in rewards:
            cell = getYellowCells(sheet)
            print_valid_transactions(sheet_xw, price, token)
            sheet.cell(row=cell[0][0], column=cell[0][1]).value = float(rewards[token])
    
    book.close()
    app.quit()

    for plan in auto_invest:
        for detail in plan["details"]:
            sheet = excel_file[str(detail['targetAsset'])]
            cell_row = getDCACell(sheet, plan['planId'])
            sheet.cell(row=cell_row, column=2).value = float(detail['purchasedAmount'])
            sheet.cell(row=cell_row, column=4).value = float(detail['totalInvestedInUSD'])

    # Save changes
    excel_file.save(file_name)



def print_valid_transactions(sheet, token_price, token):
    row = 3
    price_cell_value = sheet.range(f'O{row}').value

    print(f'token : {token} price : {float(token_price)}$')
    if price_cell_value is not None and float(price_cell_value) > float(token_price):
        print(f"   Buy {sheet.range(f'N{row}').value} of {token} for {sheet.range(f'P{row}').value}$")

    if token != 'ETH' and token != 'BTC' : 
        for row in range(6, 200):
            price_cell_value = sheet.range(f'O{row}').value
            status_cell_value = sheet.range(f'Q{row}').value

            if price_cell_value is not None and price_cell_value!= "Token Price" and status_cell_value != "Done":
                if float(price_cell_value) < float(token_price) and token != "SHIB":
                    print(f"   Sell {sheet.range(f'N{row}').value} of {token} for {sheet.range(f'P{row}').value}$ ")
                elif (token == "SHIB") :
                    if float(sheet.range(f'P{row}').value)/sheet.range(f'N{row}').value < float(token_price):
                        print(f"   Sell {sheet.range(f'N{row}').value} of {token} for {sheet.range(f'P{row}').value}$ ")


def getDCACell(sheet, planId, column_letter='E'):
    for row in sheet[column_letter]:
        if row.value == planId:
            return row.row
    return None

def getYellowCells(sheet, column_letter='B'):
    yellow_cells = []

    # Iterate through each cell in the specified column
    for row in sheet[column_letter]:
        if row.fill.start_color.index == 'FFFFFF00':  # Yellow fill color in hex
            yellow_cells.append((row.row, row.column))
            break

    return yellow_cells


today = datetime.datetime.now()
starAtlasJ0 = datetime.datetime(2021, 12, 17)

crypto_path = os.environ.get('crypto_path')
file_name = os.path.join(crypto_path, "Data/Historique d'achats.xlsx")

json_path = os.path.join(crypto_path, 'Data/config.json')

with open(json_path, 'r') as config_file:
    config = json.load(config_file)

coinmarketcap_api_key = config['coinmarketcap_api_key']
binance_api_key = config['binance_api_key']
binance_api_secret = config['binance_api_secret']

tokens = ['BTC', 'ETH', 'SOL', 'ATLAS', 'BNB', 'POLIS', 'LUNC', 'LUNA', 'MATIC', 'ATOM', 'EGLD', 'NEAR', 'GRT', 'AMP',
          'SHPING', 'XRP', 'DOT', 'LTC', 'TRX', 'ADA', 'ALGO', 'APE', 'AVAX', 'KAVA', 'DOGE', 'UNI', 'LINK', 'LDO',
          'ICP', 'SHIB', 'MINA', 'SEI','MEME','ACE','DYDX','TIA']


# Create a session object
session = Session()

# Pass this session object to your functions
token_prices = get_crypto_prices(tokens, coinmarketcap_api_key, session)


rewards = get_cumulative_total_rewards(session)
auto_invest = get_auto_invest_amount(session)
if token_prices is not None:
    update_excel_file(file_name, token_prices, rewards, auto_invest )


# Path to your bash script
batch_script = os.path.join(crypto_path, 'Data/Open_excel.bat')

# Run the script
subprocess.run([batch_script], shell=True)

input("Press Enter to close the Excel workbook...")
