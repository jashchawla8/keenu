import os

import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

from pandasai import Agent

df = pd.read_csv("reddit_crypto_posts_2.csv")
#tokens = pd.read_csv("top_1000_crypto_tokens_names.csv")["name"].head(20).to_list()

smartdf = SmartDataframe(df, config={"llm":OpenAI(os.getenv("OPENAI_API_KEY")),"description":"The table contains reddit posts about cryptocurrencies. The 'Tags' contains all the tokens that were discussed in the post and the content column, if populated contains text of the posts.","conversational": False, "custom_whitelisted_dependencies": ["nltk", "textblob", "vaderSentiment","collections","gensim", "re"]})
prompt = "I want you to act as a bias breaker. Read through the content and give me a pairing of crypto tokens that the people are hating on and the one they think is going to do good. Name this column 'bias pair'. Give me summary of each row of the 'Content' column in under 30 words and sentiment analysis of the 'Content' column. Save results in three new columns: 'bias pair', 'summary', 'sentiment'."
outputdf = smartdf.chat(prompt, output_type="dataframe")
print(outputdf)
try:
    outputdf.to_csv("reddit_crypto_posts_with_analysipandasai.csv", index=False)
    print("Data saved with structured output to reddit_crypto_posts_with_analysis.csv.")
except Exception as e:
    "Error in saving the file: ", e

