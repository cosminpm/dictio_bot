#!/usr/bin/env python
# tweepy-bots/bots/autoreply.py

import tweepy
import logging
import requests
import re
import time

from config import create_api
from random import randint
from bs4 import BeautifulSoup

from diccionario import diccionario
from wordsNotFound import conjunto

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Abrir el diccionario de Easter Eggs
f = open("listaPalabras.txt","r")
listaPalabras = f.readlines()
f.close()

# Definimos una clase llamada definicion, que basicamente contendra un str y un booleano error para indicarnos si se ha encontrado o no.

class Def:
	def __init__(self,definicion,error):
		# Cero es NO hay error y uno es SI hay error
		self.definicion=""
		self.error=1

# Numero total de palabras en espaniol
NUMBER_OF_WORDS = 80163

def rindexList(alist, value):
    return len(alist)-alist[-1::-1].index(value)-1

# TODO Revisar
def check_mentions(api, since_id):
	d = Def("",1)	
	logger.info("Retrieving mentions")
	new_since_id = since_id
	for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
		
		# Para eliminar directamente los tuits de la timeline, se eliminan aquellos tuits simplemente dando "fav" al tuit.
		if not tweet.favorited:	
			new_since_id = max(tweet.id, new_since_id)
			tweet.favorite()
			#Para comprobar que no se invoca al bot para nada.
			longitud=len(tweet.text.lower().split())
			if not (longitud>1):
				d.definicion="Error, se ha invocado incorrectamente al bot, por favor mire la descripción."
			else:
				#palabra=tweet.text.lower().split()[1]
				list = tweet.text.lower().split()
				print(list)
				index = rindexList(list,"@dictiobot")
				palabra = list[index+1]
				#La primera palabra que va a buscar en el diccionario:
				if palabra == "random":
					d = especialBEW(palabra)
					if d.error == 1:
						pass
				else:
					d = busquedaEnWeb(palabra)
					
			logger.info(f"Answering to {tweet.user.name}")
			if d.error == 1:
				conjunto.add(palabra)
				with open("wordsNotFound.py","w") as f:
					f.write("conjunto="+str(conjunto))
				f.close

			stat = "@"+str(tweet.author.screen_name) + " " + d.definicion
			stat = stat[:275]
			api.update_status(status= (stat), in_reply_to_status_id=tweet.id,)
	del d
	return new_since_id

def main():

	api = create_api()
	since_id = 1
	while True:
		try:
			since_id = check_mentions(api, since_id)
			logger.info("Waiting...")
			time.sleep(60)
		except not KeyboardInterrupt:
			pass
		except KeyboardInterrupt:
			logger.error("Fin de programa por teclado.")


def especialBEW(palabra):
	d = Def("",1)
	# Si la busqueda en web falla a la primera, se vuelve a buscar
	contador = 0
	while d.error == 1 and contador<10:
		r = randint(1,NUMBER_OF_WORDS)
		palabra = listaPalabras[r]
		palabra = palabra[:-1]
		d = busquedaEnWeb(palabra)
		contador+=1
		print(d.definicion,d.error)
	if contador > 10:
		d.definicion = ""
		d.error = 1
	else:
		d.error = 0
		d.definicion = palabra + ": " + d.definicion
		if len(d.definicion) > 263:
			d.definicion = d.definicion[:-(len(palabra)+5)]+"..."
	return d


# Se devuelve el objeto d que es un tipo de definicion
def busquedaEnWeb(palabra):
	d = Def("",1)

	api = create_api()
	# Web scrapping
	url = "https://dle.rae.es/"+palabra
	pagina = requests.get(url)
	soup = BeautifulSoup(pagina.content, 'html.parser')
	results = soup.find( "meta", attrs = {"name":'twitter:description'})
	results = str(results)
	x = er_definicion.search(results)
	
	# Desde el 1 hasta -1 para eliminar las comillas respectivas
	d.definicion = x.group(1)[1:-1] 
	if d.definicion.startswith("Definici"):
		d.definicion = d.definicion[d.definicion.find("1"):]


	# Se comprueba la longitud del tuit
	if len(d.definicion) > 263:
		d.definicion = d.definicion[:-3]+"..." 
		d.error = 0
	if d.definicion.startswith("Versión electrónica "):
		# Se mira en el diccionario de Easter Eggs.
		if palabra in diccionario.keys():
			d.definicion = diccionario.get(palabra)
			d.error = 0
		# Si no se encuentra en el diccionario de easter eggs.
		else:
			d.definicion = "Error, la palabra no existe o no está añadida actualmente en el diccionario."
			d.error = 1	
	return d

if __name__ == "__main__":
	patron_definicion = r'("[^"]*")'
	er_definicion = re.compile(patron_definicion)  
	main()
