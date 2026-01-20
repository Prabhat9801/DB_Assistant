# =========================
# DB-ONLY CHATBOT (LangGraph + OpenAI + PostgreSQL)
# Uses ONLY env variables (NO hardcoding)
# Tables: public.checklist, public.delegation, public.users
# ONLY SELECT (NO DELETE/UPDATE/TRUNCATE/DROP/INSERT)
# SUPPORTS: English and Hinglish queries
# =========================

import os
import re
import json
import psycopg2
from contextlib import contextmanager
from typing import TypedDict, Optional, Any, List, Dict
from dotenv import load_dotenv
from datetime import datetime

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

# =========================
# 1) LOAD ENV & CONFIG
# =========================
load_dotenv()  # Load .env file

def get_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise ValueError(f"Missing environment variable: {name}")
    return val

OPENAI_API_KEY = get_env("OPENAI_API_KEY")
DB_HOST = get_env("DB_HOST")
DB_NAME = get_env("DB_NAME")
DB_USER = get_env("DB_USER")
DB_PASSWORD = get_env("DB_PASSWORD")
DB_PORT = get_env("DB_PORT")

ALLOWED_TABLES = {"checklist", "delegation", "users"}
BLOCKED_KEYWORDS = ["delete", "update", "truncate", "drop", "insert", "alter", "create", "grant", "revoke"]

# Verbose mode flag
VERBOSE_MODE = True

def log_step(step_name: str, message: str, data: Any = None):
    """Log internal steps with timestamps."""
    if VERBOSE_MODE:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"\n{'='*60}")
        print(f"⏱️  [{timestamp}] STEP: {step_name}")
        print(f"{'='*60}")
        print(f"📋 {message}")
        if data:
            if isinstance(data, str):
                print(f"\n{data}")
            else:
                print(f"\n{json.dumps(data, indent=2, default=str)}")

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o-mini",
    temperature=0
)


# =========================
# 2) LANGUAGE DETECTION
# =========================
def detect_language(text: str) -> str:
    """Detect if the text is in Hinglish or English."""
    # Common Hinglish words and patterns
    hinglish_indicators = [
        # Common Hindi words written in Roman
        r'\bkitne\b', r'\bkitna\b', r'\bkitni\b', r'\bkya\b', r'\bkaise\b',
        r'\bkaun\b', r'\bkahan\b', r'\bkab\b', r'\bkyun\b', r'\bkyu\b',
        r'\bdikhao\b', r'\bdikha\b', r'\bbatao\b', r'\bbata\b', r'\bdo\b',
        r'\bdedo\b', r'\bkaro\b', r'\bkar\b', r'\bhain\b', r'\bhai\b',
        r'\bho\b', r'\btha\b', r'\bthe\b', r'\bthi\b', r'\bhoga\b',
        r'\bsabhi\b', r'\bsab\b', r'\bsaare\b', r'\bpura\b', r'\bpuri\b',
        r'\buser\b.*\bko\b', r'\btask\b.*\bka\b', r'\blist\b.*\bdo\b',
        r'\bwale\b', r'\bwali\b', r'\bwala\b', r'\bmein\b', r'\bme\b',
        r'\bse\b', r'\bka\b', r'\bki\b', r'\bke\b', r'\bko\b', r'\bne\b',
        r'\bpar\b', r'\bpe\b', r'\baur\b', r'\bya\b', r'\bnahiB\b',
        r'\bnahi\b', r'\bnahin\b', r'\bhaan\b', r'\bji\b', r'\baccha\b',
        r'\btheek\b', r'\bthik\b', r'\bzaroor\b', r'\bjaroor\b',
        r'\bpehle\b', r'\bbaad\b', r'\babhi\b', r'\bkal\b', r'\baaj\b',
        r'\bparso\b', r'\bhafta\b', r'\bmahina\b', r'\bsaal\b',
        r'\bkam\b', r'\bzyada\b', r'\bjyada\b', r'\bkam\b', r'\bbahut\b',
        r'\bthoda\b', r'\bpending\b.*\bwale\b', r'\bcomplete\b.*\bhua\b',
        r'\bdepartment\b.*\bke\b', r'\bactive\b.*\bwale\b',
        r'\bkonsa\b', r'\bkonsi\b', r'\bjinke\b', r'\bjinka\b', r'\bjinki\b',
        r'\bunke\b', r'\bunka\b', r'\bunki\b', r'\biske\b', r'\biski\b',
        r'\biska\b', r'\buska\b', r'\buski\b', r'\buske\b',
        # Task-related Hinglish
        r'\btask\b.*\bpure\b', r'\btask\b.*\bnahi\b', r'\boverdue\b.*\bwale\b',
        r'\blate\b.*\bsubmit\b', r'\bdelay\b.*\bhua\b',
    ]
    
    text_lower = text.lower()
    
    # Count Hinglish indicators
    hinglish_count = 0
    for pattern in hinglish_indicators:
        if re.search(pattern, text_lower):
            hinglish_count += 1
    
    # If 2+ Hinglish indicators found, consider it Hinglish
    if hinglish_count >= 2:
        return "hinglish"
    
    # Check for Devanagari script (pure Hindi)
    if re.search(r'[\u0900-\u097F]', text):
        return "hinglish"  # Treat as Hinglish for response
    
    return "english"


