# this is the "app/robo_advisor.py" file

#importing necessary packages
import csv
import os
import requests
import json
import dotenv 
import datetime
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt

dotenv.load_dotenv() #establishing the .env file usage
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    
    Param: my_price (int or float) like 4000.444444
    
    Example: to_usd(4000.444444)
    
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71
#Info Inputs
symbol_list= [] #empty list to store all of the stock tickers into for the loop
print("Welcome to the Robo Advisor! Feel free to enter up to 5 stock symbols at a time, one at a time, using the input below.")
while True: #validating data
    symbol= input("Please specify the stock symbol you wish to acquire data for, or type the word  done when there are no more inputs: ")
    try:
        float(symbol) #making sure that the input is not a number
        print("Looks like you entered a number! Please try again.")
        continue
    except ValueError:
        pass #letting everything that is not a number go through

    if len(symbol)<1 or len(symbol)>5: #validating appropriate character length
        print("...You must enter a stock identifier that has between 1 to 5 characters. Try again!")
        continue
    #print(type(symbol))
    elif symbol.lower()== "done": #equalizing the case to make sure there are no errors
        if len(symbol_list)!=0: #allowing done to be typed if it is not the first item entered
            break
        else: #if there have not been any valid identifiers entered, program forces you to enter one
            print("...You have not entered any valid identifiers yet! Please do so before typing done.")
            continue
    elif symbol.lower() in symbol_list: #preventing duplicates
        print("...You have already entered this symbol during this session!")
        continue
    elif len(symbol_list)== 5: #setting the limit imposed by the free api key
        print("...You have reached your 5 stock limit. The first 5 stock symbols you have entered are the only ones that will be evaluated currently. If you still want to get data on this stock, you can do so after this session is complete.")
        while True: #either letting the user continue or quit
            proceed= input("With this information in mind, do you wish to continue? (y/n): ")
            if proceed.lower()== "y":
                break
            elif proceed.lower()== "n":
                quit()
            else:
                print("Please enter either y or n.") #validation
        break
    else:
        symbol_list.append(symbol.lower()) #appending to the list, making lowercase for stylistic purposes for the csv file titles
#print(symbol_list)

for ticker in symbol_list: #looping through each ticker
    api_key= os.environ.get("ALPHAVANTAGE_API_KEY") #using the .env variable
    request_url= f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={api_key}" #getting the appropriate webpage
    #print(request_url)
    response= requests.get(request_url)
    if "https://www.alphavantage.co/documentation/" in str(response.text): #data validation method for invalid
        print("It seems as if you input an invalid stock symbol! This symbol will not generate any data. The rest of the symbols will still be generated.")
        continue
    elif "https://www.alphavantage.co/premium/" in str(response.text): #data validation for exceeding the minute or daily limits
        print("You have either exceeded your calls per minute or your calls per day. Try again in a minute, or come back tomorrow!")
        quit()
    parsed_response=json.loads(response.text) #transforming the response into readable python data

    #setting up various variables and lists
    last_refreshed= parsed_response["Meta Data"]["3. Last Refreshed"]
    now= datetime.datetime.now()
    tsd= parsed_response["Time Series (Daily)"]
    dates=list(tsd.keys())
    latest_day= dates[0] #assumes latest day is first, may need to sort if not the case anymore
    latest_close= tsd[latest_day]["4. close"]
    highs=[]
    lows=[]
    for date in dates: #looping through and banking each variable into the lists
        high_price=tsd[date]["2. high"]
        low_price=tsd[date]["3. low"]
        highs.append(float(high_price))
        lows.append(float(low_price))
    recent_high= max(highs)
    recent_low= min(lows)
    recommendation_guide= float(recent_high)/float(latest_close)
    #print(recommendation_guide)
    if recommendation_guide <= 1.1: #determing whether or not to recommend
        recommendation= "BUY!"
        recommendation_reason= "The recent high is greater than the latest close by up to 10%. This suggests that the stock has not been volatile recently or is on an upward projection."
    else:
        recommendation= "DON'T BUY."
        recommendation_reason= "The recent high is greater than the latest close by more than 10%. This suggests that the stock is recently volatile and risky or is falling from a recent peak."
    chart_data=[] #setting up the line chart for later
    for date, daily_data in tsd.items():
        record = {
            "date": date,
            "close (in dollars)": float(daily_data["4. close"])
        }
        chart_data.append(record)
    #print(chart_data[0])
    chart_df=DataFrame(chart_data)
    #breakpoint()
    #Info Outputs




    print("-------------------------")
    print("SELECTED SYMBOL:", ticker.upper()) #symbol.upper() #stylistic purposes to be upper
    print("-------------------------")
    print("REQUESTING STOCK MARKET DATA...")
    print("REQUEST AT:", now.strftime("%Y-%m-%d %I:%M %p")) #current date and time
    print("-------------------------")
    print("LATEST DATA FROM:", last_refreshed) #letting you know the most recent date
    print("LATEST CLOSE:", to_usd(float(latest_close))) #displaying prices in usd
    print("RECENT HIGH:", to_usd(float(recent_high)))
    print("RECENT LOW:", to_usd(float(recent_low)))
    print("-------------------------")
    print("RECOMMENDATION:", recommendation) #displaying the recommendation, and following reasoning
    print("RECOMMENDATION REASON:", recommendation_reason)
    print("-------------------------")
    print("WRITING DATA TO CSV...")
    print("-------------------------")
    print("SHOWING A LINE CHART OF BEHAVIOR. TO CONTINUE, CLOSE THE IMAGE! DON'T FORGET TO SAVE!")
    print("-------------------------")
    print("HAPPY INVESTING!")
    print("-------------------------")


    #csv_file_path= "data/prices.csv"

    csv_file_path= os.path.join(os.path.dirname(__file__), "..", "data", f"prices_{ticker}.csv") #making a dynamic path for csv file data
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
    
    sns.lineplot(data=chart_df, x="date", y="close (in dollars)")
    plt.show() #displaying the line plot
