import json
import requests
import traceback

from app.constants import ApiUrls, ClientCredentials


def generate_access_token():
    """ This method is used to generate the Access Token"""

    try:
        payload = f'client_id={ClientCredentials.CLIENT_ID}&client_secret={ClientCredentials.CLIENT_SECRET}&grant_type=client_credentials&scope=buy%3Ainstant-bids%3Aread'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", ApiUrls.ACCESS_TOKEN, headers=headers, data=payload)

        if response.status_code == 200:
            data = json.loads(response.text)
            return data['access_token']
        else:
            raise Exception

    except Exception as e:
        print(f"[Access Token][Error] {e} -> {traceback.format_exc()}")
        return None


def get_instant_bid_response(access_token):
    """ This method is used to get the instant bid json """

    try:
        payload = f'bearer_token={access_token}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("GET", ApiUrls.INSTANT_BID_JSON, headers=headers, data=payload)

        if response.status_code == 200:
            return json.loads(response.text)

        elif response.status_code == 401:
            new_access_token = generate_access_token()
            return get_instant_bid_response(new_access_token)

        else:
            raise Exception

    except Exception as e:
        print(f"[Instant Bid API][Error] {e} -> {traceback.format_exc()}")
        return None
