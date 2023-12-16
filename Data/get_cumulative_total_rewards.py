import requests
import hmac
import json
import hashlib
import time
from urllib.parse import urlencode

json_path = os.path.join(os.environ.get('crypto_path'), 'Data/config.json')

with open(json_path, 'r') as config_file:
    config = json.load(config_file)

API_KEY = config['binance_api_key']
API_SECRET = config['binance_api_secret']

def get_server_time():
    response = requests.get("https://api.binance.com/api/v1/time")
    if response.status_code == 200:
        return response.json()['serverTime']
    else:
        raise Exception("Could not get server time from Binance")

def get_timestamp():
    server_time = get_server_time()
    local_time = int(time.time() * 1000)
    time_offset = local_time - server_time
    return local_time - time_offset

def create_signature(query_string, api_secret):
    return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = 'timestamp={}'.format(get_timestamp())

    signature = create_signature(query_string, API_SECRET)
    url = f'https://api.binance.com{url_path}?{query_string}&signature={signature}'

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.get(url, headers=headers) if http_method == 'GET' else None
    return response

def get_cumulative_total_rewards():
    url_path = '/sapi/v1/simple-earn/flexible/position'
    cumulative_rewards = {}
    current_page = 1
    has_more = True

    while has_more:
        payload = {
            'size': 100,  # Set size to maximum (100) as per Binance API specification
            'current': current_page,  # Page number, starting from 1
        }
        response = send_signed_request('GET', url_path, payload)

        if response.status_code == 200:
            data = response.json()
            rows = data.get('rows', [])
            for row in rows:
                asset = row.get('asset')
                cumulative_rewards[asset] = row.get('cumulativeTotalRewards')
            # Check if there are more pages to fetch
            has_more = len(rows) == 100
            current_page += 1
        else:
            print("Error:", response.status_code)
            print(response.json())
            break
    
    return cumulative_rewards


