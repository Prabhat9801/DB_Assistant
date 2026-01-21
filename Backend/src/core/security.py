"""
🔒 LAYER 3: HARDCODED SECURITY VALIDATION
=========================================
This module contains IMMUTABLE security rules that CANNOT be bypassed.
Even if the LLM hallucinates or generates malicious SQL, these rules will block it.

Security Layers:
├── Length check (max 2000 chars)
├── Whitelist check (SELECT only)
├── Blocked keyword detection (40+ keywords)
├── Blocked pattern detection (regex)
└── Multiple statement detection
"""

import re
from typing import Tuple
from dataclasses import dataclass


# ============================================================================
# 🚫 HARDCODED BLOCKED KEYWORDS - DO NOT MODIFY
# ============================================================================
# These keywords are PERMANENTLY blocked and cannot be changed at runtime.
# Any SQL containing these keywords will be rejected BEFORE execution.

BLOCKED_KEYWORDS: frozenset = frozenset([
    # Data Modification
    "delete", "update", "insert", "merge", "upsert", "replace",
    
    # Data Definition
    "drop", "alter", "create", "truncate", "rename",
    
    # Permissions & Access
    "grant", "revoke", "deny",
    
    # Transaction Control
    "commit", "rollback", "savepoint",
    
    # Database Administration
    "vacuum", "analyze", "reindex", "cluster",
    
    # Dangerous Functions
    "exec", "execute", "call", "prepare",
    
    # System Operations
    "copy", "pg_dump", "pg_restore", "load",
    
    # File Operations
    "pg_read_file", "pg_write_file", "lo_import", "lo_export",
    
    # User/Role Management
    "createuser", "dropuser", "createrole", "droprole",
    "set role", "set session",
    
    # Extension/Function Creation
    "create function", "create procedure", "create trigger",
    "create extension", "create type",
    
    # Dangerous Keywords
    "into outfile", "into dumpfile", "load_file",
    "benchmark", "sleep", "waitfor",
    
    # Information Schema Abuse
    "information_schema", "pg_catalog", "pg_shadow", "pg_authid",
])


# ============================================================================
# 🚫 HARDCODED BLOCKED PATTERNS - DO NOT MODIFY
# ============================================================================
# Regex patterns to catch SQL injection and bypass attempts

BLOCKED_PATTERNS: tuple = (
    # Comment injection
    r"--",
    r"/\*",
    r"\*/",
    
    # String escape attempts
    r"\\x[0-9a-fA-F]+",
    r"chr\s*\(",
    r"char\s*\(",
    r"ascii\s*\(",
    
    # Union-based injection
    r"union\s+all\s+select",
    r"union\s+select",
    
    # Stacked queries
    r";\s*select",
    r";\s*insert",
    r";\s*update",
    r";\s*delete",
    r";\s*drop",
    r";\s*create",
    
    # Time-based injection
    r"pg_sleep\s*\(",
    r"sleep\s*\(",
    r"waitfor\s+delay",
    r"benchmark\s*\(",
    
    # Boolean-based injection
    r"'\s*or\s+'",
    r"'\s*and\s+'",
    r"1\s*=\s*1",
    r"'='",
    
    # System command execution
    r"xp_cmdshell",
    r"sp_executesql",
    r"dbms_",
    r"utl_",
    
    # Out-of-band data exfiltration
    r"dns\s*\(",
    r"http\s*\(",
    r"load_file\s*\(",
)


# ============================================================================
# 🔒 SECURITY CONFIGURATION - HARDCODED LIMITS
# ============================================================================

MAX_QUERY_LENGTH: int = 2000
MAX_RESULT_ROWS: int = 200
ALLOWED_QUERY_TYPES: frozenset = frozenset(["select"])


@dataclass
class SecurityValidationResult:
    """Result of security validation."""
    is_valid: bool
    error_message: str = ""
    blocked_reason: str = ""


