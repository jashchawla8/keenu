import openai
import pandas as pd
import os
import textwrap

# Set up your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# Define the structured prompt
structured_prompt = '''
You will be provided with the content of a Reddit post related to cryptocurrency.
Your goal will be to analyze the content and return a structured response following this schema:

- sentiment: (string) overall sentiment of the text (e.g., positive, negative, neutral)
- summary: (string) a concise summary of the post content, no longer than 50 words
- token_weightage: (dictionary) relevance scores of given tokens in the text, in the form {"token": score} if none are given, return an empty dictionary

Here is the input:
'''

# Function to perform analysis using OpenAI
def get_sentiment_summary_and_weightage(text: str, tokens: list) -> dict:
    if pd.isna(text) or not isinstance(text, str) or not text.strip():
        return {"sentiment": "N/A", "summary": "No valid input text", "token_weightage": {}}

    token_list = ", ".join(tokens)

    try:
        # Call OpenAI API with structured response prompt
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": textwrap.dedent(structured_prompt)},
                {"role": "user", "content": f"{text}\n\nTokens: {token_list}"}
            ],
            temperature=0.5
        )

        # Extract response content
        structured_response = response.choices[0].message['content']
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
input_csv = 'reddit_crypto_posts_2.csv'  # Replace with your input CSV filename
output_csv = 'reddit_crypto_posts_with_analysis.csv'  # Replace with your desired output filename
df = pd.read_csv(input_csv)

# Load tokens from a file or list
TOKENS = pd.read_csv("top_1000_crypto_tokens_names.csv")["name"].tolist()

# Apply the function to each row in the DataFrame
results = df['Content'].apply(lambda text: get_sentiment_summary_and_weightage(text, TOKENS))
df['sentiment'] = results.apply(lambda x: x['sentiment'])
df['summary'] = results.apply(lambda x: x['summary'])
df['weightage'] = results.apply(lambda x: x['token_weightage'])

# Save the updated DataFrame to a new CSV file
df.to_csv(output_csv, index=False)
print(f"Data saved with structured output to {output_csv}.")