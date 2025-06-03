from enum import StrEnum
from typing import Any


class Currency(StrEnum):
    USD = 'USD'
    UAH = 'UAH'
    CHF = 'CHF'
    GBP = 'GBP'


converter = {
    Currency.USD: {'bid': 0.8451, 'ask': 0.8461},
    Currency.UAH: {'bid': 49.3, 'ask': 50.9},
    Currency.CHF: {'bid': 1.0, 'ask': 1.0}
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
            try:
                self_value_chf = self.value / converter[self.currency]['ask']
                other_value_chf = other.value / converter[other.currency]['ask']
                return Price((self_value_chf + other_value_chf) * converter[self.currency]['bid'], self.currency)
            except KeyError as e:
                raise RuntimeError(f"Currency {str(e).split(':')[1][2:-2]} is not supported by converter")

    def __sub__(self, other: Any):
        if not isinstance(other, Price):
            raise RuntimeError('It is possible to subtract only instances of `Price` class')

        if self.currency == other.currency:
            return Price(self.value - other.value, self.currency)
        else:
            try:
                self_value_chf = self.value / converter[self.currency]['ask']
                other_value_chf = other.value / converter[other.currency]['ask']
                return Price((self_value_chf - other_value_chf) * converter[self.currency]['bid'], self.currency)
            except KeyError as e:
                raise RuntimeError(f"Currency {str(e).split(':')[1][2:-2]} is not supported by converter")


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

    gbp_100 = Price(100, Currency.GBP)
    print(gbp_100 + gbp_100)
    # print(gbp_100 + usd_100)  # exception is expected
    # print(usd_100 + gbp_100)  # exception is expected
