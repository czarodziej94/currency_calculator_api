import requests


def fetch_exchange_sell_rate(currency: str, date: str):
    url = f"http://api.nbp.pl/api/exchangerates/rates/c/{currency}/{date}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        rate = data['rates'][0]['ask']
        return {'sell': rate}
    else:
        return None


def fetch_exchange_mid_rate(currency: str, date: str):
    url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date}/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        rate = data['rates'][0]['mid']
        return {'mid': rate}
    else:
        return None
