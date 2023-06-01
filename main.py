import requests
from datetime import datetime

from_currency = input("Enter from currency: ")
to_currency = input("Enter to currency: ")

queryparams = {
    "base_currency": from_currency,
    "currencies": to_currency
}

amount = float(input("Enter amount: "))

response = requests.get("https://api.currencyapi.com/v3/latest?apikey=JapF5njCxpvTiiGryKbthPDVvdrleyQjhUf1wNTK",params=queryparams)
json = response.json()

data = ()
rate = json["data"][queryparams["currencies"]]["value"]
converted = amount * rate
converted = float("{:.4f}".format(converted))

print("Rate is",rate)
print("Amount converted",converted)
