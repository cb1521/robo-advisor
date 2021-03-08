# this is the "app/robo_advisor.py" file

import csv
import os
import requests
import json
import dotenv 
import datetime
dotenv.load_dotenv()

#Info Inputs
symbol_list= []
print("Welcome to the Robo Advisor! Feel free to enter up to 5 stock symbols at a time, one at a time, using the input below.")
while True:
    symbol= input("Please specify the stock symbol you wish to acquire data for, or type the word  done when there are no more inputs: ")
    try:
        int(symbol)
        print("Looks like you entered a number! Please try again.")
        continue
    except ValueError:
        pass

    if len(symbol)<1 or len(symbol)>5:
        print("You must enter a stock identifier that has between 1 to 5 characters. Try again!")
        continue
    else:
        pass
    #print(type(symbol))
    if symbol.lower()== "done":
        break
    elif len(symbol_list)== 5:
        print("You have reached your 5 stock limit. The first 5 stock symbols you have entered are the only ones that will be evaluated currently. If you still want to get data on this stock, you can do so after this session is complete.")
        while True:
            proceed= input("With this information in mind, do you wish to continue? (y/n): ")
            if proceed.lower()== "y":
                break
            elif proceed.lower()== "n":
                quit()
            else:
                print("Please enter either y or n.")
        break
    else:
        symbol_list.append(symbol)
#print(symbol_list)

for ticker in symbol_list:
    api_key= os.environ.get("ALPHAVANTAGE_API_KEY")
    request_url= f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}"
    #print(request_url)
    response= requests.get(request_url)
    if "https://www.alphavantage.co/documentation/" in str(response.text): #data validation method
        print("It seems as if you input an invalid stock symbol! This symbol will not generate any data. The rest of the symbols will still be generated.")
        continue
    elif "https://www.alphavantage.co/premium/" in str(response.text):
        print("You have either exceeded your calls per minute or your calls per day. Try again in a minute, or come back tomorrow!")
        quit()
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
    for date in dates:
        high_price=tsd[date]["2. high"]
        low_price=tsd[date]["3. low"]
        highs.append(float(high_price))
        lows.append(float(low_price))
    recent_high= max(highs)
    recent_low= min(lows)
    recommendation_guide= float(recent_high)/float(latest_close)
    #print(recommendation_guide)
    if recommendation_guide <= 1.1:
        recommendation= "BUY!"
        recommendation_reason= "The recent high is greater than the latest close by up to 10%. This suggests that the stock has not been volatile recently or is on an upward projection."
    else:
        recommendation= "DON'T BUY."
        recommendation_reason= "The recent high is greater than the latest close by more than 10%. This suggests that the stock is recently volatile and risky or is falling from a recent peak."
    #breakpoint()
    #Info Outputs




    print("-------------------------")
    print("SELECTED SYMBOL:", ticker.upper()) #symbol.upper()
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

    csv_file_path= os.path.join(os.path.dirname(__file__), "..", "data", f"prices_{ticker}.csv")
    csv_headers= ["timestamp", "open", "high", "low", "close", "volume"]

    with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
        writer.writeheader() # uses fieldnames set above

        #looping
        for y in dates:
            daily_prices= tsd[y]
            writer.writerow({"timestamp": y, 
            "open": daily_prices["1. open"], 
            "high": daily_prices["2. high"], 
            "low": daily_prices["3. low"], 
            "close": daily_prices["4. close"], 
            "volume": daily_prices["5. volume"]})

