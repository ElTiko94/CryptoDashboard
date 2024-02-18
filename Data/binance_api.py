import hmac
import hashlib
import time
from urllib.parse import urlencode


def make_api_request(session, url_path, api_key, api_secret, payload={}):
    """
    Generic function for making API requests
    """
    response = send_signed_request('GET', url_path, session, api_key, api_secret, payload)

    if response.status_code == 200:
        return response.json()

    print("API request error:", response.status_code, response.json())
    return None

def get_server_time(session):
    response = session.get("https://api.binance.com/api/v1/time")
    if response.status_code == 200:
        return response.json()['serverTime']

    raise Exception("Could not get server time from Binance")

def get_timestamp(session):
    server_time = get_server_time(session)
    local_time = int(time.time() * 1000)
    time_offset = local_time - server_time
    return local_time - time_offset

def create_signature(query_string, api_secret):
    return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def send_signed_request(http_method, url_path, session, api_key, api_secret,payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp(session))
    else:
        query_string = 'timestamp={}'.format(get_timestamp(session))

    signature = create_signature(query_string, api_secret)
    url = f'https://api.binance.com{url_path}?{query_string}&signature={signature}'

    headers = {
        'X-MBX-APIKEY': api_key
    }

    return session.get(url, headers=headers) if http_method == 'GET' else None
