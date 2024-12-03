import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import os
# Set your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
llm = OpenAI(api_token=openai_api_key)
pandas_ai = PandasAI(llm)

# Read the CSV file
file_path = "reddit_crypto_posts_2.csv"
data = pd.read_csv(file_path)

# Define the query to process the content
query = """
For each row, do the following:
1. Generate a 50-word summary of the 'Content' column.
2. Perform sentiment analysis of the 'Content' column (Posopitive, Negative, Neutral).
3. Identify discussed tokens in the 'Content' column and calculate their weightage as a dictionary.

Add three new columns:
- 'Summary': The 50-word summary.
- 'Sentiment': The sentiment analysis result.
- 'Token Weights': The token weights dictionary.
"""

# Use PandasAI to process the data

processed_data = pandas_ai.run(data, query)
print(processed_data)
# Save the updated DataFrame to a new CSV
# output_path = "updated_reddit_data.csv"
# processed_data.to_csv(output_path, index=False)

# print(f"Processed data saved to {output_path}")
