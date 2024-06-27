from cryptography.fernet import Fernet, InvalidToken
import os
import hvac

# Cargar las variables de entorno
vault_url = os.getenv('VAULT_ADDR')
vault_token = os.getenv('VAULT_TOKEN')

# Configurar cliente de Vault
vault_client = hvac.Client(url=vault_url, token=vault_token)

# Obtener la clave de encriptación desde Vault
vault_secret = vault_client.secrets.kv.v2.read_secret_version(path='encryption-key')
encryption_key = vault_secret['data']['data']['key'].encode()
cipher = Fernet(encryption_key)

def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data: str) -> str:
    try:
        return cipher.decrypt(data.encode()).decode()
    except InvalidToken as e:
        raise ValueError("Invalid token for decryption") from e
