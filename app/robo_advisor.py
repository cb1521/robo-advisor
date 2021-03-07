# this is the "app/robo_advisor.py" file

import csv
import os
import requests
import json
import dotenv 
dotenv.load_dotenv()

#Info Inputs

symbol= input("Please specify the stock symbol you wish to acquire data for: ")
#print(type(symbol))
api_key= os.environ.get("ALPHAVANTAGE_API_KEY")
request_url= f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
print(request_url)
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
print("SELECTED SYMBOL:", symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DATA FROM:", last_refreshed)
print("LATEST CLOSE:", float(latest_close))
print("RECENT HIGH:", float(recent_high))
print("RECENT LOW:", float(recent_low))
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("WRITING DATA TO CSV...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")

#csv_file_path= "data/prices.csv"

csv_file_path= os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers= ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above

    #looping
    for x in dates:
        daily_prices= tsd[x]
        writer.writerow({"timestamp": x, 
        "open": daily_prices["1. open"], 
        "high": daily_prices["2. high"], 
        "low": daily_prices["3. low"], 
        "close": daily_prices["4. close"], 
        "volume": daily_prices["5. volume"]})

