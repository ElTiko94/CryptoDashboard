import hmac
import os
import json
import hashlib
import time
from urllib.parse import urlencode


def get_server_time(session):
    response = session.get("https://api.binance.com/api/v1/time")
    if response.status_code == 200:
        return response.json()['serverTime']
    else:
        raise Exception("Could not get server time from Binance")

def get_timestamp(session):
    server_time = get_server_time(session)
    local_time = int(time.time() * 1000)
    time_offset = local_time - server_time
    return local_time - time_offset

def create_signature(query_string, api_secret):
    return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def send_signed_request(http_method, url_path, session, API_KEY, API_SECRET,payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp(session))
    else:
        query_string = 'timestamp={}'.format(get_timestamp(session))

    signature = create_signature(query_string, API_SECRET)
    url = f'https://api.binance.com{url_path}?{query_string}&signature={signature}'

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    return session.get(url, headers=headers) if http_method == 'GET' else None

def get_cumulative_total_rewards(session, API_KEY, API_SECRET):
    url_path = '/sapi/v1/simple-earn/flexible/position'
    cumulative_rewards = {}
    current_page = 1
    has_more = True

    while has_more:
        payload = {
            'size': 100,  # Set size to maximum (100) as per Binance API specification
            'current': current_page,  # Page number, starting from 1
        }
        response = send_signed_request('GET', url_path, session, API_KEY, API_SECRET, payload)

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
    