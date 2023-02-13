import os

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook


def get_price(product):
    URL = f"https://www.veke.fi/product/{product}"

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "lxml")

    price_div = soup.select_one(".price")

    if price_div:
        price = price_div.text.strip().strip("\xa0€").replace(",", ".")
        amount = float(price)
        return amount
    else:
        return None


if __name__ == "__main__":
    WEBHOOK_URL = os.environ["WEBHOOK_URL"]

    products = [
        ("saana-kylpypyyhe-90x160-cm-hiekka", 22.0),
        ("saana-kasipyyhe-50x70-cm-hiekka", 7.0),
    ]

    for product, price_threshold in products:
        price = get_price(product)
        if price and price <= price_threshold:
            webhook = DiscordWebhook(
                url=WEBHOOK_URL,
                content=f"**{product}** is `{price}€`",
            )
            response = webhook.execute()
