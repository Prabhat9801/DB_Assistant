from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import NoSuchTableError
from typing import Dict, Any, List

class DynamicSchema:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.metadata = MetaData(bind=self.engine)
        self.metadata.reflect()

    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """Retrieve the schema of a specific table."""
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            return {
                "table_name": table.name,
                "columns": [
                    {
                        "name": column.name,
                        "type": str(column.type),
                        "nullable": column.nullable,
                        "default": column.default
                    }
                    for column in table.columns
                ]
            }
        except NoSuchTableError:
            return {"error": f"Table '{table_name}' does not exist."}

    def list_tables(self) -> List[str]:
        """List all tables in the database."""
        return self.metadata.tables.keys()

    def add_table(self, table_name: str, columns: List[Dict[str, Any]]) -> str:
        """Add a new table to the database."""
        # Implementation for adding a table dynamically
        pass

    def update_table(self, table_name: str, columns: List[Dict[str, Any]]) -> str:
        """Update an existing table's schema."""
        # Implementation for updating a table dynamically
        pass

    def remove_table(self, table_name: str) -> str:
        """Remove a table from the database."""
        # Implementation for removing a table dynamically
        pass

    def validate_query(self, query: str) -> bool:
        """Validate the SQL query against blocked keywords."""
        blocked_keywords = ["delete", "update", "truncate", "drop", "insert", "alter", "create", "grant", "revoke"]
        query_lower = query.lower()
        return not any(keyword in query_lower for keyword in blocked_keywords)