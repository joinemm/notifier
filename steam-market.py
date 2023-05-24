import os

import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
from random_user_agent.params import HardwareType
from random_user_agent.user_agent import UserAgent

load_dotenv()
user_agent_rotator = UserAgent(hardware_types=[HardwareType.COMPUTER.value], limit=100)


def get_listings(url):
    response = requests.get(
        url, headers={"User-Agent": user_agent_rotator.get_random_user_agent()}
    )
    soup = BeautifulSoup(response.text, "lxml")
    listings = soup.select(".market_recent_listing_row")
    return [
        {
            "id": listing.select_one(".item_market_action_button").get("href").split(",")[1].strip(" '"),  # type: ignore
            "price": listing.select_one(".market_listing_price_with_fee").text.strip(),  # type: ignore
            "name": listing.select_one(".market_listing_item_name").text.strip(),  # type: ignore
        }
        for listing in listings
    ]


if __name__ == "__main__":
    WEBHOOK_URL = os.environ["WEBHOOK_URL"]
    URL = "https://steamcommunity.com/market/listings/730/"
    items = [
        URL + "%E2%98%85%20Broken%20Fang%20Gloves%20%7C%20Jade%20%28Field-Tested%29",
    ]

    for item in items:
        listings = get_listings(item)
        with open("known_listings.txt", "r+") as f:
            content = f.read().split()
            print(content)
            for listing in listings:
                if listing["id"] in content:
                    continue
                else:
                    webhook = DiscordWebhook(
                        url=WEBHOOK_URL,
                        content=f"New Steam market Listing for {listing['name']} - **{listing['price']}** [link]({item})",
                    )
                    response = webhook.execute()
                    f.write(listing["id"] + "\n")
