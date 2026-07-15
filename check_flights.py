import os
import requests
import smtplib
from email.message import EmailMessage


API_KEY = os.environ["SERPAPI_KEY"]

TARGET_PRICE = 180

ORIGIN = "PHX"
DESTINATION = "SEA"


params = {
    "engine": "google_flights",
    "departure_id": ORIGIN,
    "arrival_id": DESTINATION,
    "outbound_date": "2026-09-15",
    "return_date": "2026-09-20",
    "currency": "USD",
    "hl": "en",
    "api_key": API_KEY
}


response = requests.get(
    "https://serpapi.com/search",
    params=params
)

data = response.json()


try:
    flights = data["best_flights"]

    price = flights[0]["price"]

except:
    print("Could not find flights")
    exit()


print(f"Lowest price found: ${price}")


if price <= TARGET_PRICE:

    msg = EmailMessage()

    msg["Subject"] = (
        "🔥 PHX → SEA Flight Deal Found!"
    )

    msg["From"] = os.environ["EMAIL_FROM"]

    msg["To"] = os.environ["EMAIL_TO"]

    msg.set_content(
        f"""
        Phoenix to Seattle deal found!

        Price:
        ${price}

        Target:
        ${TARGET_PRICE}

        Check Google Flights now.
        """
    )


    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            os.environ["EMAIL_FROM"],
            os.environ["EMAIL_PASSWORD"]
        )

        smtp.send_message(msg)

else:

    print(
        "No deal yet."
    )