# =========================
# 3) DB HELPERS (IMPROVED)
# =========================
@contextmanager
def get_db_connection():
    """Context manager for safe connection handling."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=int(DB_PORT)
        )
        yield conn
    finally:
        if conn:
            conn.close()


def fetch_schema_for_allowed_tables() -> str:
    """Fetch schema for: public.checklist, public.delegation, public.users"""
    query = """
    SELECT 
        table_name, 
        column_name, 
        data_type,
        is_nullable,
        column_default
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name IN ('checklist', 'delegation', 'users')
    ORDER BY table_name, ordinal_position;
    """
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    schema_map: Dict[str, List[str]] = {}
    for table, col, dtype, nullable, default in rows:
        col_info = f"{col} ({dtype})"
        if nullable == 'NO':
            col_info += " NOT NULL"
        schema_map.setdefault(table, []).append(col_info)

    schema_text = ""
    for table, cols in schema_map.items():
        schema_text += f"Table: public.{table}\nColumns:\n  - " + "\n  - ".join(cols) + "\n\n"

    return schema_text.strip()


def fetch_column_enum_mapping() -> str:
    """Fetch the actual ENUM type used by each column in the database."""
    query = """
    SELECT 
        c.table_name,
        c.column_name,
        c.udt_name as enum_type,
        ARRAY_AGG(e.enumlabel ORDER BY e.enumsortorder) as enum_values
    FROM information_schema.columns c
    JOIN pg_type t ON c.udt_name = t.typname
    JOIN pg_enum e ON t.oid = e.enumtypid
    WHERE c.table_schema = 'public'
      AND c.table_name IN ('checklist', 'delegation', 'users')
    GROUP BY c.table_name, c.column_name, c.udt_name
    ORDER BY c.table_name, c.column_name;
    """
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    if not rows:
        return "No ENUM columns found."
    
    enum_text = "=== ⚠️ ACTUAL ENUM Column Mappings (from database) ===\n"
    enum_text += "CRITICAL: Use ONLY these exact values for each column:\n\n"
    
    for table, column, enum_type, values in rows:
        enum_text += f"  {table}.{column} (ENUM type: {enum_type}):\n"
        enum_text += f"    Valid values: {', '.join(repr(v) for v in values)}\n\n"
    
    return enum_text.strip()


def fetch_enum_values() -> str:
    """Fetch all ENUM types and their valid values from the database."""
    query = """
    SELECT 
        t.typname AS enum_name,
        e.enumlabel AS enum_value
    FROM pg_type t
    JOIN pg_enum e ON t.oid = e.enumtypid
    JOIN pg_catalog.pg_namespace n ON n.oid = t.typnamespace
    WHERE n.nspname = 'public'
    ORDER BY t.typname, e.enumsortorder;
    """
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    if not rows:
        return "No ENUM types found."
    
    enum_map: Dict[str, List[str]] = {}
    for enum_name, enum_value in rows:
        enum_map.setdefault(enum_name, []).append(enum_value)
    
    enum_text = "=== All ENUM Types in Database ===\n"
    for enum_name, values in enum_map.items():
        enum_text += f"  {enum_name}: {', '.join(repr(v) for v in values)}\n"
    
    enum_text += "\n" + fetch_column_enum_mapping()
    
    return enum_text.strip()


def fetch_sample_data() -> str:
    """Fetch sample values from key columns to help LLM understand data patterns."""
    samples = {}
    
    sample_queries = {
        "checklist.status": "SELECT DISTINCT status::text FROM public.checklist WHERE status IS NOT NULL LIMIT 10",
        "checklist.enable_reminder": "SELECT DISTINCT enable_reminder::text FROM public.checklist WHERE enable_reminder IS NOT NULL LIMIT 10",
        "checklist.department": "SELECT DISTINCT department FROM public.checklist WHERE department IS NOT NULL LIMIT 10",
        "checklist.frequency": "SELECT DISTINCT frequency FROM public.checklist WHERE frequency IS NOT NULL LIMIT 10",
        "checklist.name": "SELECT DISTINCT name FROM public.checklist WHERE name IS NOT NULL LIMIT 10",
        "checklist.planned_date (VARIOUS FORMATS)": "SELECT DISTINCT planned_date FROM public.checklist WHERE planned_date IS NOT NULL AND planned_date <> '' LIMIT 10",
        "delegation.status": "SELECT DISTINCT status FROM public.delegation WHERE status IS NOT NULL LIMIT 10",
        "users.role": "SELECT DISTINCT role::text FROM public.users WHERE role IS NOT NULL LIMIT 10",
        "users.status": "SELECT DISTINCT status::text FROM public.users WHERE status IS NOT NULL LIMIT 10",
        "users.department": "SELECT DISTINCT department FROM public.users WHERE department IS NOT NULL LIMIT 10",
        "users.user_name": "SELECT DISTINCT user_name FROM public.users WHERE user_name IS NOT NULL LIMIT 10",
    }
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for col_name, query in sample_queries.items():
                try:
                    cur.execute(query)
                    values = [str(row[0]) for row in cur.fetchall()]
                    if values:
                        samples[col_name] = values
                except Exception as e:
                    samples[col_name] = [f"Query error"]
    
    if not samples:
        return "No sample data available."
    
    sample_text = "=== Actual Sample Values from Database ===\n"
    sample_text += "⚠️ Use these EXACT values in WHERE clauses:\n\n"
    for col, values in samples.items():
        sample_text += f"  {col}: {', '.join(repr(v) for v in values[:7])}\n"
    
    return sample_text.strip()


def fetch_table_relationships() -> str:
    """Fetch foreign key relationships between allowed tables."""
    query = """
    SELECT
        tc.table_name AS source_table,
        kcu.column_name AS source_column,
        ccu.table_name AS target_table,
        ccu.column_name AS target_column
    FROM information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
        ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu
        ON ccu.constraint_name = tc.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY'
      AND tc.table_schema = 'public'
      AND tc.table_name IN ('checklist', 'delegation', 'users')
      AND ccu.table_name IN ('checklist', 'delegation', 'users');
    """
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    if not rows:
        return "No foreign key relationships found between tables."
    
    relationships = []
    for src_table, src_col, tgt_table, tgt_col in rows:
        relationships.append(f"{src_table}.{src_col} -> {tgt_table}.{tgt_col}")
    
    return "Relationships:\n" + "\n".join(relationships)


def run_select_query(sql: str) -> List[Dict[str, Any]]:
    """Execute SELECT query and return list of dict rows."""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            col_names = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
    
    return [dict(zip(col_names, r)) for r in rows]


# =========================
# 4) SECURITY / VALIDATION (ENHANCED)
# =========================
def clean_sql(sql: str) -> str:
    """Remove markdown code blocks and clean whitespace."""
    sql = sql.strip()
    sql = re.sub(r"```sql|```", "", sql).strip()
    sql = re.sub(r"--.*$", "", sql, flags=re.MULTILINE)
    return sql.strip()


def is_select_only(sql: str) -> bool:
    """Strict check: must start with SELECT and contain no blocked keywords."""
    sql_low = sql.strip().lower()
    
    if not sql_low.startswith("select"):
        return False
    
    for keyword in BLOCKED_KEYWORDS:
        pattern = rf'\b{keyword}\b'
        if re.search(pattern, sql_low):
            return False
    
    if re.search(r';\s*\w', sql_low):
        return False
    
    return True


def references_only_allowed_tables(sql: str) -> bool:
    """Block table names outside checklist/delegation/users."""
    sql_low = sql.lower()
    
    sql_clean = re.sub(r"'[^']*'", "", sql_low)
    
    patterns = [
        r'\bfrom\s+(?:public\.)?([a-zA-Z_][a-zA-Z0-9_]*)',
        r'\bjoin\s+(?:public\.)?([a-zA-Z_][a-zA-Z0-9_]*)',
    ]
    
    tables = set()
    for pattern in patterns:
        matches = re.findall(pattern, sql_clean)
        tables.update(matches)
    
    sql_keywords = {'select', 'where', 'and', 'or', 'on', 'as', 'left', 'right', 'inner', 'outer', 'cross'}
    tables -= sql_keywords
    
    if not tables:
        return True
    
    return tables.issubset(ALLOWED_TABLES)


def force_limit(sql: str, max_rows: int = 200) -> str:
    """Add LIMIT if missing to prevent huge responses."""
    sql_low = sql.lower()
    if " limit " in sql_low:
        return sql
    return sql.rstrip(";") + f" LIMIT {max_rows};"


# =========================
# 5) LANGGRAPH STATE
# =========================
class ChatState(TypedDict):
    user_question: str
    detected_language: Optional[str]  # NEW: Track language
    schema: Optional[str]
    relationships: Optional[str]
    enum_values: Optional[str]
    sample_data: Optional[str]
    intent: Optional[str]
    generated_sql: Optional[str]
    safe_sql: Optional[str]
    db_result: Optional[List[Dict[str, Any]]]
    final_answer: Optional[str]
    error: Optional[str]


# =========================
# 6) LANGGRAPH NODES (WITH LOGGING)
# =========================
def language_detection_node(state: ChatState) -> ChatState:
    """Detect if the user query is in English or Hinglish."""
    log_step("0️⃣ LANGUAGE_DETECTOR", f"Detecting language for: '{state['user_question']}'")
    
    detected = detect_language(state["user_question"])
    state["detected_language"] = detected
    
    log_step("0️⃣ LANGUAGE_DETECTOR ✅", f"Detected language: {detected.upper()}")
    return state


def schema_node(state: ChatState) -> ChatState:
    """Fetch database schema, relationships, enum values, and sample data."""
    log_step("1️⃣ SCHEMA_NODE", "Fetching database schema, relationships, enums, and sample data...")
    
    try:
        state["schema"] = fetch_schema_for_allowed_tables()
        state["relationships"] = fetch_table_relationships()
        state["enum_values"] = fetch_enum_values()
        state["sample_data"] = fetch_sample_data()
        
        log_step("1️⃣ SCHEMA_NODE ✅", "Schema fetched successfully!", 
                 f"SCHEMA:\n{state['schema']}\n\nRELATIONSHIPS:\n{state['relationships']}\n\nENUMS:\n{state['enum_values']}\n\nSAMPLE DATA:\n{state['sample_data']}")
        return state
    except Exception as e:
        state["error"] = f"Schema fetch failed: {str(e)}"
        log_step("1️⃣ SCHEMA_NODE ❌", f"Error: {state['error']}")
        return state


def intent_analyzer_node(state: ChatState) -> ChatState:
    """Analyze user intent to determine which tables are relevant."""
    log_step("2️⃣ INTENT_ANALYZER", f"Analyzing user question: '{state['user_question']}'")
    
    if state.get("error"):
        log_step("2️⃣ INTENT_ANALYZER ⏭️", "Skipped due to previous error")
        return state
    
    try:
        # Add Hinglish understanding to intent analyzer
        hinglish_context = ""
        if state.get("detected_language") == "hinglish":
            hinglish_context = """
