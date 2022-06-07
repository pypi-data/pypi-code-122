import json
from urllib import response
import requests

class Authentication():
    def getToken():
        url = "https://localhost:44350/connect/token"
        payload='client_id=makana_api&grant_type=client_credentials&scope=makanaapp_api&client_secret=TAxhx@9tH(l^MgQ9FWE8}T@NWUT9U)'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response =  requests.post(url, headers=headers, data=payload, verify=False)
        auth_response_json = response.json()
        auth_token = auth_response_json["access_token"]
        auth_token_header_value = "Bearer %s" % auth_token
        return auth_token_header_value
    
    def getRequest(url: str):
        access_token_header = Authentication.getToken()
        headers = {
            'Authorization': access_token_header,
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers, verify=False)
        return response
    
    def postRequest(url: str, data, files= None):
        access_token_header = Authentication.getToken()
        headers = {
            'Authorization': access_token_header,
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data= data, files=files, verify=False)
        return response