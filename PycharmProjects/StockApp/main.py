from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import json


def getJSONAsString(symbol):
    url = urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol +
                  '&outputsize=full&apikey=KIH6VFJ03Z89T5DI')
    str_response = url.read()
    if b"Invalid" in str_response:
        print("Invalid API call!")
        exit(1)
    else:
        return str_response

def sharesKnown(shares, last_price):
    value = last_price*shares
    return value

def sharesNotKnown(purchase_cost, purchase_date, last_price, jsonAsString):
    try:
        shares = float(purchase_cost) / float(jsonAsString['Time Series (Daily)'][purchase_date]['4. close'])
    except KeyError:
        print('Hmm, there\'s no data for that date. It\'s possible the market was closed on that day due to a holid'
              'ay. Please try again!')
        exit(1)
    value = last_price * shares
    return value

try:
    symbol = input('Please enter symbol name: ')
    str_response = getJSONAsString(symbol)
    result = json.loads(str_response)
    last_updated = result['Meta Data']['3. Last Refreshed']
    last_price = float(result['Time Series (Daily)'][last_updated]['4. close'])

    answer = input('Do you know how many shares you purchased? Enter "Y" or "N": ')

    if answer.lower() == 'y':
        shares = float(input('Please enter number of shares: '))
        value = sharesKnown(shares, last_price)
    elif answer.lower() == 'n':
        purchase_cost = float(input('If you don\'t know how many shares you purchased, enter your total stock purchase '
                                     'cost: $'))
        purchase_date = input('Now enter the purchase date in YYYY-MM-DD format: ')
        value = sharesNotKnown(purchase_cost, purchase_date, last_price, result)
    else:
        print('You did not enter "Y" or "N". You\'re gonna have to start over!')
        exit(1)
    print(f'Using data from ' + last_updated + ', your holdings are worth $%.2f.' % value)
except KeyboardInterrupt:
    print("Bye!!!")