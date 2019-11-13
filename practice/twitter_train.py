from twitter_scraper import get_tweets

for tweet in get_tweets('nwilliams030', pages=1):
    print(tweet['text'])