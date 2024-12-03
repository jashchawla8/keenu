import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load Llama 3 model and tokenizer from Hugging Face
model_name = "meta-llama/Llama-3.2-1B"  # Replace with the specific model variant you need
tokenizer = AutoTokenizer.from_pretrained(model_name)
#model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,
)
model.to("mps")
# Function to perform sentiment analysis and generate a summary
def get_sentiment_summary_and_weightage(text, tokens):
    # Handle missing or NaN text
    if pd.isna(text) or not isinstance(text, str) or not text.strip():
        return "No valid input text for sentiment analysis.", {}

    try:
        # Prepare the prompt for the model
        prompt = (
            f"Analyze the sentiment and provide a short summary under 60 words for the following text:\n\n{text}\n\n"
            f"Additionally, calculate the relevance of the following tokens in the text: {tokens}."
        )

        # Tokenize the input text
        inputs = tokenizer.encode(prompt, return_tensors="pt").to("mps")

        # Generate response from the model
        outputs = model.generate(inputs, max_length=200, temperature=0.5)

        # Decode the generated text
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Parse the response to extract sentiment and weightage
        # Assuming response format includes summary first and token weightage as JSON-like text
        parts = result.split("\n", 1)
        sentiment_summary = parts[0] if parts else "No summary available"
        token_weightage = eval(parts[1]) if len(parts) > 1 else {}

        return sentiment_summary, token_weightage
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return "Error in summary generation", {}

# Load data from the existing CSV
input_csv = 'youtube_data_4_copy.csv'  # Replace with your input CSV filename
output_csv = 'youtube_data_with_sentiment_llama.csv'  # Replace with your desired output filename
df = pd.read_csv(input_csv)

# Assuming you have a list of tokens
TOKENS = ['Bitcoin', 'Ethereum', 'Dogecoin', 'Cardano', 'Ripple', 'Litecoin']  # Replace with your token list

# Apply the function to each row in the DataFrame
df[['summary', 'weightage']] = df.apply(
    lambda row: pd.Series(get_sentiment_summary_and_weightage(row.get('description', ''), TOKENS)),
    axis=1
)

# Save the updated DataFrame to a new CSV file
df.to_csv(output_csv, index=False)
print(f"Data saved with sentiment analysis to {output_csv}.")
