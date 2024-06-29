# Challenge Seguridad

Este proyecto se ha desarrollado para obtener información de clientes desde un proveedor externo, garantizar que la información esté asegurada en todos sus estados y disponibilizar recursos para que la misma sea accesible por distintos sectores dentro de la empresa.

## Objetivo

El objetivo es consumir y almacenar datos de manera segura en una base de datos relacional, y disponibilizar esta información para que distintos equipos y aplicaciones de la empresa puedan consumirla.

## Endpoints

### Obtener y almacenar usuarios

**GET /users**

Este endpoint obtiene los datos de los usuarios desde el proveedor externo y los almacena en la base de datos.

**Respuesta Exitosa**

```json
{
	"message": "Users fetched and stored successfully."
}
```

### Listar usuarios internos

**GET /internal-users**

Este endpoint lista los usuarios almacenados en la base de datos, con los datos sensibles encriptados y desencriptados para la visualización.

**Parámetros de Consulta**

- `skip` (opcional): Omitir registros. Default: 0
- `limit` (opcional): Límite de registros. Default: 10

**Respuesta Exitosa**

```json
[
	{
		"user_name": "exampleuser",
		"codigo_zip": "12345",
		"credit_card_num": "****",
		"credit_card_ccv": "****",
		"cuenta_numero": "****",
		"direccion": "123 Main St",
		"geo_latitud": "40.7128",
		"geo_longitud": "-74.0060",
		"color_favorito": "blue",
		"foto_dni": "http://example.com/photo.jpg",
		"ip": "192.168.1.1",
		"auto": "Toyota",
		"auto_modelo": "Corolla",
		"auto_tipo": "Sedan",
		"auto_color": "Red",
		"cantidad_compras_realizadas": 5,
		"avatar": "http://example.com/avatar.jpg",
		"fec_birthday": "1990-01-01T00:00:00",
		"fec_alta": "2021-01-01T00:00:00",
		"id": 1
	}
]
```

### Autenticación

**POST /token**

Este endpoint genera un token de acceso basado en las credenciales proporcionadas.

**Cuerpo de la Solicitud**

```json
{
	"username": "exampleuser",
	"password": "examplepassword"
}
```

**Respuesta Exitosa**

```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

## Configuración del Entorno

### Variables de Entorno

Asegúrate de definir las siguientes variables de entorno en un archivo `.env`:

```
SQLALCHEMY_DATABASE_URL=postgresql://challenge_user:newpassword@localhost/challenge_db
VAULT_ADDR=http://127.0.0.1:8200
VAULT_TOKEN=hvs.CAESIJIIem80M-hmIjtlhjqkzowsRGIX5mwPq1A0AbfA30bZGh4KHGh2cy5ldGhjaDFDaGVlYUZIeHJPUUY2UUM1aEw
VAULT_SKIP_VERIFY=true
SECRET_KEY=79be785431976e770e08d1c7439b6d97a3ddc73aa3dcfe43ade0ee383d8acfca
```

### Inicializar Vault

Para inicializar y configurar Vault, sigue los siguientes pasos:

1. Iniciar Vault en modo de desarrollo:

```bash
vault server -dev
```

2. Configurar el token de Vault y la clave de encriptación:

```
export VAULT_ADDR='http://127.0.0.1:8200'
vault login <root_token>
vault kv put secret/encryption-key key=$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
```

### Crear la base de datos

1. Acceder a PostgreSQL y crear la base de datos:

```bash
psql -U postgres
CREATE DATABASE challenge_db;
CREATE USER challenge_user WITH ENCRYPTED PASSWORD 'newpassword';
GRANT ALL PRIVILEGES ON DATABASE challenge_db TO challenge_user;
```

2. Configurar la autenticación en PostgreSQL editando el archivo `pg_hba.conf`:

```bash
# Editar el archivo /etc/postgresql/14/main/pg_hba.conf y cambiar:
local   all             postgres                                peer
# a:
local   all             postgres                                md5
```

3. Reiniciar el servicio de PostgreSQL:

```bash
sudo service postgresql restart
```

### Ejecutar la aplicación

1. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

2. Iniciar la aplicación:

```
uvicorn main:app --reload
```