class HardcodedSecurityValidator:
    """
    🔒 HARDCODED SECURITY VALIDATOR
    ===============================
    This class performs IMMUTABLE security validation on SQL queries.
    The validation rules are hardcoded and CANNOT be bypassed at runtime.
    
    Validation Order:
    1. Length Check
    2. Whitelist Check (SELECT only)
    3. Blocked Keyword Detection
    4. Blocked Pattern Detection
    5. Multiple Statement Detection
    """
    
    @staticmethod
    def validate(sql_query: str) -> SecurityValidationResult:
        """
        Validate SQL query through all security layers.
        
        Args:
            sql_query: The SQL query to validate
            
        Returns:
            SecurityValidationResult with validation status
        """
        if not sql_query or not sql_query.strip():
            return SecurityValidationResult(
                is_valid=False,
                error_message="Empty query not allowed",
                blocked_reason="EMPTY_QUERY"
            )
        
        sql_clean = sql_query.strip()
        sql_lower = sql_clean.lower()
        
        # ============================================================
        # LAYER 3.1: LENGTH CHECK
        # ============================================================
        if len(sql_clean) > MAX_QUERY_LENGTH:
            return SecurityValidationResult(
                is_valid=False,
                error_message=f"Query too long. Maximum {MAX_QUERY_LENGTH} characters allowed.",
                blocked_reason="LENGTH_EXCEEDED"
            )
        
        # ============================================================
        # LAYER 3.2: WHITELIST CHECK (SELECT ONLY)
        # ============================================================
        # Allow SELECT and WITH (CTEs - Common Table Expressions)
        # CTEs are read-only and start with "WITH ... AS (...) SELECT"
        is_select = sql_lower.startswith("select")
        is_cte = sql_lower.startswith("with") and "select" in sql_lower
        
        if not (is_select or is_cte):
            return SecurityValidationResult(
                is_valid=False,
                error_message="Only SELECT queries are allowed. This is a read-only system.",
                blocked_reason="NOT_SELECT"
            )
        
        # ============================================================
        # LAYER 3.3: BLOCKED KEYWORD DETECTION
        # ============================================================
        for keyword in BLOCKED_KEYWORDS:
            # Use word boundary matching to avoid false positives
            # e.g., "selected" should not match "select"
            pattern = rf'\b{re.escape(keyword)}\b'
            if re.search(pattern, sql_lower):
                return SecurityValidationResult(
                    is_valid=False,
                    error_message=f"🚫 BLOCKED: Query contains forbidden keyword '{keyword}'",
                    blocked_reason=f"BLOCKED_KEYWORD:{keyword.upper()}"
                )
        
        # ============================================================
        # LAYER 3.4: BLOCKED PATTERN DETECTION
        # ============================================================
        for pattern in BLOCKED_PATTERNS:
            if re.search(pattern, sql_lower, re.IGNORECASE):
                return SecurityValidationResult(
                    is_valid=False,
                    error_message="🚫 BLOCKED: Query contains suspicious pattern",
                    blocked_reason=f"BLOCKED_PATTERN:{pattern}"
                )
        
        # ============================================================
        # LAYER 3.5: MULTIPLE STATEMENT DETECTION
        # ============================================================
        # Remove strings to avoid false positives from semicolons in string literals
        sql_no_strings = re.sub(r"'[^']*'", "", sql_lower)
        sql_no_strings = re.sub(r'"[^"]*"', "", sql_no_strings)
        
        if sql_no_strings.count(';') > 1:
            return SecurityValidationResult(
                is_valid=False,
                error_message="🚫 BLOCKED: Multiple statements not allowed",
                blocked_reason="MULTIPLE_STATEMENTS"
            )
        
        # Strip trailing semicolon for clean execution
        if sql_clean.endswith(';'):
            sql_clean = sql_clean[:-1].strip()
        
        # ============================================================
        # ✅ ALL CHECKS PASSED
        # ============================================================
        return SecurityValidationResult(
            is_valid=True,
            error_message="",
            blocked_reason=""
        )
    
    @staticmethod
    def sanitize_query(sql_query: str) -> str:
        """
        Sanitize query by removing dangerous characters and ensuring LIMIT.
        Only call this AFTER validation passes.
        
        Args:
            sql_query: The validated SQL query
            
        Returns:
            Sanitized SQL query with LIMIT clause
        """
        sql_clean = sql_query.strip()
        
        # Remove trailing semicolon
        if sql_clean.endswith(';'):
            sql_clean = sql_clean[:-1].strip()
        
        # Add LIMIT if not present
        sql_lower = sql_clean.lower()
        if 'limit' not in sql_lower:
            sql_clean = f"{sql_clean} LIMIT {MAX_RESULT_ROWS}"
        
        return sql_clean


# ============================================================================
# 🔒 SINGLETON VALIDATOR INSTANCE
# ============================================================================
# Use this instance for all security validations

security_validator = HardcodedSecurityValidator()


def validate_sql_security(sql_query: str) -> Tuple[bool, str, str]:
    """
    Convenience function to validate SQL query security.
    
    Args:
        sql_query: The SQL query to validate
        
    Returns:
        Tuple of (is_valid, error_message, sanitized_query)
    """
    result = security_validator.validate(sql_query)
    
    if not result.is_valid:
        return (False, result.error_message, "")
    
    sanitized = security_validator.sanitize_query(sql_query)
    return (True, "", sanitized)