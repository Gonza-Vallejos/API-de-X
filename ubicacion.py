from twikit import Client, TooManyRequests, TwitterException
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio
import os

MINIMUM_TWEETS = 100  # Cambia esto al número deseado de tweets
QUERY = 'lang:en since:2024-01-16 until:2024-09-25 '

async def get_tweets(client, tweets):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Obteniendo siguientes tweets en {wait_time} segundos...')
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
        writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes', 'Location'])

    # Autenticarse en X.com
    client = Client(language='en-US')

    try:
        # Verificar si existe el archivo de cookies
        if os.path.exists('cookies.json'):
            print('Cargando cookies...')
            client.load_cookies('cookies.json')
        else:
            print('Iniciando sesión con credenciales...')
            await client.login(auth_info_1=username, auth_info_2=email, password=password)
            client.save_cookies('cookies.json')
            print('Cookies guardadas en cookies.json')

    except TwitterException as e:
        print(f'Error al iniciar sesión: {e}')
        return

    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(client, tweets)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())  # Esperar hasta que se restablezca el límite
            continue
        except TwitterException as e:
            print(f'Error al obtener tweets: {e}')
            break

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = [
                tweet_count, 
                tweet.user.name, 
                tweet.text, 
                tweet.created_at, 
                tweet.retweet_count, 
                tweet.favorite_count, 
                tweet.place
            ]

            with open('tweets.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')

    print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')

if __name__ == '__main__':
    asyncio.run(main())
