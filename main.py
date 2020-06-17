import tweepy
import requests

import secrets


def get_timeline(account_type, since_id=None):
    auth = tweepy.OAuthHandler(secrets.KEYS[account_type]['CONSUMER_KEY'], secrets.KEYS[account_type]['CONSUMER_SECRET'])
    auth.set_access_token(secrets.KEYS[account_type]['ACCESS_TOKEN'], secrets.KEYS[account_type]['ACCESS_TOKEN_SECRET'])

    api = tweepy.API(auth)
    public_tweets = api.home_timeline(since_id=since_id, count=1500//140)

    max_id = None
    messages = []
    for tweet in public_tweets:
        message = '{}[{}]: {}'.format(tweet.user.name, tweet.user.screen_name, tweet.text)
        messages.append(message)
        if max_id is None or tweet.id > max_id:
            max_id = tweet.id

    resp = requests.post('http://localhost:7890/api/letter', data={
        'title': '트위터 {}'.format(account_type),
        'content': '\n'.join(messages),
        'sender': 'tweet-bot',
        'isPublic': True,
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
