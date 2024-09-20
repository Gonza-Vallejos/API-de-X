from twikit import Client, TooManyRequests, TwitterException
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio

MINIMUM_TWEETS = 1000  # Cambiar por la cantidad de tweets deceados
QUERY = 'Corrientes lang:es since:2024-08-20 until:2024-09-20'  # Busca tweets que mencionen "Corrientes"

async def get_tweets(client, tweets):
    if tweets is None:
        print(f'{datetime.now()} - obteniendo tweets...')
        tweets = await client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        await asyncio.sleep(wait_time)  
        tweets = await tweets.next() 

    return tweets

async def main():
    # Cargar credenciales desde el archivo config.ini
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    # Crear un archivo CSV para los tweets
    with open('tweets.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Contador de Tweets', 'npmbre de usuario', 'Texto', 'Created At', 'Retweets', 'Likes'])

    # Autenticarse en X.com
    client = Client(language='en-US') #Idioma original en ingles

    try:
        # Iniciar sesión con credenciales que obtubimos del archivo config.ini
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
    except TwitterException as e:
        print(f'Error al iniciar sesión: {e}')
        return

    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS: # recorre hasta obtener la cantidad de tweets que pusimos como minimo
        try:
            tweets = await get_tweets(client, tweets)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds()) 
            continue
        except TwitterException as e:
            print(f'Error al obtener tweets: {e}')
            break

        if not tweets:
            print(f'{datetime.now()} - No se encontraron mas tweets')
            break


        #recorre y va guardando uno por uno los tweets en el archivo tweets.csv
        for tweet in tweets: 
            tweet_count += 1
            tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
            
            with open('tweets.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')

    print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')

if __name__ == '__main__':
    asyncio.run(main()) 
