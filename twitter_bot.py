import tweepy
import time

# Consumers API
CONSUMER_API_KEY = "Gb3K3OcnoI2kYxLMKI6obcLfI"
CONSUMER_SECRET_KEY = "n4pHeqjWf4au6Del7EDK5ie4TzIUWLLJj1jY6J2YONu6HZSa7O"

# Access tokens
ACCESS_TOKEN = "1393943501134471170-DlJHrUdiXXb440yrdBFLFsTVO0UM4E"
ACCESS_SECRET_TOKEN = "0NidITPkAiAgozl0nldR9Wk0VhpNeNR6X6FU2A9u2k4P3"

# Setting authentication for Twitter API
auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)

api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
user = api.me

# Keywords as a List in lower case that is going to be searched
SEARCH_KEYWORDS_LIST = ['testing-keyword']
# Converting Keywords to string adding OR in between
SEARCH_KEYWORDS = ' AND '.join(SEARCH_KEYWORDS_LIST)
# Adding -filter:retweets to filter out retweets
SEARCH_KEYWORDS += ' -filter:retweets'
# Adding -filter:username to filter out users
SEARCH_KEYWORDS += ' -from:@username '
# Adding -filter:keyword
SEARCH_KEYWORDS += ''
# Maximum number of tweets that the API will return
NUMBER_OF_TWEETS = 20
# How many seconds the code will stop before retweeting and liking again
SLEEP_SECONDS = 10

while True:
    for tweet in tweepy.Cursor(api.search, SEARCH_KEYWORDS).items(NUMBER_OF_TWEETS):
        try:
            # If the keyword is in the text of the twitt (excluding the username and other parts)
            # then retweets and likes it.

            # Check if any keyword is in text of the tweet
            condition1 = any(keyword in tweet.text.lower() for keyword in SEARCH_KEYWORDS_LIST)
            # Check if any of the keywords are not in user_mentions
            condition2 = not any(keyword in user_mention['screen_name'].lower() for keyword in SEARCH_KEYWORDS_LIST for user_mention in tweet.entities['user_mentions'])

            if condition1 and condition2:
                tweet.retweet()
                print('Retweet published successfully.')
                time.sleep(SLEEP_SECONDS)

        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

    # Stoping X seconds and trying again to avoid the restrictions getting twitts.
    # Which are 180 twitts per 15 mins.
    time.sleep(30)