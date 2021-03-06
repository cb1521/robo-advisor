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
latest_close= tsd[latest_day]["4. close"]
highs=[]
lows=[]
for x in dates:
    high_price=tsd[x]["2. high"]
    low_price=tsd[x]["3. low"]
    highs.append(float(high_price))
    lows.append(float(low_price))
recent_high= max(highs)
recent_low= min(lows)
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
print("RECENT HIGH:", float(recent_high))
print("RECENT LOW:", float(recent_low))
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")