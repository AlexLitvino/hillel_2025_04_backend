from enum import StrEnum
import os
from typing import Any

import requests

AV_API_KEY = os.getenv("AV_API_KEY")


class Currency(StrEnum):
    USD = 'USD'
    UAH = 'UAH'
    CHF = 'CHF'
    GBP = 'GBP'

BASE_CURRENCY = 'CHF' 

class APIError(Exception):
    pass


def get_currency_rate(from_: str, to: str):
    if from_ == to:
        return {'ask': 1.0, 'bid': 1.0}
    else:
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_}&to_currency={to}&apikey={AV_API_KEY}'
        r = requests.get(url).json()
        print(r)
        error = r.get('Error Message') or r.get('Information')
        if error:
            raise APIError(error)

        data = r['Realtime Currency Exchange Rate']
        return {'ask': float(data['9. Ask Price']), 'bid': float(data['8. Bid Price'])}


class Price:

    def __init__(self, value: float, currency: Currency):
        self.value: float =  value
        self.currency: Currency = currency

    def __add__(self, other: Any):
        if not isinstance(other, Price):
            raise RuntimeError('It is possible to add only instances of `Price` class')

        if self.currency == other.currency:
            return Price(self.value + other.value, self.currency)
        else:
            self_currency_rate = get_currency_rate(self.currency, BASE_CURRENCY)
            self_currency_rate_ask = self_currency_rate['ask']
            self_currency_rate_bid = self_currency_rate['bid']
            other_currency_rate_bid = get_currency_rate(other.currency, BASE_CURRENCY)['bid']

            self_value_chf = self.value * self_currency_rate_bid
            other_value_chf = other.value * other_currency_rate_bid
            return Price((self_value_chf + other_value_chf) / self_currency_rate_ask, self.currency)

    def __sub__(self, other: Any):
        if not isinstance(other, Price):
            raise RuntimeError('It is possible to subtract only instances of `Price` class')

        if self.currency == other.currency:
            return Price(self.value - other.value, self.currency)
        else:
            self_currency_rate = get_currency_rate(self.currency, BASE_CURRENCY)
            self_currency_rate_ask = self_currency_rate['ask']
            self_currency_rate_bid = self_currency_rate['bid']
            other_currency_rate_bid = get_currency_rate(other.currency, BASE_CURRENCY)['bid']

            self_value_chf = self.value * self_currency_rate_bid
            other_value_chf = other.value * other_currency_rate_bid
            return Price((self_value_chf - other_value_chf) / self_currency_rate_ask, self.currency)

    def __repr__(self):
        return f'Price(value={self.value}, currency={self.currency})'


if __name__ == '__main__':
    usd_100 = Price(100, Currency.USD)
    usd_150 = Price(150, Currency.USD)
    print(usd_100 + usd_150)  # 250 USD
    print(usd_150 - usd_100)  # 50 USD

    uah_1000 = Price(1000, Currency.UAH)
    print(usd_100 + uah_1000)

    chf_100 = Price(100, Currency.CHF)
    print(usd_100 + chf_100)
    print(chf_100 + usd_100)
