import os
import pandas as pd
import logging
import json
import hashlib
import subprocess
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

def decrypt_data(encrypted_data):
    return cipher_suite.decrypt(encrypted_data.encode()).decode()

def encrypt_dataframe(df, filename="encrypted_data.csv"):
    encrypted_df = df.applymap(lambda x: encrypt_data(str(x)))
    encrypted_df.to_csv(filename, index=False)
    logging.info(f"Datos encriptados y guardados en {filename}")

def decrypt_dataframe(filename="encrypted_data.csv", output_filename="decrypted_data.csv"):
    encrypted_df = pd.read_csv(filename)
    decrypted_df = encrypted_df.applymap(lambda x: decrypt_data(str(x)))
    decrypted_df.to_csv(output_filename, index=False)
    logging.info(f"Datos desencriptados y guardados en {output_filename}")
    return output_filename

def backup_data(df, filename="backup_data.csv"):
    df.to_csv(filename, index=False)
    logging.info(f"Backup realizado en {filename}")

def run_jupyter_notebook(notebook_path):
    try:
        subprocess.run(["jupyter", "nbconvert", "--to", "notebook", "--execute", notebook_path], check=True)
        logging.info(f"Notebook {notebook_path} ejecutado correctamente.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al ejecutar el notebook: {e}")
        raise Exception("Error al ejecutar el notebook")

def check_model_file(model_file="modelo_final.pkl"):
    if os.path.exists(model_file):
        logging.info("Modelo generado exitosamente.")
    else:
        logging.warning("El archivo modelo_final.pkl no fue encontrado.")
        raise FileNotFoundError("El archivo modelo_final.pkl no fue encontrado.")

def push_to_github():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Automated update from pipeline"], check=True)
        subprocess.run(["git", "push", "origin", "dev"], check=True)
        logging.info("Código subido exitosamente a GitHub.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error al subir a GitHub: {e}")
        raise Exception("Error al subir a GitHub")

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

        # Encriptar datos antes de su uso
        encrypt_dataframe(df)

        # Desencriptar datos antes de ejecutar el notebook
        decrypted_filename = decrypt_dataframe()

        # Ejecutar el notebook de entrenamiento del modelo
        run_jupyter_notebook("modelo.ipynb")

        # Eliminar el archivo desencriptado después del uso
        os.remove(decrypted_filename)
        logging.info(f"Archivo {decrypted_filename} eliminado después de la ejecución del notebook.")

        # Verificar si el modelo fue generado correctamente
        check_model_file()

        # Subir cambios a GitHub
        push_to_github()

        logging.info("Pipeline finalizado satisfactoriamente.")
        print("Pipeline ejecutado satisfactoriamente.")
    except Exception as e:
        logging.error(f"Error en el pipeline: {e}")
        print(f"Error en el pipeline: {e}")

if __name__ == "__main__":
    main()
