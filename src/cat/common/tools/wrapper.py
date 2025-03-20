import logging
import time
from functools import wraps

from sqlalchemy.orm import Session

from src.cat.common.config.Config import Config

logger = logging.getLogger(__name__)


def with_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db: Session = next(Config.get_db())
        try:
            result = func(*args, db, **kwargs)
            return result
        finally:
            db.close()

    return wrapper


def with_session_commit(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        db: Session = next(Config.get_db())
        try:
            result = func(self, db, *args, **kwargs)
            db.commit()
            return result
        except Exception as e:
            db.rollback()
            raise
        finally:
            db.close()

    return wrapper


def time_counter(logger_name=__name__):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 获取指定的 logger
            logger = logging.getLogger(logger_name)

            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()

            elapsed_time_seconds = end_time - start_time
            elapsed_time_minutes = int(elapsed_time_seconds // 60)
            elapsed_time_seconds = int(elapsed_time_seconds % 60)

            logger.info(f"Function [{func.__name__}] cost: {elapsed_time_minutes} min {elapsed_time_seconds} sec.")

            return result

        return wrapper

    return decorator


def retry_wrapper(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry = max_retries
            while retry > 0:
                try:
                    if retry < max_retries:
                        time.sleep(2 * (max_retries - retry))
                    return func(*args, **kwargs)
                except Exception as e:
                    retry -= 1
                    if retry == 0:
                        raise e

        return wrapper

    return decorator
