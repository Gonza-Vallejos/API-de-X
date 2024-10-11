from random import randint
import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import Calendar
from datetime import datetime
from twikit import Client, TooManyRequests, TwitterException
import asyncio
import os
import csv
from configparser import ConfigParser

# Función que genera la query desde la interfaz gráfica
def generar_query():
    fecha_inicio = cal_inicio.get_date()
    fecha_fin = cal_fin.get_date()
    ubicacion = entry_ubicacion.get()
    numero_tweets = entry_numero_tweets.get()

    if not fecha_inicio or not fecha_fin or not ubicacion or not numero_tweets.isdigit():
        messagebox.showerror("Error", "Todos los campos son obligatorios y el número de tweets debe ser un valor numérico.")
        return

    QUERY = f'lang:en since:{fecha_inicio} until:{fecha_fin} "{ubicacion}"'
    global MINIMUM_TWEETS
    MINIMUM_TWEETS = int(numero_tweets)  # Convertir el valor ingresado en un entero
    
    # Iniciar la obtención de tweets sin cerrar la ventana
    asyncio.run(main(QUERY))

# Guardar el archivo CSV en una ubicación seleccionada por el usuario
def guardar_csv():
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
    if file_path:
        os.rename('tweets.csv', file_path)
        messagebox.showinfo("Archivo guardado", f"El archivo CSV se ha guardado en: {file_path}")

# Función para obtener tweets
async def get_tweets(client, tweets, QUERY):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Obteniendo siguientes tweets en {wait_time} segundos...')
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()

    return tweets

# Función principal que se ejecutará con la QUERY generada
async def main(QUERY):
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    with open('tweets.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes', 'Location'])

    client = Client(language='en-US')

    try:
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
            tweets = await get_tweets(client, tweets, QUERY)
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

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Generador de Query")

# Selector de fechas
label_fecha_inicio = tk.Label(ventana, text="Fecha de Inicio:")
label_fecha_inicio.pack()
cal_inicio = Calendar(ventana, selectmode='day', year=2024, month=1, day=1)
cal_inicio.pack()

label_fecha_fin = tk.Label(ventana, text="Fecha de Fin:")
label_fecha_fin.pack()
cal_fin = Calendar(ventana, selectmode='day', year=2024, month=9, day=25)
cal_fin.pack()

# Campo de texto para la ubicación
label_ubicacion = tk.Label(ventana, text="Ubicación (por ejemplo: 'Corrientes'):")
label_ubicacion.pack()
entry_ubicacion = tk.Entry(ventana)
entry_ubicacion.pack()

# Campo de texto para el número de tweets
label_numero_tweets = tk.Label(ventana, text="Número de Tweets:")
label_numero_tweets.pack()
entry_numero_tweets = tk.Entry(ventana)
entry_numero_tweets.pack()

# Botón para generar el QUERY
boton_generar = tk.Button(ventana, text="Generar Query", command=generar_query)
boton_generar.pack()

# Botón para guardar el CSV
boton_guardar = tk.Button(ventana, text="Guardar CSV", command=guardar_csv)
boton_guardar.pack()

# Ejecutar la ventana
ventana.mainloop()
