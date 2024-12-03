import praw
import pandas as pd

# Replace with your Reddit API credentials
client_id = 'EWTyRcDRpOyoO8u2Ebsc9Q'
client_secret = 'FdPffPBPfOfCTLtasi7nwQVn0Ty3RA'
user_agent = 'PsychologicalOwl18'

# Initialize Reddit instance
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)


crypto_tokens = pd.read_csv("top_1000_crypto_tokens_names.csv")["name"].tolist()

# Define subreddits to search
subreddits = "cryptocurrency+CryptoMarkets+Bitcoin+Altcoin"

# Define the number of posts to fetch
num_posts = 1000

# Fetch posts
posts_data = []
for post in reddit.subreddit(subreddits).hot(limit=num_posts):
    tags = [token for token in crypto_tokens if token.lower() in post.title.lower().split(" ") or token.lower() in post.selftext.lower().split(" ")]
    content = post.selftext if post.is_self else None
    if content:
        content = " ".join(content.split())
    posts_data.append({
        "Title": post.title,
        "URL": post.url,
        "Thumbnail": post.thumbnail if post.thumbnail.startswith('http') else None,
        "Score": post.score,
        "Upvote Ratio": post.upvote_ratio,
        "Comments Count": post.num_comments,
        "Author": str(post.author),
        "Created At": post.created_utc,
        "Tags": ", ".join(tags) if tags else None,
        "Content": content
    })

# Create a DataFrame and save to CSV
df = pd.DataFrame(posts_data)
df.to_csv("reddit_crypto_posts_2.csv", index=False)

print("CSV file 'reddit_crypto_posts.csv' has been created successfully.")
