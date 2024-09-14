import tweepy
import os
from dotenv import load_dotenv

# Cargar las claves de API desde el archivo .env
load_dotenv()

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Autenticación
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creación del objeto API
api = tweepy.API(auth)

# Prueba de la API
try:
    user = api.verify_credentials()
    if user:
        print(f"Autenticación exitosa: {user.name}")
    else:
        print("No se pudo autenticar.")
except tweepy.TweepError as e:
    print(f"Error durante la autenticación: {e}")
