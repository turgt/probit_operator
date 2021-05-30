import sys
import requests
import time
import base64

from requests.api import get, head


def get_token():
    client_id = API_KEY
    client_secret = SECRET_KEY
    print(client_id + "-----------" + client_secret)
    encodedData = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")
    url = "https://accounts.probit.com/token"

    payload = {"grant_type": "client_credentials"}
    headers = {
        "Accept": "application/json",
        "Authorization": "Basic " + encodedData,
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return response.json()['access_token']


def get_ticker(symbol):

    url = "https://api.probit.com/api/exchange/v1/ticker"

    querystring = {"market_ids": symbol}

    headers = {"Accept": "application/json"}

    r = requests.request("GET", url, headers=headers, params=querystring)

    print(r.json())
    return r.json()



def place_order(symbol, price, quantity, trade_type, order_type):
    url = "https://api.probit.com/api/exchange/v1/new_order"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + get_token()
    }
    payload = {
    "market_id": symbol,
    "type": order_type,
    "side": trade_type,
    "time_in_force": "gtc",
    "limit_price": str(float("{:.7f}".format(price))),
    "quantity": str(int(quantity))
    }
    r = requests.request('POST', url, headers=headers, json=payload)
    print(headers)
    print(payload)
    return r


if __name__ == '__main__':
    global API_KEY
    global SECRET_KEY

    API_KEY = sys.argv[1]
    SECRET_KEY = sys.argv[2]
    USDT = int(sys.argv[3])
    rate = int(sys.argv[4])
    multipler = float(sys.argv[5])
    sleep = int(sys.argv[6])
    symbol = sys.argv[7]

    #API_KEY = '9b2ce8d510893866'
    #SECRET_KEY = '49782f77f0f44ed97d8f2e87b7b7c36c'
    #USDT = 5
    #rate = 10
    #multipler = float(1.2)
    #sleep = int(2)
    #symbol = 'hot'
    
    
    symbol = symbol.upper()+"-USDT"

    y = get_ticker(symbol)
    order = float(y['data'][0]['last']) * (rate + 100) * 0.01
    count = USDT / order

    res = place_order(symbol, order, count, 'buy', 'limit')
    print(res.json())

    if res.status_code == 200:
        print("Placed Buy\n")
        if sleep != 0:
            time.sleep(sleep)
        print(str(order) + "----------" + str(order*multipler))
        res = place_order(symbol, order * multipler, count - (count * 0.03 / 100), 'sell', 'limit')
        print(res.json())
        if res.status_code == 200:
            print("\nPlaced Sell\n")