import os
import pandas as pd
import logging
import json
import hashlib
from cryptography.fernet import Fernet
from kaggle.api.kaggle_api_extended import KaggleApi

# Configuración del logging
logging.basicConfig(filename="audit_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# Cargar credenciales de Kaggle
def authenticate_kaggle():
    try:
        os.environ["KAGGLE_CONFIG_DIR"] = os.getcwd()
        api = KaggleApi()
        api.authenticate()
        return api
    except Exception as e:
        logging.error(f"Error en la autenticación con Kaggle: {e}")
        raise Exception("No se pudo autenticar con Kaggle")

# Cargar configuración de usuarios
CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Archivo de configuración no encontrado.")
        raise Exception("Archivo de configuración no encontrado.")

config = load_config()

# Función para verificar credenciales
def verify_user(username, password):
    if username not in config["users"]:
        return False
    stored_hash = config["users"][username]["password"]
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return stored_hash == password_hash

# Verificar acceso
def check_access(username):
    if username not in config["users"]:
        logging.warning(f"Acceso denegado: Usuario {username} no registrado.")
        raise PermissionError("Acceso denegado: Usuario no registrado")
    return config["users"][username]["access_level"]

# Cargar o generar clave para cifrado
KEY_FILE = "secret.key"

def load_or_generate_key():
    try:
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

key = load_or_generate_key()
cipher_suite = Fernet(key)

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

def backup_data(df, filename="backup_data.csv"):
    df.to_csv(filename, index=False)
    logging.info(f"Backup realizado en {filename}")

def main():
    try:
        # Pedir credenciales al usuario
        username = input("Ingrese su usuario: ")
        password = input("Ingrese su contraseña: ").strip()

        if not verify_user(username, password):
            logging.warning(f"Intento de acceso fallido para {username}")
            raise PermissionError("Acceso denegado: Usuario o contraseña incorrectos")

        access_level = check_access(username)
        if access_level == "restricted":
            logging.warning(f"Acceso restringido para {username}")
            raise PermissionError("No tienes permisos para ejecutar este pipeline")

        logging.info(f"Usuario {username} ha iniciado sesión correctamente.")

        # Autenticación en Kaggle
        api = authenticate_kaggle()

        # Descargar el dataset de Kaggle
        dataset = "ruchikakumbhar/obesity-prediction"
        api.dataset_download_files(dataset, path="./", unzip=True)
        logging.info("Datos descargados exitosamente desde Kaggle")

        # Cargar el dataset
        filename = "Obesity prediction.csv"
        df = pd.read_csv(filename)
        logging.info("Datos extraídos con éxito.")

        # Hacer un backup antes de encriptar
        backup_data(df)

        logging.info("Datos cifrados correctamente.")

        # Guardar datos procesados una sola vez con el nombre correcto
        df.to_csv("obesity_dataset.csv", index=False)
        logging.info("Datos procesados guardados en obesity_dataset.csv")

        # Eliminar el archivo original descargado
        os.remove(filename)
        logging.info(f"Archivo {filename} eliminado correctamente.")

        # Correr modelo.ipynb

        # Verificar si hay un archivo modelo_final.pkl

        # Subir a Github el proyecto

        logging.info("Pipeline finalizado satisfactoriamente.")
        print("Pipeline ejecutado satisfactoriamente.")
    except Exception as e:
        logging.error(f"Error en el pipeline: {e}")
        print(f"Error en el pipeline: {e}")

if __name__ == "__main__":
    main()
