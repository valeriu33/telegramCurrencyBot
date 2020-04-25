from currency import Currency


class CurrencyConverter:
    async def convert(self, from_currency: Currency, to_currency: Currency) -> float:
        raise NotImplementedError()
