"""
Custom Exceptions
==================
Application-specific exceptions for error handling.
"""


class DBAssistantException(Exception):
    """Base exception for DB Assistant."""
    
    def __init__(self, message: str = "An error occurred"):
        self.message = message
        super().__init__(self.message)


class UnauthorizedAccessException(DBAssistantException):
    """Raised when unauthorized access is attempted."""
    
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message)


class InvalidQueryException(DBAssistantException):
    """Raised when an invalid query is detected."""
    
    def __init__(self, message: str = "Invalid query"):
        super().__init__(message)


class BlockedQueryException(DBAssistantException):
    """
    Raised when a query is blocked by security validation.
    This is the primary exception for Layer 3 security violations.
    """
    
    def __init__(self, message: str = "This query is blocked for security reasons", reason: str = ""):
        self.reason = reason
        super().__init__(message)


class DatabaseConnectionException(DBAssistantException):
    """Raised when database connection fails."""
    
    def __init__(self, message: str = "Database connection failed"):
        super().__init__(message)


class SchemaDiscoveryException(DBAssistantException):
    """Raised when schema discovery fails."""
    
    def __init__(self, message: str = "Schema discovery failed"):
        super().__init__(message)


class LLMException(DBAssistantException):
    """Raised when LLM operations fail."""
    
    def __init__(self, message: str = "LLM operation failed"):
        super().__init__(message)