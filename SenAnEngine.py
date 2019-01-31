import configparser
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt


def start():
    # Get the credentials from the .ini file
    twitter_credentials = configparser.ConfigParser()
    twitter_credentials.read("twitter_credentials.ini")
    consumer_key = twitter_credentials["TWITTER"]["consumer_key"]
    consumer_secret = twitter_credentials["TWITTER"]["consumer_secret"]
    access_token_key = twitter_credentials["TWITTER"]["access_token_key"]
    access_token_secret = twitter_credentials["TWITTER"]["access_token_secret"]
    authenticate(consumer_key, consumer_secret, access_token_key, access_token_secret)


def authenticate(consumer_key, consumer_secret, access_token_key, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)
    # Call get_data() and pass api object as parameter
    get_data(api)


def get_data(api):
    # Get the keyword from the user
    keyword = input("Enter the keyword/hashtag to search: ")
    # Set the total number of tweets to retrieve
    count = 100
    # Get the data
    public_tweets = api.search(keyword, count=count, lang="en")
    tweet_list = []
    for tweet in public_tweets:
        tweet_list.append(tweet.text)
    analyze(tweet_list, count, keyword)


def percentage(a, b):
    return float(a) / float(b) * 100


def analyze(tweet_list, count, keyword):
    # This function is responsible for performing basic analytics
    neutral = 0
    positive = 0
    negative = 0
    polarity = 0
    for tweet in tweet_list:
        analysis = TextBlob(tweet)
        polarity += analysis.sentiment.polarity

        if analysis.sentiment.polarity == 0:
            neutral += 1
        elif analysis.sentiment.polarity < 0.00:
            negative += 1
        elif analysis.sentiment.polarity > 0.00:
            positive += 1
    positive = percentage(positive, count)
    negative = percentage(negative, count)
    neutral = percentage(neutral, count)

    positive = format(positive, ".2f")
    negative = format(negative, ".2f")
    neutral = format(neutral, ".2f")
    result(polarity, positive, negative, neutral, keyword, count)


def result(polarity, positive, negative, neutral, keyword, count):
    print("###Analytics Complete###")
    print(f"How people are reacting overall on {keyword} by analyzing {count} number of tweets: ")
    if polarity == 0:
        print("Neutral")
    elif polarity < 0:
        print("Negative")
    elif polarity > 0:
        print("Positive")

    labels = [f"Positive {positive}%]", f"Neutral {neutral}%]", f"Negative {negative}%]"]
    sizes = [positive, neutral, negative]
    colors = ["yellowgreen", "gold", "red"]
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title(f"How people are reacting overall on {keyword} by analyzing {count} number of tweets: ")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


start()
