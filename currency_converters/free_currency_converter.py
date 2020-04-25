import ssl
from urllib.parse import urlencode

import aiohttp

from currency import Currency
from .currency_converter import CurrencyConverter


class FreeCurrencyConverter(CurrencyConverter):
    _API_URL = "https://free.currconv.com/api/v7/convert"

    def __init__(self, api_key: str):
        self._api_key = api_key

    async def convert(self, from_currency: Currency, to_currency: Currency) -> float:
        currency_key = f'{from_currency.value}_{to_currency.value}'
        query_params = {'q': currency_key, 'compact': 'ultra'}

        json_response = await self._api_request(query_params)
        return round(json_response[currency_key], 2)

    async def _api_request(self, query_parameters: dict) -> dict:
        query_parameters['apiKey'] = self._api_key
        query = urlencode(query_parameters)
        url = f'{self._API_URL}?{query}'

        async with aiohttp.ClientSession() as session:
            response = await session.get(url, ssl=ssl.SSLContext())
            return await response.json()



