import pymysql
from contextlib import contextmanager
from config import config
import os

class Database:
    """Database connection manager for VitaPink BloodBank."""
    
    def __init__(self):
        config_name = os.environ.get('FLASK_ENV', 'development')
        self.config = config[config_name]
        
    def get_connection(self):
        """Get a database connection."""
        try:
            connection = pymysql.connect(
                host=self.config.DB_HOST,
                port=self.config.DB_PORT,
                user=self.config.DB_USER,
                password=self.config.DB_PASSWORD,
                database=self.config.DB_NAME,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False
            )
            return connection
        except Exception as e:
            print(f"Database connection error: {e}")
            raise
    
    @contextmanager
    def get_cursor(self):
        """Context manager for database operations."""
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
            yield cursor
            connection.commit()
        except Exception as e:
            connection.rollback()
            print(f"Database operation error: {e}")
            raise
        finally:
            cursor.close()
            connection.close()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results."""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()
    
    def execute_single(self, query, params=None):
        """Execute a query and return single result."""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()
    
    def execute_insert(self, query, params=None):
        """Execute an insert query and return the inserted ID."""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.lastrowid
    
    def execute_update(self, query, params=None):
        """Execute an update/delete query and return affected rows."""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.rowcount

# Global database instance
db = Database() 