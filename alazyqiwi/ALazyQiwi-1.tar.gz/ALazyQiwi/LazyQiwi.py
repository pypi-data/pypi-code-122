from random import *
import time
import httpx
import asyncio
from .errors import *

class LazyQiwi(object):

    def __init__(self, token: str, phone: str = "", proxies: dict = None):

        """Changed SimpleQiwi library for qiwi farms

        Args
        ----
            token : str
            phone : str
            proxies : dict

        Important
        ---------
            Specify the proxy servers in the dict format => {"http": "http://...
        """

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        self.phone = phone
        self.proxies = proxies


    @property
    def _transaction_id(self) -> str:

        """Unical id generator
        
        Developed by Nodu$ iNC.
        -----------------------

        Returns
        -------
            UNIX time * randint(1000, 2000)
        """

        return str(int(time.time() * randint(1000, 2000)))

    @asyncio.coroutine
    async def account_balance(self) -> list:

        """
        Getting the balance from all accounts

        Developed by Nodu$ iNC.
        -----------------------

        Returns
        -------
            balance : list
        """

        balances = await self.get_balance()
        r = list()

        for i in balances:
            if i['balance'] is not None:
                r.append(i['balance']['amount'])

        return r

    
    async def get_balance(self) -> list:

        try:
            match self.proxies:
            
                case None:
                    
                    async with httpx.AsyncClient(headers=self.headers) as client:
                        
                        r = await client.get('https://edge.qiwi.com/funding-sources/v1/accounts/current')

                        if r is None:
                            raise InvalidTokenError("Invalid token used;")

                        json = r.json()
                        await client.aclose()
                case _:
                    async with httpx.AsyncClient(headers=self.headers, proxies=self.proxies) as client:
                        r = await client.get('https://edge.qiwi.com/funding-sources/v1/accounts/current')

                        if r is None:
                            raise InvalidTokenError("Invalid token used;")

                        json = r.json()
                        await client.aclose()
                    
        except Exception as e:
            raise InRequestError(e)

        if 'code' in json or 'errorCode' in json:
            raise APIError(json)

        balances = list()

        for account in json['accounts']:
            if account['hasBalance']:
                balances.append({
                    'type': account['type'],
                    'balance': account['balance']
                })

        return balances

    @asyncio.coroutine
    async def pay(self, account: str, amount: float, currency: str = '643', comment: str = None, tp: str = 'Account', acc_id: str = '643'):

        """
        Transfer money from an account to another qiwi account

        Args
        ----
            account : str // Transfer to number in qiwi system
            amount : float or int // Transfer amount
            currency : str // Transfer currency
            comment : str  // Transfer comment
            tp : str // Transfer type
            acc_id : str

        Developed by Nodu$ iNC.
        -----------------------

        Returns
        -------
            Server return

        """

        post_args = {
            "id": self._transaction_id,
            "sum": {
                "amount": amount,
                "currency": currency
            },
            "paymentMethod": {
                "type": tp,
                "accountId": acc_id
            },
            "fields": {
                "account": account
            }
        }

        if comment is not None:
            post_args["comment"] = comment

        try:
            match self.proxies:

                case None:
                    async with httpx.AsyncClient(headers=self.headers) as client:
                        response = await client.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments', json=post_args)
                        data = response.json()
                        await client.aclose()
                    
                
                case _:
                    async with httpx.AsyncClient(headers=self.headers, proxies=self.proxies) as client:
                        response = await client.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments', json=post_args)
                        data = response.json()
                        await client.aclose()
                        
        except Exception as e:
            raise InRequestError(e)        

        if 'code' in data or 'errorCode' in data:
            raise APIError(data)

        return data
