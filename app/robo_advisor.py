# this is the "app/robo_advisor.py" file

import requests
import json

#Info Inputs

request_url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
response= requests.get(request_url)
#print(response.status_code) #200
#print(response.text)
parsed_response=json.loads(response.text)

last_refreshed= parsed_response["Meta Data"]["3. Last Refreshed"]
tsd= parsed_response["Time Series (Daily)"]
dates=list(tsd.keys())
latest_day= dates[0] #assumes latest day is first, may need to sort
latest_close= parsed_response["Time Series (Daily)"][latest_day]["4. close"]
#breakpoint()
#Info Outputs




print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY:", last_refreshed)
print("LATEST CLOSE:", float(latest_close))
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")