import tweepy, time, os, random, threading
from datetime import datetime
import config, algorithm, logs

client = tweepy.Client(config.token, config.api_key, config.api_secret, config.access_token, config.access_token_secret)

# Created by Henrique: github.com/henriquelmeeee // 2022
# v2.0

# The code below retweets Linux-related tweets and uses the algorithm located in "algorithm.py" for checking.

def retweet(tweetid : int):
    try:
        api = tweepy.API(auth)
        api.retweet(tweetid)
        return True
    except Exception as error:
        print(f"Um erro ocorreu ao tentar retweetar o tweet de ID {tweetid}: {str(error)}")
        return False

class MyStream(tweepy.StreamingClient):

    def on_connect(self):
        print(
            f"Bot iniciado"
        )

    def on_tweet(self, tweet):
        try:
            if 'BOT DA GÁVEA' in tweet.text and ' ' in tweet.text or '@RT_FLAMENGUISTA' in tweet.text and ' ' in tweet.text:
                retweet(tweet.id)
            else:
                now = datetime.now()
                if algorithm.check(tweet.text, is_replie=False if tweet.referenced_tweets is None else True) and retweet(tweet.id):
                    print(f'{now} | Tweet de ID {tweet.id} retweetado com sucesso!')
                    config.retweeted_today += 1
                    time.sleep(random.randint(50, 100))
        except Exception as error:
            print('--------------------' + str(error) + '--------------------')

    def on_connection_error(self):
        print("Um erro na conexão foi encontrado, o cliente esperará 1 minuto até voltar a funcionar...")
        time.sleep(60)


stream = MyStream(bearer_token=config.token)
add_rules = False # set it to "True" if you need to add the rules

if add_rules:
    try:
        for word in config.words:
            stream.add_rules(
                tweepy.StreamRule(word)
            )
    except Exception as erro:
        print(f"Um erro ocorreu!\n'{str(erro)}'\nO bot irá continuar a funcionar mesmo assim.")
        
os.system('clear')

print('Iniciando logs...')
os.system('rm -rf __pycache__ && echo "Iniciando bot..."')

log = threading.Thread(name='logs', target=logs.logs)
log.start() # Start logs system in background because it will be running in loop

auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

stream.filter(tweet_fields=["referenced_tweets"])