# this is the "app/robo_advisor.py" file

import csv
import os
import requests
import json
import dotenv 
import datetime
dotenv.load_dotenv()

#Info Inputs

symbol= input("Please specify the stock symbol you wish to acquire data for: ")

try:
    int(symbol)
    print("Looks like you entered a number! Please try again.")
    quit()
except ValueError:
    pass

if len(symbol)<1 or len(symbol)>5:
    print("Please enter a stock identifier that has between 1 to 5 characters. Try again!")
    quit()
else:
    pass
#print(type(symbol))
api_key= os.environ.get("ALPHAVANTAGE_API_KEY")
request_url= f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
#print(request_url)
response= requests.get(request_url)
if "Error Message" in str(response.text): #data validation method
    print("It seems as if you input an invalid stock symbol! Please try again.")
    quit()
#print(response.status_code) #200
#print(response.text)
parsed_response=json.loads(response.text)

last_refreshed= parsed_response["Meta Data"]["3. Last Refreshed"]
now= datetime.datetime.now()
tsd= parsed_response["Time Series (Daily)"]
dates=list(tsd.keys())
latest_day= dates[0] #assumes latest day is first, may need to sort if not the case
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    
    Param: my_price (int or float) like 4000.444444
    
    Example: to_usd(4000.444444)
    
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71
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
recommendation_guide= float(recent_high)/float(latest_close)
#print(recommendation_guide)
if recommendation_guide <= 1.1:
    recommendation= "BUY!"
    recommendation_reason= "The recent high is greater than the latest close by 10 percent or less. This suggests that the stock has not been volatile recently or is on an upward projection."
else:
    recommendation= "DON'T BUY."
    recommendation_reason= "The recent high is greater than the latest close by more than 10 percent. This suggests that the stock is recently volatile and risky or is falling from a recent peak."
#breakpoint()
#Info Outputs




print("-------------------------")
print("SELECTED SYMBOL:", symbol.upper())
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT:", now.strftime("%Y-%m-%d %I:%M %p"))
print("-------------------------")
print("LATEST DATA FROM:", last_refreshed)
print("LATEST CLOSE:", to_usd(float(latest_close)))
print("RECENT HIGH:", to_usd(float(recent_high)))
print("RECENT LOW:", to_usd(float(recent_low)))
print("-------------------------")
print("RECOMMENDATION:", recommendation)
print("RECOMMENDATION REASON:", recommendation_reason)
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

