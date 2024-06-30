# Challenge Seguridad

## Descripción

Este proyecto es un API para la gestión de usuarios y autenticación interna. Utiliza FastAPI y SQLAlchemy para manejar las operaciones de base de datos y la autenticación.

## Requisitos

- Python 3.10+
- PostgreSQL
- Entorno virtual de Python
- [Poetry](https://python-poetry.org/) (opcional, pero recomendado)
- [Docker](https://www.docker.com/) (opcional, para simplificar la configuración de la base de datos)

## Configuración

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd challenge-seguridad
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crea un archivo `.env` en el directorio raíz del proyecto con las siguientes variables:

```env
SECRET_KEY=<tu_secret_key>
SQLALCHEMY_DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
VAULT_ADDR=<vault_address>
VAULT_TOKEN=<vault_token>
```

### 5. Crear la base de datos y las tablas

Asegúrate de que PostgreSQL está en funcionamiento y ejecuta el siguiente comando:

```bash
python create_internal_users.py
```

Este script creará las tablas necesarias y añadirá usuarios internos con roles de administrador y usuario regular.

### 6. Ejecutar la aplicación

```bash
uvicorn main:app --reload
```

La aplicación estará disponible en `http://127.0.0.1:8000`.

## Uso

### Obtener token de acceso

Para obtener un token de acceso, realiza una solicitud `POST` a `/token` con los siguientes parámetros en el body (x-www-form-urlencoded):

```
username: adminuser
password: adminpassword
```

### Obtener usuarios externos

Realiza una solicitud `GET` a `/users` para obtener y almacenar usuarios desde el proveedor externo.

### Obtener usuarios internos

Realiza una solicitud `GET` a `/internal-users` con el token de acceso como Bearer token en el encabezado de autorización.

## Autores

- **Marko Jauregui**
- **Colaboradores**

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT.