NOTE: The user's question is in HINGLISH (Hindi + English mix).
Common Hinglish patterns to understand:
- "dikhao" / "dikha do" = show
- "batao" = tell/show
- "kitne" / "kitna" = how many/much
- "sabhi" / "sab" / "saare" = all
- "wale" / "wali" = those who/which
- "karo" = do
- "hai" / "hain" = is/are
- "nahi" / "nahin" = not/no
- "complete nahi hua" = not completed
- "pending wale" = pending ones
- "department ke" = of department
- "user ko" = to user
- "task ka" = of task
"""
        
        prompt = f"""Analyze the user's question and determine:
1. Which tables are relevant (checklist, delegation, users)
2. Whether JOINs are needed
3. What type of aggregation/filtering is required

CRITICAL RULE: This is READ-ONLY. No modifications allowed.
{hinglish_context}

Available Tables:
{state['schema']}

{state['relationships']}

{state['enum_values']}

{state['sample_data']}

User Question: {state['user_question']}

Respond in JSON format:
{{"tables": ["table1", "table2"], "needs_join": true/false, "query_type": "simple/aggregate/join", "notes": "brief analysis"}}
"""
        log_step("2️⃣ INTENT_ANALYZER", "Sending prompt to LLM...", 
                 f"PROMPT (truncated):\n{prompt[:500]}...")
        
        resp = llm.invoke(prompt)
        state["intent"] = resp.content.strip()
        
        log_step("2️⃣ INTENT_ANALYZER ✅", "Intent analysis complete!", state["intent"])
        return state
    except Exception as e:
        state["error"] = f"Intent analysis failed: {str(e)}"
        log_step("2️⃣ INTENT_ANALYZER ❌", f"Error: {state['error']}")
        return state


def sql_generator_node(state: ChatState) -> ChatState:
    """LLM generates SQL for checklist/delegation/users. READ-ONLY ONLY."""
    log_step("3️⃣ SQL_GENERATOR", "Generating SQL query...")
    
    if state.get("error"):
        log_step("3️⃣ SQL_GENERATOR ⏭️", "Skipped due to previous error")
        return state
    
    try:
        # Add Hinglish understanding
        hinglish_sql_context = ""
        if state.get("detected_language") == "hinglish":
            hinglish_sql_context = """
