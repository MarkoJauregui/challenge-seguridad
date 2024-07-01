from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# Añadir la ruta de tu aplicación para poder importar los módulos correctamente
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')

# Importar la base de datos y los modelos
from app.database import Base
from app import models  # Asegúrate de que todos los modelos están importados

# Configuración de Alembic
config = context.config

# Interpretar el archivo de configuración para Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Configurar la metadata de los modelos
target_metadata = Base.metadata

# Valores adicionales desde la configuración, definidos según las necesidades de env.py
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'.

    Configura el contexto solo con una URL y no un Engine.
    Al saltar la creación del Engine, ni siquiera necesitamos un DBAPI disponible.

    Las llamadas a context.execute() aquí emiten la cadena dada a la
    salida del script.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'.

    En este escenario necesitamos crear un Engine
    y asociar una conexión con el contexto.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
