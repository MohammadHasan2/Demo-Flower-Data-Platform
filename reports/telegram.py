import os

import requests
from dotenv import load_dotenv


load_dotenv()


def send_telegram_message(message: str):

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN is not configured"
        )

    if not chat_id:
        raise ValueError(
            "TELEGRAM_CHAT_ID is not configured"
        )

    url = (
        f"https://api.telegram.org/bot"
        f"{bot_token}/sendMessage"
    )

    response = requests.post(
        url,
        json={
            "chat_id": chat_id,
            "text": message
        },
        timeout=15
    )

    response.raise_for_status()

    return response.json()

if __name__ == "__main__":

    send_telegram_message(
        "🌸 ZeeFlower Analytics test message"
    )

    print("Telegram message sent successfully.")