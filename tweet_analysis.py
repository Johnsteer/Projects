import tweepy
import numpy as np
import pandas as pd
import matplotlib
import textblob
import re
import time
import MySQLdb as Mysql
import string
import re
import requests

TWITTER_APP_KEY = 'DyMsBhvcdn6jgeD1GNsBtQ'
TWITTER_APP_SECRET = 'p4fcQvHOmSerFDjAoNzYVzkFe8KyS4lviOX3eGAMFU'
TWITTER_KEY = '372430501-kUSVMdwC4F9MOx7tBz2g1wmbptYkZko30roFaRgt'
TWITTER_SECRET = 'bxxX5cwd907ZNJia7QJFHqTxed47RMbU5GMXtRoOM'

auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
api = tweepy.API(auth)

host, user, password, db = '10.142.0.3', 'tutor', 'Smith@234', 'sandbox_tweets'
connection = Mysql.connect(host=host, user=user, password=password, db=db)
cursor = connection.cursor()


def clean_tweet(tweet):
    """
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def analize_sentiment(tweet):
    """
    Utility function to classify the polarity of a tweet
    using textblob.
    """
    analysis = textblob.TextBlob(clean_tweet(tweet))
    return analysis


class StreamListener(tweepy.StreamListener):
    def __init__(self):
        super(StreamListener, self).__init__()

    def on_status(self, status):
        if hasattr(status, 'retweeted_status'):
            if status.retweeted_status:
                return

        if status.is_quote_status:
            return

        try:
            if hasattr(status, 'extended_tweet'):
                text = status.extended_tweet["full_text"]
            else:
                text = status.text
        except:
            time.sleep(5)

        tweet_length = len(text)
        tweet_id = status.id
        tweet_datetime = status.created_at
        tweet_source = status.source.replace("'", "").replace('"', '')

        tweet_polarity = np.array([analize_sentiment(text).sentiment.polarity])[0]
        tweet_subjectivity = np.array([analize_sentiment(text).sentiment.subjectivity])[0]

        print(text, "\n", tweet_length, tweet_id, tweet_datetime, tweet_source, tweet_polarity, tweet_subjectivity,
              "\n")
        try:
            cursor.execute("INSERT INTO tweets_tweet (twitter_id, length, source, date, polarity, subjectivity) VALUES"
                       "({twitter_id}, {length}, '{source}', '{date}', {polarity}, {subjectivity})".
                       format(twitter_id=tweet_id, length=tweet_length, source=tweet_source, date=tweet_datetime,
                              polarity=tweet_polarity, subjectivity=tweet_subjectivity))
            connection.commit()
        except:
            pass


stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')
stream.filter(track=["trump"])

tweet_id = 1099911965047087105
status = api.get_status(tweet_id)

text = ''

while True:
    if hasattr(status, 'retweeted_status'):
        if status.retweeted_status:
            break
    if status.is_quote_status:
        break
    if hasattr(status, 'extended_tweet'):
        text = status.extended_tweet["full_text"]
        break
    else:
        text = status.text
        break

print(text)
