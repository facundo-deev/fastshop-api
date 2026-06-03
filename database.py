import psycopg2
# Esta libreria iteractua con el S.O. 
import os
# importamos (load_dotenv) para que pueda buscar y cargar los archivos .env que hay en la carpeta del proyecto
from dotenv import load_dotenv

# aca los carga y esta listo para usarse
load_dotenv()

def connection_database():
    conecction = psycopg2.connect(
            # aca usamos (os) como intermediario para que busque el archivo .env
            # usamos (.getenv) para obtener el valor de la variable y los colocamos en ("")
        host = os.getenv("DB_HOST"),
        port = os.getenv("DB_PORT"),
        database = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")
    )
    return conecction