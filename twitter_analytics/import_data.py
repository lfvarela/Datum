#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class TwitterClient(object):
    '''
    Client for sentiment
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'EkyNqGmgBJc5wlY6Zc6YmgThg'
        consumer_secret = 'ZwGEqugdG37upAlr8yIlzfEyYS7AkIvpn92wGVZlXIltCuu5zv'
        access_token = '2176798724-DDdFopCRsnqcX2Y3GGTEiUAcpUEZC9GMjk1fceS'
        access_token_secret = 'YlrBQI2FHCYysTUASd0xgiQFABYmV8mAd4LPulAnyaZVi'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
            self.stream = Stream(auth, l)
        except:
            print("Error: Authentication Failed")


    def get_query_terms():
        queries = {
            'track':['crypto', 'cryptocurrency', 'dat', 'datum', 'datum network', 'filecoin', 'enigma ico', 'enigma catalyst']
            'follow':['']
        }

    def start_stream(self):
        stream_listener = StreamListener()
        stream = Stream(self.auth, stream_listener)
