import requests
import pandas as pd

# Replace with your actual API key
API_KEY = 'AIzaSyA8q8h_p-mniKAVyH0OmqQwyLYNYk6PCSI'
SEARCH_QUERY = 'crypto market trends'  # Replace with your search query
MAX_RESULTS = 1000  # Number of results to fetch

# List of tokens to check for in video titles
TOKENS = pd.read_csv("top_1000_crypto_tokens_names.csv")["name"].tolist()

# URL to search videos by a query
base_url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&maxResults=50&q={}&key={}'.format(SEARCH_QUERY, API_KEY)

# Prepare data list for DataFrame
video_data = []
total_fetched = 0
next_page_token = None

def fetch_video_details(video_id):
    """Fetch complete video details using the YouTube videos API."""
    url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    if 'items' in data and len(data['items']) > 0:
        snippet = data['items'][0]['snippet']
        return snippet.get('description', '')  # Return full description
    return ''

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
            video_id = item['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            published_time = item['snippet']['publishedAt']  # Extract published time

            # Fetch full video description
            video_description = fetch_video_details(video_id)

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
df.to_csv('youtube_data_full_description.csv', index=False)

# Output the DataFrame
print("Data saved to 'youtube_data_full_description.csv'. Here's the DataFrame:")
print(df)
