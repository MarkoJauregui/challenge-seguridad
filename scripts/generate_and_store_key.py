from cryptography.fernet import Fernet
import hvac
import os

# Generar una clave segura
key = Fernet.generate_key()
print(f"Generated encryption key: {key.decode()}")

# Configurar el cliente de Vault
vault_addr = os.getenv('VAULT_ADDR', 'http://vault:8200')
vault_token = os.getenv('VAULT_TOKEN', 'root')

client = hvac.Client(url=vault_addr, token=vault_token)

# Guardar la clave en Vault
client.secrets.kv.v2.create_or_update_secret(
    path='encryption-key',
    secret={'key': key.decode()}
)

print("Encryption key stored in Vault at 'secret/encryption-key'")
