import os
import requests
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta


SERPAPI_KEY = os.environ["SERPAPI_KEY"]

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]


TARGET_PRICE = 180


today = datetime.now()

start_date = today + timedelta(days=14)

end_date = today + timedelta(days=180)


params = {

    "engine": "google_flights",

    "departure_id": "PHX",

    "arrival_id": "SEA",

    "type": "1",

    "currency": "USD",

    "hl": "en",

    "api_key": SERPAPI_KEY,

    "outbound_date":
        start_date.strftime("%Y-%m-%d"),

    "return_date":
        end_date.strftime("%Y-%m-%d")
}


response = requests.get(
    "https://serpapi.com/search",
    params=params
)


data = response.json()


try:

    price = data["price_insights"]["lowest_price"]

except:

    print("Could not find price data")

    exit()


print(
    f"Lowest price found: ${price}"
)


if price <= TARGET_PRICE:


    msg = EmailMessage()

    msg["Subject"] = (
        "🔥 PHX → SEA Flight Deal Found!"
    )

    msg["From"] = EMAIL_FROM

    msg["To"] = EMAIL_TO


    msg.set_content(

f"""

Phoenix → Seattle deal found!

Lowest price:
${price}

Your target:
${TARGET_PRICE}

Check Google Flights and book if the dates work.

"""

    )


    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            EMAIL_FROM,
            EMAIL_PASSWORD
        )

        smtp.send_message(msg)

else:

    print(
        "No deal yet."
    )
