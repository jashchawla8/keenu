import requests
from datetime import datetime, timedelta
import pandas as pd
import json

yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

API_KEY = '3e0268e173224f6eb66573622eceaa92'  
url = ('https://newsapi.org/v2/everything?'
       'q=crypto&'
       'from={}&'
       'sortBy=popularity&'
       'apiKey={}'.format(yesterday, API_KEY))

data = requests.get(url)
data = data.json()

TOKENS = ["Bitcoin", "Ethereum", "Dogecoin", "Cardano", "Litecoin", "Ripple"]
articles = data.get('articles', [])

# Extract required fields
titles, thumbnails, descriptions, urls, published_times, tags = [], [], [], [], [], []
# for article in articles:
#     titles.append(article['title'])
#     thumbnails.append(article['urlToImage'])
#     descriptions.append(article['description'])
#     urls.append(article['url'])
#     published_times.append(article['publishedAt'])
#     tags = [token for token in TOKENS if token.lower() in (article['title'] + " " + article['description']).lower()]

# # Create DataFrame
# df = pd.DataFrame({
#     "title": titles,
#     "thumbnail": thumbnails,
#     "description": descriptions,
#     "url": urls,
#     "published_time": published_times,
#     "tags": tags
# })

df = pd.DataFrame({
    'title': [article.get('title', 'N/A') for article in articles],
    'thumbnail': [article.get('urlToImage', 'N/A') for article in articles],
    'description': [article.get('description', 'N/A') for article in articles],
    'publishedAt': [article.get('publishedAt', 'N/A') for article in articles],
    'tags': [
        [token for token in TOKENS if token.lower() in (article.get('title', '') + " " + article.get('description', '')).lower()]
        for article in articles
    ]
})
# Generate tags from descriptions
# def generate_tags(descriptions):
#     vectorizer = CountVectorizer(max_features=5, stop_words='english')
#     X = vectorizer.fit_transform(descriptions)
#     tags_list = []
#     for row in X.toarray():
#         tags = [vectorizer.get_feature_names_out()[i] for i, val in enumerate(row) if val > 0]
#         tags_list.append(", ".join(tags))
#     return tags_list

# df['tags'] = generate_tags(df['description'])

# Display the resulting DataFrame
print(df)

df.to_csv('news_articles.csv', index=False)

