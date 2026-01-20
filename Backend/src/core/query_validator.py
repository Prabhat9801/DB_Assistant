from typing import List
import re

BLOCKED_KEYWORDS = ["delete", "update", "truncate", "drop", "insert", "alter", "create", "grant", "revoke"]

def clean_sql(sql: str) -> str:
    """Remove unnecessary whitespace and comments from SQL."""
    sql = sql.strip()
    sql = re.sub(r"(--.*?$)|(/\*.*?\*/)", "", sql, flags=re.MULTILINE).strip()
    return sql

def is_select_only(sql: str) -> bool:
    """Check if the SQL query is a SELECT statement and does not contain blocked keywords."""
    sql_lower = sql.strip().lower()
    
    if not sql_lower.startswith("select"):
        return False
    
    for keyword in BLOCKED_KEYWORDS:
        if re.search(rf'\b{keyword}\b', sql_lower):
            return False
    
    return True

def validate_query(sql: str) -> bool:
    """Validate the SQL query to ensure it is safe to execute."""
    cleaned_sql = clean_sql(sql)
    return is_select_only(cleaned_sql)