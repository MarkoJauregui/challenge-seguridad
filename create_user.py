import requests
from app.database import SessionLocal
from app import schemas, crud

# Crear una sesión de base de datos
db = SessionLocal()

# Datos del nuevo usuario
user = {
    'id': 1,
    'user_name': 'exampleuser',
    'password': 'examplepassword',
    'codigo_zip': '12345',
    'credit_card_num': '1234-5678-9876-5432',
    'credit_card_ccv': '123',
    'cuenta_numero': '123456789',
    'direccion': '123 Main St',
    'geo_latitud': '40.7128',
    'geo_longitud': '-74.0060',
    'color_favorito': 'blue',
    'foto_dni': 'http://example.com/photo.jpg',
    'ip': '192.168.1.1',
    'auto': 'Tesla',
    'auto_modelo': 'Model S',
    'auto_tipo': 'Sedan',
    'auto_color': 'Red',
    'cantidad_compras_realizadas': 10,
    'avatar': 'http://example.com/avatar.jpg',
    'fec_birthday': '2000-01-01T00:00:00Z',
    'fec_alta': '2021-01-01T00:00:00Z'
}

# Crear el usuario en la base de datos
crud.create_user(db, user)
