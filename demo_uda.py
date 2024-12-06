print("Enter your wallet Address:")
a = input()
import datetime as datetime
import pandas as pd
from tabulate import tabulate
customer_portfolio = pd.read_csv("./uda/{}.csv".format(a))
print(tabulate(customer_portfolio, headers='keys', tablefmt='pretty'))
customer_portfolio['total_investment_per_token'] = customer_portfolio['purchase_price'] * customer_portfolio['quantity']
customer_portfolio['token_weightage'] = customer_portfolio['total_investment_per_token'].apply(lambda x: x  / customer_portfolio['total_investment_per_token'].sum())
customer_portfolio['profit_loss'] = (customer_portfolio['current_price'] - customer_portfolio['purchase_price']) * customer_portfolio['quantity']
customer_portfolio['purchase_date'] = pd.to_datetime(customer_portfolio['purchase_date'])
customer_portfolio['recency'] = customer_portfolio['purchase_date'].rank(method='min', ascending=False)
customer_portfolio['final_rating'] = (customer_portfolio['token_weightage'] * 0.5 + (1/customer_portfolio['recency']) * 0.4)

top_3_tokens_total = customer_portfolio.sort_values('final_rating', ascending=False).head(3)
top_3_tokens_recency = customer_portfolio.sort_values('recency', ascending=True).head(3)
top_3_tokens_weightage = customer_portfolio.sort_values('token_weightage', ascending=False).head(3)

top_3_token = top_3_tokens_total['token_name'].tolist()

tokens_of_interest = top_3_token
# Filter DataFrame for rows where the most_positive_token is in the list of interest
yt_st_ratings = pd.read_csv("./uda/youtube_data_with_sentiment_scores.csv")
reddit_st_ratings = pd.read_csv("./uda/reddit_data_with_sentiment_scores.csv")
news_st_ratings = pd.read_csv("./uda/news_data_with_sentiment_scores.csv")
filtered_df_youtube = yt_st_ratings[yt_st_ratings['most_positive_token'].isin(tokens_of_interest)]
filtered_df_reddit = reddit_st_ratings[reddit_st_ratings['most_positive_token'].isin(tokens_of_interest)]
filtered_df_news = news_st_ratings[news_st_ratings['most_positive_token'].isin(tokens_of_interest)]
# Sort the filtered DataFrame by positive_score in descending order
top_videos = filtered_df_youtube.drop_duplicates(['title']).sort_values(by="positive_score", ascending=False).head(3)
top_videos = top_videos[['title','url']]

top_reddit_posts = filtered_df_reddit.drop_duplicates(['Title']).sort_values(by="positive_score", ascending=False).head(3)
top_reddit_posts = top_reddit_posts[['Title','URL']]

top_news_articles = filtered_df_news.drop_duplicates(['title']).sort_values(by="positive_score", ascending=False).head(3)
top_news_articles = filtered_df_news[['title']]

print("Here are the top media sources for the tokens you are interested in: ")
print("Top Youtube Videos")
print(tabulate(top_videos, headers='keys', tablefmt='pretty'))
print("Top Reddit Posts")
print(tabulate(top_reddit_posts, headers='keys', tablefmt='pretty'))
print("Top News Articles")
print(tabulate(top_news_articles, headers='keys', tablefmt='pretty'))


print("Press 1 to Exit")
print("Press 2 for Investment Trigger Warning")
print("Press 3 for Bias Breaker")

b = input()
if b == '1':
    exit()
elif b == '2':
    tokens_of_interest = top_3_token
# Filter DataFrame for rows where the most_positive_token is in the list of interest

    filtered_df_youtube_tw = yt_st_ratings[yt_st_ratings['most_negative_token'].isin(tokens_of_interest)]
    filtered_df_reddit_tw = reddit_st_ratings[reddit_st_ratings['most_negative_token'].isin(tokens_of_interest)]
    iltered_df_news_tw = news_st_ratings[news_st_ratings['most_negative_token'].isin(tokens_of_interest)]
# Sort the filtered DataFrame by positive_score in descending order
    top_videos_tw = filtered_df_youtube_tw.drop_duplicates(['title']).sort_values(by="negative_score", ascending=True).head(3)
    top_videos_tw = top_videos_tw[['url','title']]

    top_reddit_posts_tw = filtered_df_reddit_tw.drop_duplicates(['Title']).sort_values(by="negative_score", ascending=True).head(3)
    top_reddit_posts_tw = top_reddit_posts_tw[['Title','URL']]

    top_news_articles_tw = iltered_df_news_tw.drop_duplicates(['title']).sort_values(by="negative_score", ascending=True).head(3)
    top_news_articles_tw = top_news_articles_tw[['title']]

    print("Here are the top media sources you should be aware of for the tokens you are interested in: ")
    print("Top Youtube Videos")
    print(tabulate(top_videos_tw, headers='keys', tablefmt='pretty'))
    print("Top Reddit Posts")
    print(tabulate(top_reddit_posts_tw, headers='keys', tablefmt='pretty'))
    print("Top News Articles")
    print(tabulate(top_news_articles_tw, headers='keys', tablefmt='pretty'))
elif b == '3':
    tokens_of_interest = top_3_token
    bias_dict = {"Ethereum": "Bitcoin", "Dogecoin": "Pepe"}

    def replace_tokens(token, replacements):
        return replacements.get(token, token)
    # Filter DataFrame for rows where the most_positive_token is in the list of interest

    filtered_df_youtube_bb = yt_st_ratings
    filtered_df_reddit_bb = reddit_st_ratings
    filtered_df_news_bb = news_st_ratings

    filtered_df_youtube_bb['most_positive_token'] = yt_st_ratings['most_positive_token'].apply(lambda x: replace_tokens(x, bias_dict))
    filtered_df_reddit_bb['most_positive_token'] = reddit_st_ratings['most_positive_token'].apply(lambda x: replace_tokens(x, bias_dict))
    filtered_df_news_bb['most_positive_token'] = news_st_ratings['most_positive_token'].apply(lambda x: replace_tokens(x, bias_dict))

    filtered_df_youtube_bb = filtered_df_youtube_bb[filtered_df_youtube_bb['most_positive_token'].isin(bias_dict.values())]
    filtered_df_reddit_bb = filtered_df_reddit_bb[filtered_df_reddit_bb['most_positive_token'].isin(bias_dict.values())]
    filtered_df_news_bb = filtered_df_news_bb[filtered_df_news_bb['most_positive_token'].isin(bias_dict.values())]
    # Sort the filtered DataFrame by positive_score in descending order
    top_videos_bb = filtered_df_youtube_bb.drop_duplicates(['title']).sort_values(by="positive_score", ascending=False).head(3)
    top_videos_bb = top_videos_bb[['url','title']]

    top_reddit_posts_bb = filtered_df_reddit_bb.drop_duplicates(['Title']).sort_values(by="positive_score", ascending=False).head(3)
    top_reddit_posts_bb = top_reddit_posts_bb[['Title','URL']]

    top_news_articles_bb = filtered_df_news_bb.drop_duplicates(['title']).sort_values(by="positive_score", ascending=False).head(3)
    top_news_articles_bb = top_news_articles_bb[['title']]
    print("Here are the top media sources to break your investment biases for the tokens you are interested in: ")
    print("Top Youtube Videos")
    print(tabulate(top_videos_bb, headers='keys', tablefmt='pretty'))
    print("Top Reddit Posts")
    print(tabulate(top_reddit_posts_bb, headers='keys', tablefmt='pretty'))
    print("Top News Articles")
    print(tabulate(top_news_articles_bb, headers='keys', tablefmt='pretty'))

