import requests
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

API_STOCK = "ZOUDWTFD3Y6R5WKA"
API_NEWS = "9ceeaeb6b15b4e7eae2bf8f762cb16ee"

parameters = {
    "function":"TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": API_STOCK,
}

response = requests.get(url=STOCK_ENDPOINT, params= parameters)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
print(data)
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

new_data_list= [value for (key,value) in data.items()]
print(new_data_list)

yesterday=new_data_list[0]['4. close'] #closing value yesterday
print(yesterday)
before_yesterday=new_data_list[1]['4. close'] #closing value day before yesterday
print(before_yesterday)

normal_dif = float(yesterday)-float(before_yesterday)

if normal_dif<0:
    sign = "🔻"
else:
    sign = "🔺"

dif = abs(normal_dif)
print(dif)

percent = round((dif/float(yesterday))*100)

print(percent)

    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.


#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

from twilio.rest import Client

TWILIO_ACCOUNT= os.environ.get("TWILIO_ACCOUNT")
TWILIO_TOKEN= os.environ.get("TWILIO_TOKEN")

account_sid = TWILIO_ACCOUNT
auth_token = TWILIO_TOKEN

def send_message():
    global news
    client = Client(account_sid, auth_token)
    for n in range(3):
        message = client.messages \
            .create(
            body=f"{STOCK_NAME} : {sign} {percent} \n Headline: {news[n]['title']} \n Brief: {news[n]['description']}",
            from_='+19032460085',
            to='+447795205833'
        )

    print(message.sid)

#TODO 9. - Send each article as a separate message via Twilio.


if percent > 5:
    parameters_news = {
        "q": COMPANY_NAME,
        "apiKey": API_NEWS,
        "language" : 'en',
        "sort_by" : 'relevancy',
    }
    response_news = requests.get(url=NEWS_ENDPOINT, params=parameters_news)
    response_news.raise_for_status()
    news= response_news.json()['articles'][:3]
    print(news)
    send_message()

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

