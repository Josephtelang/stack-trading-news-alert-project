import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

MY_STACK_API_KEY = "1TGENZC6NXY749GN"
NEWS_API_KEY = "4ba29a41b580488492743b0e7145a8cd"
TWILIO_SID = "AC7da5be457a459024ed243c2e44cc7ed0"
TWILIO_AUTH_TOKEN = "52a8d723c0f39c4a55e378f778a1c796"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
parameters = {
    "function" : "TIME_SERIES_DAILY",
    "symbol" : STOCK_NAME,
    "apikey" : MY_STACK_API_KEY
}
response = requests.get(url=STOCK_ENDPOINT,params=parameters)
stock_data =  response.json()["Time Series (Daily)"]
print(stock_data)

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
list_data = [value for (key,value) in stock_data.items() ]
yesterday_closing_price = list_data[0]["4. close"]

print(yesterday_closing_price)
#TODO 2. - Get the day before yesterday's closing stock price
day_before_yesterday_closing_price = list_data[1]["4. close"]
print(day_before_yesterday_closing_price)
#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
yesterday_c_price =float(yesterday_closing_price) 
day_before_yesterday_c_price = float(day_before_yesterday_closing_price)
difference = yesterday_c_price - day_before_yesterday_c_price

up_down = None
if difference < 0:
    up_down = "📉"
else:
    up_down = "📈"
#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = round((difference / (yesterday_c_price)) * 100 )

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if abs(percentage_difference) > 5:
    parameters = {
        "apikey" : NEWS_API_KEY,
        "qInTitle" : COMPANY_NAME
    }
    
    #TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    response = requests.get(url=NEWS_ENDPOINT,params=parameters)
    news_data = response.json()["articles"]
    #TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    #TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    first_three_articles = news_data[:3]
    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
    formatted_articles =[f"{STOCK_NAME} : {up_down} {percentage_difference}% \n Headline: {article["title"]} , \n Brief: {article["description"]}"for article in first_three_articles]




    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 
client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
#TODO 9. - Send each article as a separate message via Twilio. 
for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_ = "+12315997776",
        to =  "+919359109047"
    )



#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

