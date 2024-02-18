"""
Module: binance_api
This module provides a class BinanceApi for interacting with the Binance API
for managing lending and earning features.
"""

import hmac
import hashlib
import time
from urllib.parse import urlencode

class BinanceApi :
    """
    Class for interacting with the Binance API for managing lending and earning features.

    Args:
        api_key (str): The API key provided by Binance.
        api_secret (str): The API secret provided by Binance.
        session: The session object used for making HTTP requests.

    Attributes:
        api_key (str): The API key provided by Binance.
        api_secret (str): The API secret provided by Binance.
        session: The session object used for making HTTP requests.

    Methods:
        make_api_request: Generic function for making API requests.
        get_server_time: Retrieves the server time from the Binance API.
        get_timestamp: Calculates the current timestamp adjusted for the time offset.
        create_signature: Creates a signature for the request using HMAC-SHA256 encryption.
        send_signed_request: Sends a signed request to the specified URL path.
        get_plans_id: Fetches a list of plan IDs for auto-investment from Binance lending.
        get_plan_details: Retrieves details of a specific auto-investment plan by ID.
        get_auto_invest: Fetches details of all auto-investment plans.
        get_cumulative_total_rewards: Retrieves cumulative total rewards for flexible positions.
    """
    def __init__(self, api_key, api_secret, session):
        """
        Initialize the BinanceApi object with the provided API key,
        API secret, and a session object for making HTTP requests
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = session

    def make_api_request(self, url_path, payload={}):
        """
        Generic function for making API requests
        """
        response = self.send_signed_request('GET', url_path, payload)

        if response.status_code == 200:
            return response.json()

        print("API request error:", response.status_code, response.json())
        return None

    def get_server_time(self):
        """
        Retrieve the server time from the Binance API
        """
        response = self.session.get("https://api.binance.com/api/v1/time")
        if response.status_code == 200:
            return response.json()['serverTime']

        raise Exception("Could not get server time from Binance")

    def get_timestamp(self):
        """
        Calculate the current timestamp adjusted for the time offset
        between the local machine and the Binance server.
        """
        server_time = self.get_server_time()
        local_time = int(time.time() * 1000)
        time_offset = local_time - server_time
        return local_time - time_offset

    def create_signature(self, query_str):
        """
        Create a signature for the request using HMAC-SHA256 encryption with the API secret.
        """
        return hmac.new(self.api_secret.encode('utf-8'), query_str.encode('utf-8'), hashlib.sha256).hexdigest()

    def send_signed_request(self, http_method, url_path, payload={}):
        """
        Send a signed request to the specified URL path with optional payload data.
        """
        query_string = urlencode(payload, True)
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = 'timestamp={}'.format(self.get_timestamp())

        signature = self.create_signature(query_string)
        url = f'https://api.binance.com{url_path}?{query_string}&signature={signature}'

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        return self.session.get(url, headers=headers) if http_method == 'GET' else None

    def get_plans_id(self):
        """
        Fetch a list of plan IDs for auto-investment from Binance
        """
        url_path = '/sapi/v1/lending/auto-invest/plan/list'
        response_data = self.make_api_request(url_path, {'size': 100})

        if response_data and 'plans' in response_data:
            return [plan['planId'] for plan in response_data['plans']]

        return []

    def get_plan_details(self, plan_id):
        """
        Retrieve details of a specific auto-investment plan by ID.
        """
        url_path = '/sapi/v1/lending/auto-invest/plan/id'
        response_data = self.make_api_request(url_path, {'size': 100, 'planId': plan_id})

        if response_data:
            return response_data

        return {}

    def get_auto_invest(self, plan_id_to_name):
        """
        Fetch details of all auto-investment plans and organizes them into a list of dictionaries.
        """
        plan_ids = self.get_plans_id()
        plans = []
        for plan_id in plan_ids:
            plan_details = self.get_plan_details(plan_id)
            plan = {"planId": plan_id_to_name[str(plan_id)], "details": []}

            for detail in plan_details.get("details", []):
                plan["details"].append({
                    "targetAsset": detail["targetAsset"],
                    "totalInvestedInUSD": detail["totalInvestedInUSD"],
                    "purchasedAmount": detail["purchasedAmount"]
                })
            plans.append(plan)

        return plans

    def get_cumulative_total_rewards(self):
        """
        Retrieves cumulative total rewards for flexible positions in the Binance Earn program.
        """
        url_path = '/sapi/v1/simple-earn/flexible/position'
        cumulative_rewards = {}
        current_page = 1
        has_more = True

        while has_more:

            data = self.make_api_request(url_path, {'size': 100, 'current': current_page})

            if data is not None:
                rows = data.get('rows', [])
                for row in rows:
                    asset = row.get('asset')
                    cumulative_rewards[asset] = row.get('cumulativeTotalRewards')
                # Check if there are more pages to fetch
                has_more = len(rows) == 100
                current_page += 1
            else:
                print("Error:",data)
                break

        return cumulative_rewards