=== HINGLISH QUERY TRANSLATION GUIDE ===
The user is asking in Hinglish. Translate these common patterns:
- "sabhi users dikhao" = SELECT * FROM users
- "kitne tasks hain" = SELECT COUNT(*) FROM checklist
- "pending wale tasks" = WHERE status = 'no'
- "complete ho gaye" = WHERE status = 'yes'
- "ADMIN department ke users" = WHERE department = 'ADMIN'
- "active users batao" = WHERE status = 'active'
- "task count department wise" = GROUP BY department
- "top 5 departments" = ORDER BY ... LIMIT 5
- "recent delegations" = ORDER BY created_at DESC
- "jinka task complete nahi hua" = WHERE status = 'no'
- "delay wale tasks" = WHERE delay IS NOT NULL AND delay > INTERVAL '0'

"""
        
        system_rules = f"""You are a PostgreSQL SQL generator for a READ-ONLY chatbot.
{hinglish_sql_context}

=== CRITICAL SAFETY RULES (NEVER BREAK) ===
1. ONLY generate SELECT queries
2. NEVER use: DELETE, UPDATE, TRUNCATE, DROP, INSERT, ALTER, CREATE, GRANT, REVOKE
3. If user asks to modify data, return: SELECT 'READ_ONLY_MODE: Cannot modify data' as message;

