from urllib.request import urlopen
import json

try:
    symbol = input('Please enter symbol name: ')
    url = urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol +
                  '&outputsize=full&apikey=KIH6VFJ03Z89T5DI')
    str_response = url.read()
    result = json.loads(str_response)
    last_updated = result['Meta Data']['3. Last Refreshed']
    last_price = float(result['Time Series (Daily)'][last_updated]['4. close'])

    answer = input('Do you know how many shares you purchased? Enter "y" or "n": ')

    if answer.lower() == 'y':
        shares = float(input('Please enter number of shares: '))
        value = last_price*shares
        print (f'Using data from ' + last_updated + ', your holdings are worth $%.2f.' % value)
    elif answer.lower() == 'n':
        purchase_cost = float(input('If you don\'t know how many shares you purchased, enter your total stock purchase '
                                     'cost: $'))
        purchase_date = input('Now enter the purchase date in YYYY-MM-DD format: ')
        shares = float(purchase_cost) / float(result['Time Series (Daily)'][purchase_date]['4. close'])
        value = last_price*shares
        print(f'Using data from ' + last_updated + ', your holdings are worth $%.2f.' % value)
    else:
        print('You did not enter "y" or "n". You\'re gonna have to start over!')
except KeyboardInterrupt:
    print("Bye!!!")