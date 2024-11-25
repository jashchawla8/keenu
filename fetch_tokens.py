import requests
import pandas as pd
import json

# Set Up API Key and Endpoint

# Define the API key and endpoint URL for the CoinMarketCap API
api_key = '1f96b26e-8764-4c1a-8a01-fb1046ceb1b6'  # Replace with your actual CoinMarketCap API key
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

# Set up the headers for the API request
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

# Define the parameters for the API request
parameters = {
    'start': '1',
    'limit': '1000',
    'convert': 'USD'
}


# Fetch Data from CoinMarketCap API

# Make the API request
response = requests.get(url, headers=headers, params=parameters)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    #print(data)
    
    # Extract the relevant data
    crypto_data = data['data']
    
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(crypto_data)
    #print(df.head())
    
    # Save the DataFrame to a CSV file
    df.to_csv('top_1000_crypto_tokens.csv', index=False)
else:
    print(f"Failed to fetch data: {response.status_code}")

# Process and Extract Relevant Data

# Extract relevant data such as token name, symbol, market cap, price, volume, etc.
processed_data = []
for token in crypto_data:
    print(token)
    token_info = {
        'name': token['name'],
        'symbol': token['symbol'],
        'market_cap': token['quote']['USD']['market_cap'],
        'price': token['quote']['USD']['price'],
        'volume_24h': token['quote']['USD']['volume_24h'],
        'percent_change_1h': token['quote']['USD']['percent_change_1h'],
        'percent_change_24h': token['quote']['USD']['percent_change_24h'],
        'percent_change_7d': token['quote']['USD']['percent_change_7d']
    }
    processed_data.append(token_info)

# Convert the processed data to a pandas DataFrame
df_processed = pd.DataFrame(processed_data)

# Save the processed DataFrame to a CSV file
df_processed.to_csv('top_1000_crypto_tokens_processed.csv', index=False)

# Save Data to CSV File

# Use pandas to save the extracted data to a CSV file
df_processed.to_csv('top_1000_crypto_tokens_processed.csv', index=False)

df_processed['name'].to_csv('top_1000_crypto_tokens_names.csv', index=False)