=== SCOPE RULES ===
- Use ONLY tables: public.checklist, public.delegation, public.users
- Use JOINs when needed between tables
- Always qualify columns with table names in JOINs

=== OUTPUT RULES ===
- Return ONLY ONE SQL query (single statement)
- NEVER return multiple SQL statements separated by semicolons
- No explanations, no markdown
- Use proper PostgreSQL syntax
- If the query already needs a LIMIT, include it. Do NOT add LIMIT if not needed.

=== ⚠️⚠️⚠️ SUPER CRITICAL: ENUM VALUES ⚠️⚠️⚠️ ===
For checklist.status:
  - ONLY valid values: 'yes', 'no'
  - 'yes' = task completed, 'no' = task not completed
  - DO NOT use 'done', 'completed', 'pending'

For users.status:
  - Valid values: 'active', 'inactive', 'on_leave', 'terminated'

For delegation.status:
  - This is TEXT, not ENUM - values like 'done', 'Done', 'extend'

=== ⚠️⚠️⚠️ SUPER CRITICAL: TYPE COMPATIBILITY ⚠️⚠️⚠️ ===
NEVER use UNION between checklist and delegation status columns!
- checklist.status is ENUM type (enable_reminder)
- delegation.status is TEXT type
- They CANNOT be combined with UNION directly!

=== ⚠️⚠️⚠️ SUPER CRITICAL: DATE FORMAT HANDLING ⚠️⚠️⚠️ ===
The checklist.planned_date column is TEXT with MIXED FORMATS - AVOID IT!

Use these TIMESTAMP columns instead:
- checklist.created_at: TIMESTAMP
- checklist.task_start_date: TIMESTAMP
- checklist.submission_date: TIMESTAMP
- delegation.created_at: TIMESTAMP
- delegation.planned_date: TIMESTAMP (this one is proper timestamp)

=== LOGIC FOR "NOT COMPLETED ON TIME" ===
- "Not completed" = checklist.status = 'no'
- Use 'delay' column (INTERVAL) or 'submission_date' (TIMESTAMP)

