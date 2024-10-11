from twikit import Client, TooManyRequests, TwitterException
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio
import os

MINIMUM_TWEETS = 100  # número deseado de tweets


QUERY = 'lang:en since:2024-01-16 until:2024-09-25 geocode:-27.4698,-58.8303,50km'

async def obtener_tweets(client, tweets):
    if tweets is None:
        print(f'{datetime.now()} - Obteniendo tweets...')
        tweets = await client.search_tweet(QUERY, product='Latest')
    else:
        tiempo_espera = randint(5, 10)
        print(f'{datetime.now()} - Obteniendo siguientes tweets en {tiempo_espera} segundos...')
        await asyncio.sleep(tiempo_espera)
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
        writer.writerow(['Número_Tweet', 'Usuario', 'Texto', 'Creado En', 'Retweets', 'Me Gusta', 'Ubicación'])

    # Autenticarse en X.com
    client = Client(language='es-ES')

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

    cuenta_tweets = 0
    tweets = None

    while cuenta_tweets < MINIMUM_TWEETS:
        try:
            tweets = await obtener_tweets(client, tweets)
        except TooManyRequests as e:
            reinicio_limite = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Se alcanzó el límite de solicitudes. Esperando hasta {reinicio_limite}')
            tiempo_espera = reinicio_limite - datetime.now()
            await asyncio.sleep(tiempo_espera.total_seconds())  # Esperar hasta que se restablezca el límite
            continue
        except TwitterException as e:
            print(f'Error al obtener tweets: {e}')
            break

        if not tweets:
            print(f'{datetime.now()} - No se encontraron más tweets')
            break

        # Recorre y guarda los tweets en el archivo CSV
        for tweet in tweets:
            cuenta_tweets += 1
            datos_tweet = [
                cuenta_tweets, 
                tweet.user.name, 
                tweet.text, 
                tweet.created_at, 
                tweet.retweet_count, 
                tweet.favorite_count, 
                tweet.place
            ]

            with open('tweets.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(datos_tweet)

        print(f'{datetime.now()} - Se obtuvieron {cuenta_tweets} tweets')

    print(f'{datetime.now()} - ¡Hecho! Se obtuvieron {cuenta_tweets} tweets')

if __name__ == '__main__':
    asyncio.run(main())

