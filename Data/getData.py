import json
import re
import openpyxl
import datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from get_cumulative_total_rewards import get_cumulative_total_rewards


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

def update_excel_file(file_name, token_prices,rewards):
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
        if token in rewards:
            cell = getYellowCells(sheet)
            sheet.cell(row=cell[0][0], column=cell[0][1]).value = float(rewards[token])


    # Save changes
    excel_file.save(file_name)

def getYellowCells(sheet, column_letter='B'):
    yellow_cells = []

    # Iterate through each cell in the specified column
    for row in sheet[column_letter]:
        if row.fill.start_color.index == 'FFFFFF00':  # Yellow fill color in hex
            yellow_cells.append((row.row, row.column))
            break

    return yellow_cells

def getGreenCells(sheet, column_letter='B'):
    Green_cells = []

    # Iterate through each cell in the specified column
    for row in sheet[column_letter]:
        if row.fill.start_color.index == 'FFFFFF00':  # Yellow fill color in hex
            Green_cells.append((row.row, row.column))
            break

    return Green_cells

today = datetime.datetime.now()
starAtlasJ0 = datetime.datetime(2021, 12, 17)
file_name = r"C:\Users\Tiko\Desktop\Tiko\investissement\Gestion de crypto\Data\Historique d'achats.xlsx"
api_key = '33921097-6bb4-45e6-89a4-52591f85703b'

tokens = ['BTC', 'ETH', 'ATLAS', 'POLIS', 'LUNC', 'LUNA', 'SOL', 'BNB', 'MATIC', 'ATOM', 'EGLD', 'NEAR', 'GRT', 'AMP',
          'SHPING', 'XRP', 'DOT', 'LTC', 'TRX', 'ADA', 'ALGO', 'APE', 'AVAX', 'KAVA', 'DOGE', 'UNI', 'LINK', 'LDO',
          'ICP', 'SHIB', 'MINA']

token_prices = get_crypto_prices(tokens, api_key)

rewards = get_cumulative_total_rewards()
if token_prices is not None:
    update_excel_file(file_name, token_prices, rewards )