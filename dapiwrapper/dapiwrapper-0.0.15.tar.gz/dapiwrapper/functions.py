import requests

def get_token_balance():

    return 0

def get_token_balances_for_user(key, user, token, network, rpc_url=None):

    return 1

def get_token_balance_for_users(key, users : list, token, network, rpc_url=None):
    url = "https://test-api.dcentralab.com/tokenBalanceForUsers"
    headers = { 'X-API-KEY': key }
    data = {
        "network": network,
        "users": users,
        "token": token,
        "rpc": rpc_url
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def calculate_reserves_amount_from_pair():
    return 3

def get_reserves_from_pair():
    return 4

def calculate_token_price_from_pair():
    return 5