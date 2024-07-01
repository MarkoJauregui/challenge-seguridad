import hvac
import os
from cryptography.fernet import Fernet

vault_url = os.getenv('VAULT_URL', 'http://vault:8200')
vault_token = os.getenv('VAULT_TOKEN', 'root')
client = hvac.Client(url=vault_url, token=vault_token)

# Lee la clave de cifrado de Vault
vault_secret = client.secrets.kv.v2.read_secret_version(path='encryption-key')
print("Vault Secret:", vault_secret)  # Agrega esta línea para imprimir el contenido completo

# Ajuste basado en la estructura actual del diccionario
encryption_key = vault_secret['data']['data']['key'].encode()
cipher = Fernet(encryption_key)

def encrypt_data(data):
    if isinstance(data, str):
        data = data.encode()
    return cipher.encrypt(data).decode()  # Asegúrate de que se devuelva como cadena

def decrypt_data(token):
    if isinstance(token, str):
        token = token.encode()
    return cipher.decrypt(token).decode()  # Asegúrate de que se devuelva como cadena
