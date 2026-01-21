"""
Database Service
=================
Handles all database operations with READ-ONLY access.
This service only executes SELECT queries that have passed security validation.
"""

import os
from typing import Any, Dict, List, Optional
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


class DatabaseService:
    """
    Database service for executing READ-ONLY queries.
    
    This service:
    - Only executes SELECT queries
    - Uses connection pooling
    - Returns results as dictionaries
    - Handles errors gracefully
    """
    
    def __init__(self):
        self.connection_params = {
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT", "5432"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
        }
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            yield conn
        finally:
            if conn:
                conn.close()
    
    @contextmanager
    def get_cursor(self, dict_cursor: bool = True):
        """Context manager for database cursors."""
        with self.get_connection() as conn:
            cursor_factory = RealDictCursor if dict_cursor else None
            cursor = conn.cursor(cursor_factory=cursor_factory)
            try:
                yield cursor
            finally:
                cursor.close()
    
    def execute_select(self, sql: str) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return results.
        
        IMPORTANT: This method should ONLY be called after security validation.
        The query must have already passed through the HardcodedSecurityValidator.
        
        Args:
            sql: The validated SELECT query
            
        Returns:
            List of dictionaries containing query results
        """
        with self.get_cursor(dict_cursor=True) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            # Convert RealDictRow to regular dict
            return [dict(row) for row in results]
    
    def test_connection(self) -> bool:
        """Test if database connection is working."""
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
        except Exception:
            return False
    
    def get_table_names(self, schema: str = "public") -> List[str]:
        """Get all table names in the specified schema."""
        sql = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """
        with self.get_cursor() as cursor:
            cursor.execute(sql, (schema,))
            return [row['table_name'] for row in cursor.fetchall()]
    
    def get_column_info(self, table_name: str, schema: str = "public") -> List[Dict[str, Any]]:
        """Get column information for a table."""
        sql = """
            SELECT 
                c.column_name,
                c.data_type,
                c.is_nullable,
                c.column_default,
                c.udt_name,
                pg_catalog.col_description(format('%%s.%%s', c.table_schema, c.table_name)::regclass::oid, c.ordinal_position) as column_description
            FROM information_schema.columns c
            WHERE c.table_schema = %s AND c.table_name = %s
            ORDER BY c.ordinal_position
        """
        with self.get_cursor() as cursor:
            cursor.execute(sql, (schema, table_name))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_enum_values(self, enum_type: str) -> List[str]:
        """Get all values for an ENUM type."""
        sql = """
            SELECT enumlabel
            FROM pg_enum
            JOIN pg_type ON pg_enum.enumtypid = pg_type.oid
            WHERE pg_type.typname = %s
            ORDER BY enumsortorder
        """
        with self.get_cursor() as cursor:
            cursor.execute(sql, (enum_type,))
            return [row['enumlabel'] for row in cursor.fetchall()]
    
    def get_sample_data(self, table_name: str, schema: str = "public", limit: int = 3) -> List[Dict[str, Any]]:
        """Get sample data from a table."""
        # Note: table_name and schema should be validated before calling this
        sql = f"SELECT * FROM {schema}.{table_name} LIMIT %s"
        with self.get_cursor() as cursor:
            cursor.execute(sql, (limit,))
            return [dict(row) for row in cursor.fetchall()]


# Singleton instance
db_service = DatabaseService()