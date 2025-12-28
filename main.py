import requests
import time

# ===== WEATHER API =====
API_KEY = "11f04d652b2e45259d5144428252812"
CITY = "Dehradun"

# ===== TELEGRAM =====
BOT_TOKEN = "8438796872:AAEtrjfPgsjIEYjRdjWnJRkfqu6CGC4KQxk"

telegram_api = f"https://api.telegram.org/bot{BOT_TOKEN}"

last_update_id = None

print("🤖 Bot started... Waiting for /weather command")

while True:
    params = {}
    if last_update_id:
        params["offset"] = last_update_id + 1

    response = requests.get(
        telegram_api + "/getUpdates",
        params=params
    ).json()

    if "result" in response:
        for update in response["result"]:
            last_update_id = update["update_id"]

            if "message" not in update:
                continue

            text = update["message"].get("text", "")
            chat_id = update["message"]["chat"]["id"]

            print("📩 Message received:", text)

            if text == "/weather":

                print("🌤 Fetching weather...")

                weather = requests.get(
                    "https://api.weatherapi.com/v1/current.json",
                    params={"key": API_KEY, "q": CITY}
                ).json()

                msg = (
                    "🌤 Weather Update\n"
                    f"City : {weather['location']['name']}\n"
                    f"Temp : {weather['current']['temp_c']}°C\n"
                    f"Humidity : {weather['current']['humidity']}%\n"
                    f"Wind : {weather['current']['wind_kph']} km/h"
                )

                requests.post(
                    telegram_api + "/sendMessage",
                    data={
                        "chat_id": chat_id,
                        "text": msg
                    }
                )

                print("✅ Weather sent")

    time.sleep(2)
