from typing import Dict
from datetime import datetime

import requests
import json

from currency import Currency
from secrets import API_KEY

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
API_LINK = "https://free.currconv.com/api/v7/"


def get_price_from_API_for(currency: Currency) -> float:
    api_response = requests.get(
        API_LINK + "convert?q=" + currency.value + "_MDL&compact=ultra&apiKey=" + API_KEY,
        headers=HEADERS)

    try:
        currency_resp = json.loads(api_response.content)
        return round(currency_resp[currency.value + "_MDL"], 2)
    except():
        raise ConnectionError


def get_all_prices_from_API() -> Dict[Currency, float]:
    curr_prices = {Currency.EURO: 0, Currency.US_DOLLAR: 0}

    api_response = requests.get(
        API_LINK + "convert?q=USD_MDL,EUR_MDL&compact=ultra&apiKey=" + API_KEY,
        headers=HEADERS)

    try:
        currency_resp = json.loads(api_response.content)
        curr_prices[Currency.EURO] = round(currency_resp[Currency.EURO.value + "_MDL"], 2)
        curr_prices[Currency.US_DOLLAR] = round(currency_resp[Currency.US_DOLLAR.value + "_MDL"], 2)
        return curr_prices
    except():
        raise ConnectionError


def get_all_prices_from_API_for_date(search_date: datetime) -> Dict[Currency, float]:
    curr_prices = {Currency.EURO: 0, Currency.US_DOLLAR: 0}
    formated_date = search_date.strftime("%Y-%m-%d")

    api_response = requests.get(
        API_LINK + "convert?q=USD_MDL,EUR_MDL&date=" + formated_date + "&compact=ultra&apiKey=" + API_KEY,
        headers=HEADERS)

    try:
        currency_resp = json.loads(api_response.content)
        curr_prices[Currency.EURO] = round(currency_resp[Currency.EURO.value + "_MDL"][formated_date], 2)
        curr_prices[Currency.US_DOLLAR] = round(currency_resp[Currency.US_DOLLAR.value + "_MDL"][formated_date], 2)
        return curr_prices
    except():
        raise ConnectionError
