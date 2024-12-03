import openai
import pandas as pd
from typing import Dict, List
import os
from pydantic import BaseModel
import textwrap
# Set up your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

class VideoAnalysis(BaseModel):
    sentiment: str
    summary: str
    token_weightage: Dict[str, float]

# Define the structured prompt
structured_prompt = '''
You will be provided with the title and description of a YouTube video related to cryptocurrency.
Your goal will be to analyze the content and return a structured response following this schema:

- sentiment: (string) overall sentiment of the text (e.g., positive, negative, neutral)
- summary: (string) a concise summary of the video description, no longer than 60 words
- token_weightage: (dictionary) relevance scores of given tokens in the text, in the form {"token": score} if none are given, return an empty dictionary

Here is the input:
'''

# Function to perform analysis using OpenAI
def get_sentiment_summary_and_weightage(text: str, tokens: List[str]) -> Dict:
    if pd.isna(text) or not isinstance(text, str) or not text.strip():
        return {"sentiment": "N/A", "summary": "No valid input text", "token_weightage": {}}

    token_list = ", ".join(tokens)

    try:
        # Call OpenAI API with structured response prompt
        response = openai.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": textwrap.dedent(structured_prompt)},
                {"role": "user", "content": f"{text}\n\nTokens: {token_list}"}
            ],
            temperature=0.5,
            response_format=VideoAnalysis
        )

        # Extract response content
        structured_response = response
        print(f"Raw response: {structured_response}")

        # Manually parse the response
        response_lines = structured_response.split("\n")
        sentiment = response_lines[0].split(":", 1)[1].strip() if len(response_lines) > 0 else "N/A"
        summary = response_lines[1].split(":", 1)[1].strip() if len(response_lines) > 1 else "No summary available"
        token_weightage = eval(response_lines[2].split(":", 1)[1].strip()) if len(response_lines) > 2 else {}

        return {
            "sentiment": sentiment,
            "summary": summary,
            "token_weightage": token_weightage
        }

    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return {"sentiment": "Error", "summary": "Error in generating summary", "token_weightage": {}}

# Load data from the CSV file
input_csv = 'youtube_data_4_copy.csv'  # Replace with your input CSV filename
output_csv = 'youtube_data_with_sentiment.csv'  # Replace with your desired output filename
df = pd.read_csv(input_csv)

# Load tokens from a file or list
TOKENS = pd.read_csv("top_1000_crypto_tokens_names.csv")["name"].tolist()

# Apply the function to each row in the DataFrame
results = df['description'].apply(lambda text: get_sentiment_summary_and_weightage(text, TOKENS))
df['sentiment'] = results.apply(lambda x: x['sentiment'])
df['summary'] = results.apply(lambda x: x['summary'])
df['weightage'] = results.apply(lambda x: x['token_weightage'])

# Save the updated DataFrame to a new CSV file
df.to_csv(output_csv, index=False)
print(f"Data saved with structured output to {output_csv}.")
