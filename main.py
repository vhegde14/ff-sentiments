import tweepy
import local
from textblob import TextBlob
import math

player = input("Which football player do you want to analyze? (spelling is important)\n")
max_results = input("How many tweets do you want to search through? (maximum 100)\n")

client = tweepy.Client(bearer_token=local.BEARER_TOKEN)

query = player.lower() + " -is:retweet"
print("Creating a query: Analyze " + query + " for " + str(max_results) + " results")

negative_tweets, positive_tweets, neutral_tweets = [], [], []
polarity = 0
subjectivity = 0

def perform_sentiment_analysis(tweet):
    blob = TextBlob(tweet.text).sentiment
    global polarity
    global subjectivity
    # print(tweet)
    polarity += blob.polarity
    subjectivity += blob.subjectivity
    if blob.polarity < 0:
        negative_tweets.append(tweet.text)
    elif blob.polarity > 0:
        positive_tweets.append(tweet.text)
    else:
        neutral_tweets.append(tweet.text)

tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'], max_results=max_results)

print("Analyzing sentiment around " + player + " for " + str(max_results) + " results")
for tweet in tweets.data:
    # print(tweet)
    perform_sentiment_analysis(tweet)

total_tweets = len(negative_tweets) + len(positive_tweets) + len(neutral_tweets)
total_polarity = round((polarity / total_tweets), 5)
total_subjectivity = math.floor((subjectivity / total_tweets) * 100)
percentage_negative_tweets = round((len(negative_tweets) / total_tweets) * 100)
percentage_positive_tweets = round((len(positive_tweets) / total_tweets) * 100)
percentage_neutral_tweets = round((len(neutral_tweets) / total_tweets) * 100)

print("-----------------------------------------------------------------")
print(f"{player} Sentiment Analysis Results")
print(f"Positive Tweets: {percentage_positive_tweets}%")
print(f"Negative Tweets: {percentage_negative_tweets}%")
print(f"Neutral Tweets: {percentage_neutral_tweets}%")
if total_polarity > 0:
    print(f"Overall Sentiment is Positive: {total_polarity} with roughly {total_subjectivity}% subjectivity")
elif total_polarity < 0:
    print(f"Overall Sentiment is Negative: {total_polarity} with roughly {total_subjectivity}% subjectivity")
else:
    print(f"Overall Sentiment is Neutral: {total_polarity} with roughly {total_subjectivity}% subjectivity")
