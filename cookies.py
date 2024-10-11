from twikit import Client, TooManyRequests, TwitterException
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio

async def main():
    # Cargar credenciales desde el archivo config.ini
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

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
