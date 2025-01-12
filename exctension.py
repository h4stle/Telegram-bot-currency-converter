from config import keys
import requests
import json

class APIException(Exception):
    pass

class Convert:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException("Перевод в одну и ту же валюту невозможен")
        
        if base not in keys or quote not in keys:
            raise APIException("Валюта нераспознана")
        
        try:
            amount = float(amount)
        except:
            raise APIException("Некорректная сумма")
        
        if amount > 1000000000000000000:
            raise APIException("Сумма перевода превышает максимально допустимую")
        
        if amount < 0.01:
            raise APIException("Сумма перевода меньше минимально допустимой")
        
        r = requests.get(f'https://v6.exchangerate-api.com/v6/651e86be994ff176ebc888f1/pair/{base}/{quote}/{amount}')
        total = json.loads(r.content)["conversion_result"]

        return total
    