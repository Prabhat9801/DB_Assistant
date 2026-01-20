def clean_sql(sql: str) -> str:
    """Remove unwanted characters and sanitize SQL queries."""
    sql = sql.strip()
    # Remove comments
    sql = re.sub(r"--.*?$|/\*.*?\*/", "", sql, flags=re.DOTALL)
    # Remove any SQL injection patterns
    sql = re.sub(r"(['\";])", "", sql)
    return sql.strip()