import tweepy
import requests

import secrets


def get_timeline(account_type, since_id=None):
    auth = tweepy.OAuthHandler(secrets.KEYS[account_type]['CONSUMER_KEY'], secrets.KEYS[account_type]['CONSUMER_SECRET'])
    auth.set_access_token(secrets.KEYS[account_type]['ACCESS_TOKEN'], secrets.KEYS[account_type]['ACCESS_TOKEN_SECRET'])

    api = tweepy.API(auth)
    public_tweets = api.home_timeline(since_id=since_id, count=100)

    messages = []
    for tweet in public_tweets:
        message = '{}: {}'.format(tweet.user.name, tweet.text)
        messages.append(message.replace('\n', ' '))

    resp = requests.post('http://localhost:7890/api/letter', data={
        'title': '트위터 {}'.format(account_type),
        'content': '|'.join(messages),
        'sender': 'tweet-bot',
        'isPublic': False,
    })
    print(resp)
    try:
        print(resp.content.decode())
    except:
        pass


if __name__ == '__main__':
    get_timeline('public')
    get_timeline('private')
    get_timeline('game')
