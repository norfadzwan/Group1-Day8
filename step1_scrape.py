import requests
import json
from datetime import datetime

def scrape_country(base="USD", targets=["MYR", "EUR", "GBP"]):
    """
    Fetches the latest currency exchange rates from 'base' to each target currency.
    Returns the rates as a dictionary or None if the request fails.
    """
    url = "https://api.frankfurter.dev/v1/latest"
    params = {
        "from": base,
        "to": ",".join(targets)
    }
    try:
        response = requests.get(url, params=params, verify=False)
        response.raise_for_status()
        data = response.json()
        # print(f"Exchange rates for {data['base']} on {data['date']}:")
        # for currency, rate in data['rates'].items():
        #     print(f"  1 {data['base']} = {rate} {currency}")
        # return data['rates']

        # Filter the rates dictionary so it only includes the target currencies
        filtered_rates = {cur: rate for cur, rate in data['rates'].items() if cur in targets}
        # Build the filtered JSON object
        filtered_json = {
            "base": data["base"],
            "date": data["date"],
            "rates": filtered_rates,
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        }

        # Print the raw JSON in a readable format
        print(json.dumps(filtered_json, indent=2))
        return data  # You can also return it for further use

    except requests.RequestException as e:
        print("Error fetching data:", e)
        return None

# Usage Example
scrape_country()



# # ============================================================
# # step1_scrape.py
# # WHAT  : Fetch weather data from wttr.in for Kuala Lumpur
# # HOW   : Use requests to call the API, parse the JSON response
# # ============================================================

# import requests
# import json
# from datetime import datetime


# def scrape_country(country: str = "EUR") -> dict:
#     """
#     Scrape current country for a given country from frankfurter.
#     Returns a clean dictionary with the exchange rate data.
#     """

#     # wttr.in supports JSON format via ?format=j1
#     url = f"https://api.frankfurter.dev/v1/latest?from=USD&to=MYR,EUR,GBP"

#     print(f"[SCRAPE] Fetching rate for: {country}")
#     print(f"[SCRAPE] URL: {url}")

#     # Send GET request to the website
#     response = requests.get(url, timeout=10)

#     # Check if the request was successful (status code 200 = OK)
#     if response.status_code != 200:
#         raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

#     # # Parse the JSON response
#     # raw = response.json()

#     # Extract only the fields we need
#     # current = raw["current_condition"][0]
#     # nearest_area = raw["nearest_area"][0]

#     # exchange_data = {
#     #     "country": country,
#     #     "country": nearest_area["country"][0]["value"],
#     #     "rate": float(current[""]),
#     #     "feels_like_c": int(current["FeelsLikeC"]),
#     #     "humidity_percent": int(current["humidity"]),
#     #     "wind_speed_kmph": int(current["windspeedKmph"]),
#     #     "weather_desc": current["weatherDesc"][0]["value"],
#     #     "visibility_km": int(current["visibility"]),
#     #     "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     # }

#     # print(f"[SCRAPE] Success! Exchange_rate: {exchange_data['temperature_c']}°C | {exchange_data['weather_desc']}")
#     # return exchange_data


# # ── Run this file directly to test ───────────────────────────
# # if __name__ == "__main__":
# #     data = scrape_country("MYR")
# #     print("\n── Exchange Rate Data ──")
# #     print(json.dumps(data, indent=2))