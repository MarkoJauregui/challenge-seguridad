# Challenge Seguridad 

## Descripción

Este proyecto utiliza FastAPI para crear un API que maneja usuarios y sus datos asociados. La información se almacena en una base de datos PostgreSQL.

## Estructura del Proyecto

- `app/`
  - `main.py`: Configuración y rutas principales de la aplicación.
  - `database.py`: Configuración de la conexión a la base de datos.
  - `models.py`: Definición de los modelos de datos.
  - `schemas.py`: Definición de los esquemas Pydantic.
  - `routers/`
    - `users.py`: Rutas y lógica para manejar usuarios.

## Instalación y Configuración

### Prerrequisitos

- Python 3.10
- PostgreSQL
- PIP
- Git

### Pasos de Instalación

1. Clonar el repositorio:

   ```sh
   git clone <URL-del-repositorio>
   cd challenge-seguridad
   ```

2. Crear y activar un entorno virtual:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instalar las dependencias:

   ```sh
   pip install -r requirements.txt
   ```

4. Configurar la base de datos PostgreSQL:

- Crear una base de datos y usuario en PostgreSQL.
- Actualizar la variable DATABASE_URL en el archivo .env con la cadena de conexión a la base de datos.

5. Ejecutar la aplicación:

   ```sh
   uvicorn app.main:app --reload
   ```

6. Acceder a la documentación automática de la API en:
   ```arduino
   http://127.0.0.1:8000/docs
   ```

## Funcionalidades Implementadas:

- Conexión a la base de datos PostgreSQL.
- Recuperación de datos de usuarios.
- Documentación automática con Swagger en /docs.

## Pasos Pendientes

1. **Validaciones**:

   - Añadir validaciones en los esquemas y rutas.
   - Verificar el manejo de errores.

2. **Funciones CRUD**:

   - Implementar las funciones de creación, actualización y eliminación de usuarios.

3. **Autenticación y Autorización**:

   - Añadir autenticación de usuarios (JWT, OAuth2, etc.).
   - Implementar autorización para diferentes roles de usuario.

4. **Pruebas**:

   - Crear pruebas unitarias y de integración.
   - Configurar CI/CD para ejecutar las pruebas automáticamente.

5. **Documentación**:

   - Completar la documentación de la API y del proyecto.
   - Añadir ejemplos de uso en el README.

6. **Despliegue**:
   - Configurar el despliegue en un servidor de producción.
   - Considerar el uso de Docker para el despliegue.

## Notas Adicionales

- Asegúrate de que la carpeta `venv` esté incluida en el `.gitignore` para evitar subir archivos innecesarios al repositorio.
- El archivo `.env` no debe ser incluido en el control de versiones por razones de seguridad.

## Autores

- **Marko Jauregui** - Desarrollador Principal

## Contacto

Para cualquier pregunta o problema, por favor contacta a [Marko Jauregui](https://www.linkedin.com/in/marko-jauregui/).
