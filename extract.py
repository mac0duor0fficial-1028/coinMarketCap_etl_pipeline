import requests
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

def fetch_crypto_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    api_key =   os.getenv("CMC_API_KEY")# Placeholder: In a production environment, use environment variables for API keys
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": api_key
    }
    params = {
        "start": "1",
        "limit": "5000",
        "convert": "USD"
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    crypto_market_data = pd.DataFrame(data['data'])
    crypto_market_data.to_csv('crypto_market_data.csv', index=False)

    return crypto_market_data