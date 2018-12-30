from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import json


def getJSONAsString(symbol):
    url = urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol +
                  '&outputsize=full&apikey=KIH6VFJ03Z89T5DI')
    str_response = url.read()
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

def singleHoldingMode():
    while True:
        symbol = input('Please enter symbol name: ')
        str_response = getJSONAsString(symbol)
        if b"Invalid" not in str_response:
            break
        else:
            print("Invalid API call! Try again.")

    result = json.loads(str_response)
    last_updated = result['Meta Data']['3. Last Refreshed']
    last_price = float(result['Time Series (Daily)'][last_updated]['4. close'])
    shares = float(input('Please enter number of shares: '))
    value = sharesKnown(shares, last_price)

    print(f'Using data from ' + last_updated + ', your holdings are worth $%.2f.' % value)
    return

def initializeTable(symbolSet):
    table = {}
    for symbol in symbolSet:
        table[symbol] = 0
    return table

def updateTable(table):
    for key in table:
        while True:
            shares = input('How many shares of ' + key.upper() + ' do you own? ')
            try:
                number = int(shares)
                if number <= 0:
                    print("That number was not positive, please try again.")
                else:
                    table[key] = shares
                    break
            except ValueError:
                print("This was not a number, please try again.")

    return table


def portfolioMode():
    print('You have selected Portfolio mode. To start, enter all of your portolio\'s symbols. \n'
          'We will let you know if we can\'t find the symbol you entered and ask you to try again. \n'
          'When you\'re done entering symbols, please enter "Done"\n')

    symbolSet = []

    while True:
        symbol = input('Please enter symbol name: ')
        if symbol.lower() == "done":
            break
        else:
            if symbol.upper() not in symbolSet:
                str_response = getJSONAsString(symbol)
                if b"Invalid" not in str_response:
                    # add symbol to symbol list
                    print("Found recent market data for " + symbol.upper() + "!")
                    symbolSet.append(symbol.upper())
                else:
                    print("Invalid API call! Try again.")
            else:
                print(symbol.upper() + " was already in the symbol list.")

    if len(symbolSet) == 0:
        print("You have given us an empty symbol list. Your total portfolio value is $0.00!")
    else:
        print("the list is not empty")
        print(symbolSet)
        table = initializeTable(symbolSet)
        print(table)
        print('Now you must tell us how many shares (as integers) of each stock you own.\n')
        table = updateTable(table)
        print(table)
    return

try:
    mode = input('Enter "P" for Portfolio (multiple holdings) mode or "S" for single holding mode: ')
    if mode.lower() == 'p':
        # do portfolio
        portfolioMode();
    elif mode.lower() == 's':
        # do single holding
        singleHoldingMode()
except KeyboardInterrupt:
    print("\nBye!!!")