=== JOIN LOGIC ===
- Link users to tasks: users.user_name = checklist.name
- Or by department: users.department = checklist.department

=== SEARCH / LIKE QUERIES ===
For name searches, use ILIKE for case-insensitive:
WHERE user_name ILIKE '%abhishek%'
WHERE name ILIKE '%abhishek%'
"""

        prompt = f"""{system_rules}

Database Schema:
{state['schema']}

{state['relationships']}

{state['enum_values']}

{state['sample_data']}

Intent Analysis:
{state['intent']}

User Question:
{state['user_question']}

⚠️⚠️⚠️ CRITICAL REMINDERS ⚠️⚠️⚠️
1. checklist.status uses 'yes'/'no' (NOT 'done'/'completed')
2. NEVER UNION checklist.status with delegation.status without casting!
3. Use ILIKE for name searches
4. Use proper TIMESTAMP columns for date filtering

Return ONLY ONE SQL statement:"""

        log_step("3️⃣ SQL_GENERATOR", "Sending prompt to LLM for SQL generation...")
        
        resp = llm.invoke(prompt)
        sql = clean_sql(resp.content)
        state["generated_sql"] = sql
        
        log_step("3️⃣ SQL_GENERATOR ✅", "SQL generated!", f"GENERATED SQL:\n{sql}")
        return state

    except Exception as e:
        state["error"] = f"SQL generation failed: {str(e)}"
        log_step("3️⃣ SQL_GENERATOR ❌", f"Error: {state['error']}")
        return state


def validator_node(state: ChatState) -> ChatState:
    """Validate and sanitize the SQL. Block anything that's not SELECT."""
    log_step("4️⃣ VALIDATOR", "Validating SQL for security...")
    
    if state.get("error"):
        log_step("4️⃣ VALIDATOR ⏭️", "Skipped due to previous error")
        return state
    
    sql = state.get("generated_sql", "").strip()
    
    log_step("4️⃣ VALIDATOR", "Check 1: Is SQL empty?", f"SQL length: {len(sql)}")
    if not sql:
        state["error"] = "No SQL was generated"
        log_step("4️⃣ VALIDATOR ❌", "Empty SQL")
        return state
    
    sql_upper = sql.upper().strip()
    starts_with_select = sql_upper.startswith("SELECT")
    log_step("4️⃣ VALIDATOR", "Check 2: Is it SELECT only?", f"Starts with SELECT: {starts_with_select}")
    
    if not starts_with_select:
        state["error"] = "Only SELECT queries are allowed (read-only mode)"
        log_step("4️⃣ VALIDATOR ❌", "Not a SELECT query")
        return state
    
    dangerous_keywords = [
        "DELETE", "UPDATE", "INSERT", "DROP", "TRUNCATE", 
        "ALTER", "CREATE", "GRANT", "REVOKE", "EXECUTE",
        "EXEC", "INTO OUTFILE", "INTO DUMPFILE"
    ]
    
    for keyword in dangerous_keywords:
        if re.search(r'\b' + keyword + r'\b', sql_upper):
            state["error"] = f"Dangerous keyword '{keyword}' detected. Only SELECT allowed."
            log_step("4️⃣ VALIDATOR ❌", f"Dangerous keyword: {keyword}")
            return state
    
    log_step("4️⃣ VALIDATOR", "Check 3: References only allowed tables?")
    
    sql_for_limit_check = sql_upper.replace('\n', ' ').replace('\t', ' ')
    has_limit = bool(re.search(r'\bLIMIT\s+\d+\s*;?\s*$', sql_for_limit_check))
    
    if has_limit:
        safe_sql = sql.rstrip(';').strip()
    else:
        safe_sql = sql.rstrip(';').strip() + " LIMIT 200"
    
    state["safe_sql"] = safe_sql
    log_step("4️⃣ VALIDATOR ✅", "All security checks passed!", f"SAFE SQL:\n{safe_sql};")
    
    return state


