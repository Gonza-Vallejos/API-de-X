from twikit import Client, TooManyRequests, TwitterException
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio

MINIMUM_TWEETS = 2000  # Cambia esto al número deseado de tweets
QUERY = 'lang:en since:2024-01-16 until:2024-09-25 geocode:-27.4698,-58.8303,50km'

async def get_tweets(client, tweets):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Obteniendo siguientes tweets {wait_time} seconds ...')
        await asyncio.sleep(wait_time)  # Usar await para sleep
        tweets = await tweets.next()  # Asegúrate de que esta línea es correcta

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
        # Iniciar sesión con credenciales
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
        print("Inicio de sesión exitoso")
        
        # Guardar las cookies después de iniciar sesión
        client.save_cookies('cookies.json')
        print("Cookies guardadas correctamente en 'cookies.json'")

    except TwitterException as e:
        print(f'Error al iniciar sesión: {e}')
        return

if __name__ == '__main__':
    # Ejecutar la función main usando asyncio
    asyncio.run(main())
