# dictio_bot
Creacion de un bot mediante la libreria Tweepy. Consiste en un bot que al mencionarlo en Twitter, te devuelve una descripción de la palabra haciendo webscrapping de la página oficial de la RAE.  Este bot esta modulado en varios ficheros principales: 
bot.py            --> Implementa toda la funcionalidad principal. 
config.py         --> Creacion de la API. 
diccionario.py    --> Palabras extra, son easter eggs. 
wordsNotFound.py  --> Palabras que no se han encontrado cuando alguien mencionaba al bot, utilizado para detectar posibles fallos del diccionario. 
listaPalabras.txt --> Todas las palabras de la RAE. 
startBot.sh       --> Script en bash que simplemente inicializa los tokens y ejecuta python3 ./bot.py  

(Anotación: Este código no se ha optimizado, hay muchas cosas que se podrían optimizar, simplemente fue un proyecto sencillo que hice por aburrimiento.)