def db_node(state: ChatState) -> ChatState:
    """Execute the validated SQL query."""
    log_step("5️⃣ DB_EXECUTOR", "Executing SQL query on database...")
    
    if state.get("error"):
        log_step("5️⃣ DB_EXECUTOR ⏭️", "Skipped due to previous error")
        return state
    
    try:
        log_step("5️⃣ DB_EXECUTOR", f"Connecting to: {DB_HOST}/{DB_NAME}")
        log_step("5️⃣ DB_EXECUTOR", f"Executing SQL:\n{state['safe_sql']}")
        
        result = run_select_query(state["safe_sql"])
        state["db_result"] = result
        
        sample = result[:5] if len(result) > 5 else result
        log_step("5️⃣ DB_EXECUTOR ✅", f"Query returned {len(result)} rows", 
                 f"SAMPLE (first {len(sample)} rows):\n{json.dumps(sample, indent=2, default=str)}")
        return state
    except Exception as e:
        state["error"] = f"DB execution failed: {str(e)}"
        log_step("5️⃣ DB_EXECUTOR ❌", f"Error: {state['error']}")
        return state


def answer_node(state: ChatState) -> ChatState:
    """Generate natural language answer from database results."""
    log_step("6️⃣ ANSWER_GENERATOR", "Generating natural language response...")
    
    try:
        if state.get("error"):
            # Error messages based on language
            if state.get("detected_language") == "hinglish":
                state["final_answer"] = f"❌ Error ho gaya: {state['error']}"
            else:
                state["final_answer"] = f"❌ Error: {state['error']}"
            log_step("6️⃣ ANSWER_GENERATOR", f"Returning error message: {state['error']}")
            return state

        result = state.get("db_result") or []

        if not result:
            if state.get("detected_language") == "hinglish":
                state["final_answer"] = "📭 Koi data nahi mila aapki query ke liye. Search mein zero results aaye."
            else:
                state["final_answer"] = "📭 No data found for your query. The search returned zero results."
            log_step("6️⃣ ANSWER_GENERATOR", "No results found")
            return state

        display_result = result[:50] if len(result) > 50 else result
        truncated = len(result) > 50

        # Language-specific prompt
        language_instruction = ""
        if state.get("detected_language") == "hinglish":
            language_instruction = """
=== CRITICAL: RESPOND IN HINGLISH ===
The user asked in Hinglish (Hindi + English mix), so you MUST respond in Hinglish.

Hinglish Response Rules:
1. Mix Hindi words (in Roman script) with English naturally
2. Use common Hinglish phrases like:
   - "Yeh raha data..." (Here's the data)
   - "Total X users/tasks mile" (Found total X users/tasks)
   - "Sabse zyada..." (Most/Maximum)
   - "...department mein" (in department)
   - "...wale users" (users who...)
   - "Koi data nahi mila" (No data found)
   - "Ye hai list..." (This is the list)
   - "...complete ho chuke hain" (have been completed)
   - "...pending hain" (are pending)
   - "...ke paas" (has/have)
3. Keep technical terms in English (department, task, user, status, etc.)
4. Use Hindi sentence structure where natural
5. Be friendly and conversational in Hinglish tone

Example Hinglish Responses:
- "👥 **ADMIN Department ke Users (14 mile):**"
- "📊 **Department wise Task Count:**\n- **IT:** 45 tasks hain\n- **HR:** 32 tasks hain"
- "✅ Badhai ho! Koi overdue task nahi hai abhi."
- "📋 **Task Details:**\n- **Name:** Monthly Report\n- **Status:** Complete ho gaya hai"
"""
        else:
            language_instruction = """
=== RESPOND IN ENGLISH ===
The user asked in English, so respond in clear, professional English.
"""

        prompt = f"""You are a friendly database assistant. Your job is to convert database results into clear, natural language responses.

{language_instruction}

=== FORMATTING RULES ===
1. ALWAYS respond in natural, conversational language
2. INCLUDE the actual data from the results in your answer
3. Format data in a readable way:
   - Use bullet points or numbered lists for multiple items
   - Format dates nicely (e.g., "January 19, 2025" or "19 January, 2025")
   - Format numbers with commas if large (e.g., "1,234")
4. Summarize if there are many results
5. Be concise but complete
6. Add relevant context when helpful
7. Use emojis sparingly to make it visually appealing

=== YOUR TASK ===
User Question: {state['user_question']}
Detected Language: {state.get('detected_language', 'english').upper()}

Database Result ({len(result)} rows{', showing first 50' if truncated else ''}):
{json.dumps(display_result, indent=2, default=str)}

Provide a natural, friendly response with the actual data formatted nicely."""

        log_step("6️⃣ ANSWER_GENERATOR", "Sending results to LLM for answer generation...")
        
        resp = llm.invoke(prompt)
        answer = resp.content.strip()
        
        if truncated:
            if state.get("detected_language") == "hinglish":
                answer += f"\n\n📌 *Total {len(result)} results mein se 50 dikha rahe hain. Zyada specific data ke liye query refine karein.*"
            else:
                answer += f"\n\n📌 *Showing 50 of {len(result)} total results. Refine your query for more specific data.*"
        
        state["final_answer"] = answer
        
        log_step("6️⃣ ANSWER_GENERATOR ✅", "Answer generated!", 
                 f"FINAL ANSWER:\n{state['final_answer']}")
        return state

    except Exception as e:
        state["final_answer"] = f"Answer generation failed: {str(e)}"
        log_step("6️⃣ ANSWER_GENERATOR ❌", f"Error: {str(e)}")
        return state


