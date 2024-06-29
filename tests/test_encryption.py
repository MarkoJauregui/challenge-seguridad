from cryptography.fernet import Fernet
import os
import hvac

# Cargar las variables de entorno
vault_url = os.getenv('VAULT_ADDR')
vault_token = os.getenv('VAULT_TOKEN')

# Configurar cliente de Vault
vault_client = hvac.Client(url=vault_url, token=vault_token)

# Obtener la clave de encriptación desde Vault
vault_secret = vault_client.secrets.kv.v2.read_secret_version(path='encryption-key')  # Ajusta la ruta aquí
encryption_key = vault_secret['data']['data']['key'].encode()
cipher = Fernet(encryption_key)

def encrypt_data(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data: str) -> str:
    return cipher.decrypt(data.encode()).decode()

# Probar la encriptación y desencriptación
original_data = "test_data"
encrypted_data = encrypt_data(original_data)
decrypted_data = decrypt_data(encrypted_data)

print("Original Data:", original_data)
print("Encrypted Data:", encrypted_data)
print("Decrypted Data:", decrypted_data)
