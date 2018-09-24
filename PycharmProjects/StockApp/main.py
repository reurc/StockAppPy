from urllib.request import urlopen;
import json

symbol = input('Please enter symbol name: ');
shares = float(input('Please enter number of shares: '));

url = urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol +'&outputsize=compact&apikey=KIH6VFJ03Z89T5DI');
str_response = url.read();
result = json.loads(str_response);
last_updated = result['Meta Data']['3. Last Refreshed'];
last_price = float(result['Time Series (Daily)'][last_updated]['4. close']);
value = last_price*shares;
print (f'Using data from ' + last_updated + ', your holdings are worth $%.2f.' % value);