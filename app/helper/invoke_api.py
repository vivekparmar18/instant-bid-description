import json
import requests
import traceback

from app.constants import ApiUrls, ClientCredentials


class InvokeAPI:

    def __init__(self):
        self.access_token = None

    def __generate_access_token(self):
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

    def __get_instant_bid_response(self, access_token, instant_bid_id):
        """ This method is used to get the instant bid json """

        try:
            payload = {}
            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            instant_bid_api_url = ApiUrls.INSTANT_BID_JSON.format(instant_bid_id=instant_bid_id)
            response = requests.request("GET", instant_bid_api_url, headers=headers, data=payload)

            if response.status_code == 200:
                return json.loads(response.text)

            elif response.status_code == 401:
                self.access_token = self.__generate_access_token()
                return self.__get_instant_bid_response(self.access_token, instant_bid_id)

            else:
                raise Exception

        except Exception as e:
            print(f"[Instant Bid API][Error] {e} -> {traceback.format_exc()}")
            return None

    def invoke_instant_bid_api(self, instant_bid_id):
        self.access_token = self.__generate_access_token()
        api_response = self.__get_instant_bid_response(self.access_token, instant_bid_id)
        return api_response
