import requests
import pandas as pd

# Cloudflare API details
API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/c886e2113615b3fe3a957a568dbb03cf/ai/run/"
headers = {"Authorization": "Bearer 0hpaiksD7YysCCWIFJdk1AzMkYtw3TRtJjw_pWeK"}
CLOUDFLARE_ACCOUNT_ID = "your_account_id"  # Replace with your Cloudflare Account ID
CLOUDFLARE_API_TOKEN = "0hpaiksD7YysCCWIFJdk1AzMkYtw3TRtJjw_pWeK"  # Replace with your Cloudflare API Token
LLAMA_MODEL = "@cf/meta/llama-3.1-8b-instruct"  # Llama model to use
BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/c886e2113615b3fe3a957a568dbb03cf/ai/run/{LLAMA_MODEL}"

# Function to perform sentiment analysis and generate a summary
def get_sentiment_and_summary(text, tokens):
    if pd.isna(text) or not isinstance(text, str) or not text.strip():
        return "No valid input text for analysis", {}

    prompt = (
        f"Analyze the sentiment and provide a short summary (under 60 words) for the following text:\n\n{text}\n\n"
        f"Additionally, calculate the relevance of the following tokens in the text: {tokens}."
    )

    try:
        headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "max_tokens": 256,
            "temperature": 0.6
        }

        response = requests.post(BASE_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        print("Raw response:", result)

        # Ensure the 'result' key exists in the response
        generated_text = result.get("result", {}).get("response", "")
        if generated_text:
            # Parse the response to extract the sentiment and token weightage
            sentiment_summary = "No summary available"
            token_weightage = {}

            parts = generated_text.split("\n\n")  # Split into sections
            if len(parts) > 0:
                sentiment_summary = parts[0].strip()  # First part is the sentiment summary
            if len(parts) > 1:
                # Process token weightage (assuming JSON-like structure in the second part)
                try:
                    token_weightage = eval(parts[1].strip())  # Parse relevance as dictionary
                except Exception as e:
                    print(f"Error parsing token relevance: {e}")

            return sentiment_summary, token_weightage
        else:
            return "No valid response from model", {}
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return "Error in sentiment analysis", {}

# Load data from CSV
input_csv = 'youtube_data_4_copy.csv'  # Replace with your input CSV filename
output_csv = 'youtube_data_with_sentiment.csv'  # Replace with your desired output filename
df = pd.read_csv(input_csv)

# Assuming you have a list of tokens
TOKENS = pd.read_csv("top_1000_crypto_tokens_names.csv")["name"].tolist()

# Apply the function to each row in the DataFrame
df[['summary', 'weightage']] = df.apply(
    lambda row: pd.Series(get_sentiment_and_summary(row.get('description', ''), TOKENS)),
    axis=1
)

# Save the updated DataFrame to a new CSV file
df.to_csv(output_csv, index=False)
print(f"Data saved with sentiment analysis to {output_csv}.")
