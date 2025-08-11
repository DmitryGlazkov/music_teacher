import logging
import time
import os
import sys

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

# Конфигурация
SQLALCHEMY_DATABASE_URI = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    "postgresql://music_teacher_user:djembelessons@db:5432/djembe_teacher_db"
)
ALEMBIC_CONFIG_PATH = os.getenv("ALEMBIC_CONFIG_PATH", "migrations/alembic.ini")
REQUIRED_TABLES = ['user', 'learning_process', 'lesson_price', 'text_data']
MAX_DB_CONNECTION_ATTEMPTS = 5
RETRY_DELAY = 3

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Кастомное исключение для ошибок базы данных"""
    pass

def wait_for_database():
    """
    Ожидает доступность базы данных.
    Возвращает engine при успехе или None при неудаче.
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    
    for attempt in range(1, MAX_DB_CONNECTION_ATTEMPTS + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("Database connection established")
                return engine
        except OperationalError as e:
            if attempt == MAX_DB_CONNECTION_ATTEMPTS:
                logger.error(f"Failed to connect to database after {MAX_DB_CONNECTION_ATTEMPTS} attempts")
                return None
            logger.warning(f"Database connection attempt {attempt}/{MAX_DB_CONNECTION_ATTEMPTS} failed. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
    
    return None

def verify_tables(engine):
    """
    Проверяет наличие всех необходимых таблиц.
    Возвращает список отсутствующих таблиц.
    """
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        missing_tables = [table for table in REQUIRED_TABLES if table not in existing_tables]
        
        if missing_tables:
            logger.warning(f"Missing tables: {', '.join(missing_tables)}")
        else:
            logger.info("All required tables exist")
            
        return missing_tables
    except SQLAlchemyError as e:
        logger.error(f"Error verifying tables: {str(e)}")
        raise DatabaseError(f"Table verification failed: {str(e)}")

def apply_migrations():
    """Применяет миграции Alembic"""
    try:
        alembic_cfg = Config(ALEMBIC_CONFIG_PATH)
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations applied successfully")
    except Exception as e:
        logger.error(f"Failed to apply migrations: {str(e)}")
        raise DatabaseError(f"Migration failed: {str(e)}")

def main():
    """Основная логика выполнения миграций"""
    logger.info("Starting database migration process")
    
    # Шаг 1: Ожидание доступности БД
    engine = wait_for_database()
    if not engine:
        logger.error("Database is not available")
        sys.exit(1)
    
    try:
        # Шаг 2: Применение миграций
        apply_migrations()
        
        # Шаг 3: Проверка таблиц
        missing_tables = verify_tables(engine)
        if missing_tables:
            logger.error(f"Migration incomplete: missing tables detected")
            sys.exit(1)
            
        logger.info("Database migration completed successfully")
        sys.exit(0)
        
    except DatabaseError as e:
        logger.error(f"Migration process failed: {str(e)}")
        sys.exit(1)
    finally:
        engine.dispose()

if __name__ == "__main__":
    main()