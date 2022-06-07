import requests

def get_token_balance(key, user, token, network, rpc_url=None):
    url = "https://test-api.dcentralab.com/tokenBalance"
    headers = { 'X-API-KEY': key }
    data = {
        "network": network,
        "user": user,
        "token": token,
        "rpc_url": rpc_url
    }
    response = requests.get(url, json=data, headers=headers)
    return response.json()

    return 0

def get_token_balances_for_user(key, user, tokens : list, network, rpc_url=None):
    url = "https://test-api.dcentralab.com/tokenBalancesForUser"
    headers = { 'X-API-KEY': key }
    data = {
        "network": network,
        "user": user,
        "tokens": tokens,
        "rpc_url": rpc_url
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def get_token_balance_for_users(key, users : list, token, network, rpc_url=None):
    url = "https://test-api.dcentralab.com/tokenBalanceForUsers"
    headers = { 'X-API-KEY': key }
    data = {
        "network": network,
        "users": users,
        "token": token,
        "rpc_url": rpc_url
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def calculate_reserves_amount_from_pair(key, pool, amount, network, rpc_url=None):
    url = "https://test-api.dcentralab.com/calculateReservesAmountsFromPair"
    headers = { 'X-API-KEY': key }
    data = {
        "network": network,
        "pool": pool,
        "amount": amount,
        "rpc_url": rpc_url
    }
    response = requests.get(url, json=data, headers=headers)
    return response.json()

def get_reserves_from_pair(key, pool, network, rpc_url=None):
    url = "https://test-api.dcentralab.com/getReservesFromPair"
    headers = { 'X-API-KEY': key }
    data = {
        "network": network,
        "pool": pool,
        "rpc_url": rpc_url
    }
    response = requests.get(url, json=data, headers=headers)
    return response.json()

def calculate_token_price_from_pair():
    return 5