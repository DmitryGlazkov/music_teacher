from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, inspect, text
import logging
from sqlalchemy.exc import DisconnectionError
import time

SQLALCHEMY_DATABASE_URI='postgresql://music_teacher_user:djembelessons@db:5432/djembe_teacher_db'
# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def init_database():
    """Инициализация базы данных"""
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    try:
        logger.info("Schema creation completed successfully")
    except Exception as e:
        logger.error(f"Error creating schema: {e}")
        raise
    finally:
        engine.dispose()

def run_migrations_with_retry(max_attempts=3, delay=4):
    """Запускает миграции с повторными попытками при ошибках подключения"""
    attempt = 0
    while attempt < max_attempts:
        try:
            run_migrations()
            return
        except DisconnectionError as e:
            attempt += 1
            if attempt == max_attempts:
                logger.error(f"Failed after {max_attempts} attempts: {e}")
                raise
            logger.warning(f"Connection error (attempt {attempt}/{max_attempts}): {e}")
            time.sleep(delay)

def run_migrations():
    try:
        # Инициализируем БД если её нет
        init_database()
        
        # Запускаем миграции
        alembic_cfg = Config("migrations/alembic.ini")
        command.upgrade(alembic_cfg, "head")
        
        # Проверяем, что все таблицы созданы
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        inspector = inspect(engine)
        required_tables = ['user', 'learning_process', 'lesson_price', 'text_data']
        existing_tables = inspector.get_table_names()
        
        missing_tables = set(required_tables) - set(existing_tables)
        if missing_tables:
            raise Exception(f"Missing tables after migration: {missing_tables}")
            
        logger.info("Migrations completed successfully")
        
    except DisconnectionError as e:
        logger.error(f"Database connection error: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during migrations: {e}")
        raise
    finally:
        engine.dispose()

def check_connection(engine):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            logger.info("Database connection check: OK")
            return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False

if __name__ == "__main__":
    run_migrations_with_retry()

