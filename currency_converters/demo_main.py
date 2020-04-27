import asyncio
import os

from currency import Currency
from currency_converters import FreeCurrencyConverter, CurrencyConverter


def get_converter() -> CurrencyConverter:
    return FreeCurrencyConverter(os.environ['API_KEY'])


async def main():
    converter = get_converter()
    price = await converter.convert(Currency.EURO, Currency.MDL)
    print(price)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
