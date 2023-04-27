import json
import re
import openpyxl
import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

green_sheets = []

def get_crypto_prices(symbols, api_key):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {'symbol': ','.join(symbols)}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None

    prices = {}
    for symbol in symbols:
        prices[symbol] = data["data"][symbol]["quote"]["USD"]["price"]

    return prices

def update_excel_file(file_name, token_prices):
    excel_file = openpyxl.load_workbook(file_name)

    # Update Star Atlas number of Stacking days
    sheet = excel_file['ATLAS']
    cell = sheet.cell(row=2, column=8)  # H2
    cell.value = int((today - starAtlasJ0).days)

    # Update Tokens prices
    for token, price in token_prices.items():
        sheet = excel_file[str(token)]
        cell = sheet.cell(row=3, column=10)  # J3
        cell.value = float(price)

   # Check for green color in column O for every sheet
    for sheet_name in excel_file.sheetnames:
        sheet = excel_file[sheet_name]
        for row in sheet.iter_rows(min_row=4, max_col=15, max_row=sheet.max_row):
            if row[14].fill.start_color.index == 'FF00FF00':  # Check if color is green
                green_sheets.append((sheet_name, row[14].row))  # Append tuple of sheet name and row number


    # Save changes
    excel_file.save(file_name)

today = datetime.datetime.now()
starAtlasJ0 = datetime.datetime(2021, 12, 17)
file_name = "C:/Users/Tiko/Desktop/Tiko/investissement/Gestion de crypto/Data/Historique d'achats.xlsx"
api_key = '33921097-6bb4-45e6-89a4-52591f85703b'

tokens = ['BTC', 'ETH', 'ATLAS', 'POLIS', 'LUNC', 'LUNA', 'SOL', 'BNB', 'MATIC', 'ATOM', 'EGLD', 'NEAR', 'GRT', 'AMP',
          'SHPING', 'XRP', 'DOT', 'LTC', 'TRX', 'ADA', 'ALGO', 'APE', 'AVAX', 'KAVA', 'DOGE', 'UNI', 'LINK', 'LDO',
          'ICP', 'SHIB', 'MINA']

token_prices = get_crypto_prices(tokens, api_key)

if token_prices is not None:
    update_excel_file(file_name, token_prices)