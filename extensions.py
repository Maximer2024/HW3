import requests
import json


class APIException(Exception):
    pass


class Converter:
    currency_codes = {
        "доллар": "USD",
        "евро": "EUR",
        "рубль": "RUB",
    }

    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base = Converter.currency_codes.get(base.lower(), base.upper())
        quote = Converter.currency_codes.get(quote.lower(), quote.upper())

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        if base == quote:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}.")

        url = f"https://v6.exchangerate-api.com/v6/08b9005ec950ddbd4d9a4ef2/latest/{base}"
        response = requests.get(url)

        if response.status_code != 200:
            raise APIException("Ошибка запроса к API.")

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise APIException("Ошибка обработки ответа от API: неверный формат JSON.")

        if 'conversion_rates' not in data:
            raise APIException("Отсутствует ключ 'conversion_rates' в ответе API.")

        rates = data['conversion_rates']
        if quote not in rates:
            raise APIException(f"Валюта {quote} не найдена в API.")

        quote_rate = rates[quote]
        total_quote = quote_rate * amount
        return total_quote
