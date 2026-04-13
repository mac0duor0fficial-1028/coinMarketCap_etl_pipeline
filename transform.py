def preprocess_crypto_data(crypto_market_data):
    columns_to_drop = [
        'quote', 'tags', 'tvl_ratio', 'platform',
        'self_reported_circulating_supply',
        'self_reported_market_cap', 'minted_market_cap'
    ]

    crypto_market_data_cleaned = crypto_market_data.drop(columns=columns_to_drop)
    crypto_market_data_cleaned = crypto_market_data_cleaned.dropna(how='any')
    crypto_market_data_cleaned = crypto_market_data_cleaned.drop_duplicates()

    return crypto_market_data_cleaned