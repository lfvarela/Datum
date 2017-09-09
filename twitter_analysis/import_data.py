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


        self.tweet_queue = []

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

    def get_query_terms(self):
        queries = {
            'track':['crypto', 'cryptocurrency', 'dat', 'datum', 'datum network', 'filecoin', 'enigma ico', 'enigma catalyst'],
            'follow':[]
        }
        return queries

    def start_stream(self, stream_listener):
        queries = self.get_query_terms()
        stream = Stream(self.auth, stream_listener)
        stream.filter(track=queries['track'], language='en')

class cryptoStreamListener(StreamListener):
    def __init__(self, tweet_queue):
        self.tweet_queue = tweet_queue

    def on_status(self, status):
        return

    def on_data(self, data):
        self.tweet_queue.push(data)
        if len(self.tweet_queue > 25):
            write_queue(self.tweet_queue)
        print(data)
        return

    def on_error(self, status_code):
            print('There was an error with status code')
            print(status_code)
            if status_code == 420:
                print('Recieved a 420 rate limit error, shutting down stream')
                #returning False in on_data disconnects the stream
                return False

def write_queue():
    return

def ingest_data():
    twitter = TwitterClient()
    twitter_queue = []
    stream_listener = cryptoStreamListener(twitter_queue)
    twitter.start_stream(stream_listener)
    twitter = TwitterClient()


ingest_data()
