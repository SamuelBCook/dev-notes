from pathlib import Path
import duckdb
from loguru import logger

# def careful_con(db_path:Path, *args, **kwargs):

#     def decorate(func):

#         with duckdb.connect(str(db_path)) as con: 

#             try:

#                 con.execute("BEGIN TRANSACTION;")

#                 value = func(con, *args, **kwargs)

#                 con.execute("COMMIT;")

#             except Exception as e:

#                 con.execute("ROLLBACK;")
#                 logger.error(f'Error - rolling back: {e}')
#                 raise

#         return value
    
#     return value



def careful_con(func):
    """Decorator: run a function inside a DuckDB transaction."""
    def wrapper(*args, db_path:Path, **kwargs):

        with duckdb.connect(str(db_path)) as con:
            try:
                con.execute("BEGIN TRANSACTION;")
                result = func(con, *args, **kwargs)
                con.execute("COMMIT;")
                return result
            
            except Exception as e:
                con.execute("ROLLBACK;")
                logger.error(f'Error - rolling back: {e}')
                raise

    return wrapper
