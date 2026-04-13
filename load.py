import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

def load_crypto_data(crypto_market_data_cleaned):
    conn = psycopg2.connect(
        dbname="coin_market_cap_db",
        user="avnadmin",
        password=os.getenv("DB_PASSWORD"),  # Placeholder: In a production environment, use environment variables for credentials
        host="pg-marcos-de-db-marcos.a.aivencloud.com",
        port=14233
    )

    cursor = conn.cursor()

    insert_query = """
        INSERT INTO crypto.crypto_market_data (
            id, name, symbol, slug, infinite_supply, circulating_supply,
            total_supply, max_supply, date_added, num_market_pairs,
            cmc_rank, last_updated
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    data_for_insert = [
        tuple(row) for row in crypto_market_data_cleaned[[
            "id", "name", "symbol", "slug", "infinite_supply", "circulating_supply",
            "total_supply", "max_supply", "date_added", "num_market_pairs",
            "cmc_rank", "last_updated"
        ]].values
    ]

    cursor.executemany(insert_query, data_for_insert)

    conn.commit()

    cursor.close()
    conn.close()