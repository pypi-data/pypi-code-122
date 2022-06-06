"""
Copyright (c) 2022 Ben

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .exceptions import RequestException
from .models import Anime, FullAnime
import aiohttp
from typing import Optional


class AioJikan:
    """
    Class for interacting with the jikan api
    """

    def __init__(self, session: aiohttp.ClientSession = None, api_url: str = None) -> None:
        """
        Aiojikan innit "insert british joke here"
        """
        self.session = session if session else aiohttp.ClientSession()
        self.API_URL: str = api_url if api_url else "https://api.jikan.moe/v4"

    async def close(self) -> None:
        """
        Call this to close your session and if aiojikan ever needs this in the future, it's readily available
        """
        await self.session.close()

    async def _request(self, url: str) -> Optional[aiohttp.ClientResponse]:
        """
        Request a api endpoint

        Parameters
        ----------
        url: str
            The url to request

        Raises
        ------
        RequestException
            Raised when the request fails to return a 200

        Returns
        -------
        aiohttp.ClientResponse
            The request
        """
        request = await self.session.get(f"{self.API_URL}{url}")
        if request.status != 200:
            raise RequestException(request.status, await request.json())
        else:
            return request

    async def get_anime(self, mal_id: int) -> Anime:
        """
        Get an anime by it's MyAnimeList ID

        Parameters
        ----------
        id: int
            The MAL ID"""
        request = await self._request(f"/anime/{str(mal_id)}")
        anime = Anime((await request.json()).get("data"))
        return anime

    async def get_full_anime(self, mal_id: int) -> FullAnime:
        """
        Get the full animes info by it's MyAnimeList ID

        Parameters
        ----------
        mal_id: int
        """
        request = await self._request(f"/anime/{str(mal_id)}/full")
        fullanime = FullAnime((await request.json()).get("data"))
        return fullanime
