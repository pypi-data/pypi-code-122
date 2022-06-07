import requests
import aiohttp

url = 'https://browser.translate.yandex.net/api/v1/tr.json/translate'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
}


def translate(text: str, from_lang: str, to_lang: str, debug: bool = False) -> str:
    params = {
        'id': '1813dbffd7d74abc-1-0',
        'srv': 'yabrowser',
        'text': text,
        'lang': f'{from_lang}-{to_lang}',
        'format': 'html'
    }

    response = requests.get(url, params=params, headers=headers)
    if debug:
        print(response.text)
    return response.json().get('text')[0]


async def async_translate(text: str, from_lang: str, to_lang: str, debug: bool = False) -> str:
    params = {
        'id': '1813dbffd7d74abc-1-0',
        'srv': 'yabrowser',
        'text': text,
        'lang': f'{from_lang}-{to_lang}',
        'format': 'html'
    }

    connector = aiohttp.TCPConnector(ssl=False)
    session = aiohttp.ClientSession(connector=connector)

    response = await session.get(url, params=params, headers=headers)

    await connector.close()
    await session.close()

    if debug:
        print(await response.text())

    return (await response.json()).get('text')[0]
