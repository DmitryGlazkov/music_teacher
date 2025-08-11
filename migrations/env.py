import logging
import os
import sys
from logging.config import fileConfig

from alembic import context

# Добавьте путь к корню проекта, где находится __init__.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируйте db из вашего пакета
from music_teacher import db

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Получаем строку подключения из файла alembic.ini
target_url = config.get_main_option("sqlalchemy.url")


def get_engine():
    """Возвращает SQLAlchemy Engine на основе строки подключения."""
    from sqlalchemy import create_engine
    return create_engine(target_url)


def get_metadata():
    return db.Model.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=target_url,
        target_metadata=get_metadata(),
        literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    from logging.config import fileConfig

    from alembic import context
    from sqlalchemy import create_engine

    # Инициализация конфигурации
    config = context.config
    fileConfig(config.config_file_name)

    # Создание движка
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url")
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            # другие параметры, если нужны
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()