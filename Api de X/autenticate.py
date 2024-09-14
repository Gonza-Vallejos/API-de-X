import tweepy

'''
Función utilizada para utilizar la Api de Twitter
'''
def get_auth():
    consumer_key ='7nqMJZGsZso4OJuvRwykiIubG'
    consumer_secret ='Dq3uPPvvvDHVbWFduct1I4cHXTcRd5TtlaBJoQPUnuuKRy9N4l'
    access_token ='WTJCZl81azZGWlpQZkUtNEVhZWo6MTpjaQ'
    access_token_secret ='zq7qRpnvtdLzBzfdrai-zMnZvI246OLUFgoMixdGxFONshlmOn'
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth
