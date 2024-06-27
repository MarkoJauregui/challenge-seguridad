# src/config.py
from dotenv import load_dotenv
import os

load_dotenv()

VAULT_ADDR = os.getenv('VAULT_ADDR')
VAULT_TOKEN = os.getenv('VAULT_TOKEN')
