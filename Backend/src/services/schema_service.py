"""
Schema Service
===============
Dynamic schema discovery and management.
This service adapts to database changes and allows flexible table management.
"""

import os
from typing import Dict, Any, List, Set, Optional
from threading import Lock
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


class SchemaService:
    """
    Dynamic Schema Service for database introspection.
    
    Features:
    - Auto-discovery of tables and columns
    - ENUM value detection
    - Schema caching with TTL
    - Flexible table management (add/remove)
    - Thread-safe operations
    """
    
    def __init__(self):
        # Default allowed tables - can be modified at runtime
        self.allowed_tables: Set[str] = {
            "public.users",
            "public.checklist", 
            "public.delegation"
        }
        
        # Schema cache
        self._schema_cache: Dict[str, Any] = {}
        self._cache_timestamp: Optional[datetime] = None
        self._cache_ttl = timedelta(minutes=int(os.getenv("SCHEMA_CACHE_TTL_MINUTES", "5")))
        
        # Thread safety
        self._lock = Lock()
        
        # Database service (lazy initialization)
        self._db_service = None
    
    @property
    def db_service(self):
        """Lazy initialization of database service."""
        if self._db_service is None:
            from .db_service import DatabaseService
            self._db_service = DatabaseService()
        return self._db_service
    
    def _is_cache_valid(self) -> bool:
        """Check if the schema cache is still valid."""
        if not self._cache_timestamp:
            return False
        return datetime.now() - self._cache_timestamp < self._cache_ttl
    
    def refresh_schema(self) -> None:
        """Force refresh of the schema cache."""
        with self._lock:
            self._schema_cache = self._discover_schema()
            self._cache_timestamp = datetime.now()
    
    def _discover_schema(self) -> Dict[str, Any]:
        """Discover schema for all allowed tables."""
        schema = {}
        
        for table_full_name in self.allowed_tables:
            try:
                # Parse schema and table name
                if '.' in table_full_name:
                    schema_name, table_name = table_full_name.split('.', 1)
                else:
                    schema_name = "public"
                    table_name = table_full_name
                
                # Get column information
                columns = self.db_service.get_column_info(table_name, schema_name)
                
                # Process columns and detect ENUMs
                column_info = {}
                for col in columns:
                    col_data = {
                        "type": col['data_type'],
                        "nullable": col['is_nullable'] == 'YES',
                        "default": col['column_default'],
                        "description": col.get('column_description')
                    }
                    
                    # Check for ENUM types (PostgreSQL USER-DEFINED types)
                    if col['data_type'] == 'USER-DEFINED':
                        enum_values = self.db_service.get_enum_values(col['udt_name'])
                        col_data['type'] = 'ENUM'
                        col_data['enum_values'] = enum_values
                    
                    column_info[col['column_name']] = col_data
                
                # Get sample data
                try:
                    sample_data = self.db_service.get_sample_data(table_name, schema_name, limit=3)
                except Exception:
                    sample_data = []
                
                schema[table_full_name] = {
                    "columns": column_info,
                    "sample_data": sample_data
                }
                
            except Exception as e:
                schema[table_full_name] = {
                    "error": str(e),
                    "columns": {},
                    "sample_data": []
                }
        
        return schema
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the current schema (from cache or fresh)."""
        with self._lock:
            if not self._is_cache_valid():
                self._schema_cache = self._discover_schema()
                self._cache_timestamp = datetime.now()
            return self._schema_cache
    
    def get_schema_dict(self) -> Dict[str, Any]:
        """Get schema as a dictionary for API responses."""
        return self.get_schema()
    
    def get_formatted_schema_context(self) -> str:
        """
        Generate schema string in the format:
        Table:
        Column (Type) -- Description
        """
        schema = self.get_schema()
        lines = []
        
        for table_name, table_data in schema.items():
            if "error" in table_data:
                continue
                
            lines.append(f"{table_name}:")
            for col_name, col_info in table_data["columns"].items():
                desc = f" -- {col_info['description']}" if col_info.get('description') else ""
                lines.append(f"{col_name} ({col_info['type']}){desc}")
            lines.append("") # Empty line between tables
            
        return "\n".join(lines)

    def get_schema_context(self) -> str:
        """
        Generate schema context string for LLM prompts.
        This is used by the chat service to provide database context to the LLM.
        """
        schema = self.get_schema()
        context_parts = []
        
        context_parts.append("=== DATABASE SCHEMA ===\n")
        
        for table_name, table_info in schema.items():
            if "error" in table_info:
                continue
                
            context_parts.append(f"\nTable: {table_name}")
            context_parts.append("Columns:")
            
            for col_name, col_info in table_info.get("columns", {}).items():
                col_type = col_info.get("type", "UNKNOWN")
                
                if col_type == "ENUM":
                    enum_vals = col_info.get("enum_values", [])
                    context_parts.append(f"  - {col_name}: {col_type} (values: {enum_vals})")
                else:
                    context_parts.append(f"  - {col_name}: {col_type}")
            
            # Add sample data hint
            sample_data = table_info.get("sample_data", [])
            if sample_data:
                context_parts.append(f"Sample data: {sample_data[:2]}")
            
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def add_allowed_table(self, table_name: str) -> bool:
        """
        Add a table to the allowed list.
        
        Args:
            table_name: Full table name (e.g., 'public.new_table')
            
        Returns:
            True if table was added, False if it doesn't exist
        """
        # Parse table name
        if '.' in table_name:
            schema_name, tbl_name = table_name.split('.', 1)
        else:
            schema_name = "public"
            tbl_name = table_name
            table_name = f"public.{table_name}"
        
        # Verify table exists in database
        try:
            existing_tables = self.db_service.get_table_names(schema_name)
            if tbl_name not in existing_tables:
                return False
        except Exception:
            return False
        
        with self._lock:
            self.allowed_tables.add(table_name)
            # Invalidate cache
            self._cache_timestamp = None
        
        return True
    
    def remove_allowed_table(self, table_name: str) -> bool:
        """
        Remove a table from the allowed list.
        
        Args:
            table_name: Full table name (e.g., 'public.old_table')
            
        Returns:
            True if table was removed, False if it wasn't in the list
        """
        # Normalize table name
        if '.' not in table_name:
            table_name = f"public.{table_name}"
        
        with self._lock:
            if table_name in self.allowed_tables:
                self.allowed_tables.discard(table_name)
                # Invalidate cache
                self._cache_timestamp = None
                return True
        
        return False
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database."""
        if '.' in table_name:
            schema_name, tbl_name = table_name.split('.', 1)
        else:
            schema_name = "public"
            tbl_name = table_name
        
        try:
            existing_tables = self.db_service.get_table_names(schema_name)
            return tbl_name in existing_tables
        except Exception:
            return False


# Singleton instance
schema_service = SchemaService()