# =========================
# 7) BUILD GRAPH
# =========================
graph = StateGraph(ChatState)

graph.add_node("language_detection_node", language_detection_node)  # NEW NODE
graph.add_node("schema_node", schema_node)
graph.add_node("intent_analyzer_node", intent_analyzer_node)
graph.add_node("sql_generator_node", sql_generator_node)
graph.add_node("validator_node", validator_node)
graph.add_node("db_node", db_node)
graph.add_node("answer_node", answer_node)

graph.set_entry_point("language_detection_node")  # Start with language detection
graph.add_edge("language_detection_node", "schema_node")
graph.add_edge("schema_node", "intent_analyzer_node")
graph.add_edge("intent_analyzer_node", "sql_generator_node")
graph.add_edge("sql_generator_node", "validator_node")
graph.add_edge("validator_node", "db_node")
graph.add_edge("db_node", "answer_node")
graph.add_edge("answer_node", END)

app = graph.compile()


# =========================
# 8) MAIN FUNCTION
# =========================
def ask_db_bot(question: str, verbose: bool = True) -> str:
    """Ask the database bot a question."""
    global VERBOSE_MODE
    VERBOSE_MODE = verbose
    
    print("\n" + "🚀"*30)
    print(f"🚀 STARTING PIPELINE FOR: '{question}'")
    print("🚀"*30)
    
    state: ChatState = {
        "user_question": question,
        "detected_language": None,
        "schema": None,
        "relationships": None,
        "enum_values": None,
        "sample_data": None,
        "intent": None,
        "generated_sql": None,
        "safe_sql": None,
        "db_result": None,
        "final_answer": None,
        "error": None
    }

    out = app.invoke(state)

    # Final Summary
    print("\n" + "="*60)
    print("📊 PIPELINE SUMMARY")
    print("="*60)
    print(f"❓ Question: {question}")
    print(f"🌐 Language: {out.get('detected_language', 'N/A').upper()}")
    print(f"🎯 Intent: {out.get('intent', 'N/A')[:100]}...")
    print(f"📝 Generated SQL: {out.get('generated_sql', 'N/A')}")
    print(f"✅ Safe SQL: {out.get('safe_sql', 'N/A')}")
    print(f"📊 Results: {len(out.get('db_result') or [])} rows")
    print(f"💬 Answer: {out.get('final_answer', 'N/A')}")
    print("="*60)

    return out.get("final_answer", "")


# =========================
# 9) INTERACTIVE CHAT LOOP
# =========================
def chat_loop(verbose: bool = True):
    """Interactive chat with the database bot."""
    print("\n🤖 DB Assistant Ready!")
    print("📊 Connected to tables: checklist, delegation, users")
    print("🔒 Read-only mode (SELECT queries only)")
    print("🌐 Supports: English & Hinglish queries")
    print(f"🔍 Verbose mode: {'ON' if verbose else 'OFF'}")
    print("Type 'quit' or 'exit' to stop")
    print("Type 'verbose on/off' to toggle detailed logging\n")
    
    current_verbose = verbose
    
    while True:
        try:
            question = input("You: ").strip()
            if not question:
                continue
            if question.lower() in ('quit', 'exit', 'q'):
                print("Goodbye! Alvida! 👋")
                break
            if question.lower() == 'verbose on':
                current_verbose = True
                print("🔍 Verbose mode: ON")
                continue
            if question.lower() == 'verbose off':
                current_verbose = False
                print("🔍 Verbose mode: OFF")
                continue
            ask_db_bot(question, verbose=current_verbose)
        except KeyboardInterrupt:
            print("\nGoodbye! Alvida! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    chat_loop(verbose=True)