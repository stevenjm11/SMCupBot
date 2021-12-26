#!/usr/bin/env python3
# Created by Steven Morgan

# Import libraries
import tweepy
import pandas

# Set up Keys
API_KEY = ws.environment['API_KEY']
API_SECRET_KEY = ws.environment['API_SECRET_KEY']
ACCESS_TOKEN = ws.environment['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = ws.environment['ACCESS_TOKEN_SECRET']

# Authenticate
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Follow back the previous 10 followers
for follower in api.get_followers(count = 10):
    api.create_friendship(user_id = follower.id)

# Key phrases that will trigger replies
KEY_PHRASES = ["who holds the cup", "who has the cup"]

# Read in the last 10 years of results
df = pandas.read_csv("history.csv").tail(10)

# Consider the last 10 mentions and reply if they include one of the key phrases
# Reply with the current holder of the cup and the previous 10 winners represented as emoji.
# Like the mention and follow the user who posted it.
for tweet in api.mentions_timeline(count = 10):
    if (KEY_PHRASES[0] in tweet.text.lower() and not tweet.favorited) or (KEY_PHRASES[1] in tweet.text.lower() and not tweet.favorited):
        current_winner = df.iloc[-1,1]
        past_winners = "".join(df.iloc[:,2])
        decade_inteval = "(" + str(df.iloc[0,0]) + "-" + str(df.iloc[9,0]) + ")"
        reply_text = "The " + current_winner + " are the current holders of the Sargeant-McKinnis Cup. \n\n10 year history " + decade_inteval + ": " + past_winners
        api.update_status(status=reply_text, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
        api.create_favorite(tweet.id)
        api.create_friendship(user_id = tweet.user.id)

# Key phrases that will trigger a like and retweet if posted from a set  of official acounts.
SM_KEY_PHRASES = ["sargeant-mckinnis", "sargeant mckinnis"]

# Set of official accounts
OFFICIAL_ACCOUNTS = ["@MelbourneVixens", "@NSWSwifts", "@SuperNetball", "@NetballAust"]

# For the latest 3 tweets from each of the official accounts, if they contain one of the key phrases, like and retweet.
for account in OFFICIAL_ACCOUNTS:
    latest_tweets = api.user_timeline(count = 3, screen_name = account, include_rts = True, exclude_replies = True)
    for tweet in latest_tweets:
        if (SM_KEY_PHRASES[0] in tweet.text.lower() and not tweet.favorited) or (SM_KEY_PHRASES[1] in tweet.text.lower() and not tweet.favorited):
            api.retweet(tweet.id)
            api.create_favorite(tweet.id)
