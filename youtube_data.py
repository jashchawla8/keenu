import requests
import pandas as pd
# from pymongo import MongoClient

# MongoDB connection setup
# client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI if needed
# db = client['youtube_database']  # Database name
# collection = db['video_titles']  # Collection name

API_KEY = 'AIzaSyA8q8h_p-mniKAVyH0OmqQwyLYNYk6PCSI'  # Replace with your actual API key
SEARCH_QUERY = 'crypto market trends'     # Replace with your search query
MAX_RESULTS = 1000                   # Number of results to fetch

# List of tokens to check for in video titles
#TOKENS = ["Bitcoin", "Ethereum", "Dogecoin", "Cardano", "Litecoin", "Ripple"]  # Add tokens as needed

TOKENS = pd.read_csv("top_1000_crypto_tokens_names.csv")["name"].tolist()


# URL to search videos by a query
base_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=50&q={}&key={}'.format(SEARCH_QUERY, API_KEY)

# Prepare data list for DataFrame
video_data = []
total_fetched = 0
next_page_token = None

while total_fetched < MAX_RESULTS:
    url = base_url
    if next_page_token:
        url += f'&pageToken={next_page_token}'
    
    # Make a GET request to fetch the data
    response = requests.get(url)
    data = response.json()
    
    # Extract required information from each video item
    for item in data.get('items', []):
        # Check if the item is a video and contains 'videoId'
        if item['id']['kind'] == 'youtube#video' and 'videoId' in item['id']:
            video_title = item['snippet']['title']
            video_description = item['snippet'].get('description', '')  # Get description or an empty string if missing
            video_id = item['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            published_time = item['snippet']['publishedAt']  # Extract published time

            # Find tokens mentioned in either the title or description
            tags = [token for token in TOKENS if token.lower() in (video_title + " " + video_description).lower()]

            # Extract thumbnail URLs
            thumbnails = item['snippet']['thumbnails']
            thumbnail_url = thumbnails.get('high', thumbnails.get('medium', thumbnails.get('default')))['url']

            # Append data to list
            video_data.append({
                'title': video_title,
                'description': video_description,
                'url': video_url,
                'tags': tags,
                'thumbnail_url': thumbnail_url,
                'published_time': published_time
            })
            total_fetched += 1
            if total_fetched >= MAX_RESULTS:
                break
    
    # Check if there is a next page token
    next_page_token = data.get('nextPageToken')
    if not next_page_token:
        break

# Create DataFrame
df = pd.DataFrame(video_data)
df.to_csv('youtube_data_3.csv', index=False)
# Store DataFrame in MongoDB
# collection.insert_many(df.to_dict("records"))

# Output the DataFrame
print("Data stored in MongoDB. Here's the DataFrame:")
print(df)