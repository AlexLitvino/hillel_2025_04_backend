from enum import StrEnum
from typing import Any


class Currency(StrEnum):
    USD = 'USD'
    UAH = 'UAH'
    CHF = 'CHF'


converter = {
    Currency.USD: {'bid': 0.8451, 'ask': 0.8461},
    Currency.UAH: {'bid': 49.3, 'ask': 50.9}
}


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
            self_value_chf = self.value / converter[self.currency]['ask']
            other_value_chf = other.value / converter[other.currency]['ask']
            return Price((self_value_chf + other_value_chf) * converter[self.currency]['bid'], self.currency)

    def __sub__(self, other: Any):
        if not isinstance(other, Price):
            raise RuntimeError('It is possible to subtract only instances of `Price` class')

        if self.currency == other.currency:
            return Price(self.value - other.value, self.currency)
        else:
            self_value_chf = self.value / converter[self.currency]['ask']
            other_value_chf = other.value / converter[other.currency]['ask']
            return Price((self_value_chf - other_value_chf) * converter[self.currency]['bid'], self.currency)


    def __repr__(self):
        return f'Price(value={self.value}, currency={self.currency})'


if __name__ == '__main__':
    usd_100 = Price(100, Currency.USD)
    usd_150 = Price(150, Currency.USD)
    print(usd_100 + usd_150)  # 250 USD
    print(usd_150 - usd_100)  # 50 USD

    uah_1000 = Price(1000, Currency.UAH)
    print(usd_100 + uah_1000)