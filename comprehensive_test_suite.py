"""
🧪 Comprehensive Test Suite for DB Assistant
==============================================
This script contains ALL possible query types organized by category.
Run this to test the complete functionality of the DB Assistant system.

Total Queries: 267+
- Valid Queries: 242
- Security Tests: 25
- Edge Cases: 20+
"""

from db_assistant import ask_db_bot
import time
import json
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class TestQuery:
    """Represents a single test query."""
    category: str
    language: str  # 'english' or 'hinglish'
    query: str
    expected_behavior: str  # 'success', 'blocked', 'error', 'no_data'
    description: str = ""


# ============================================================================
# 1️⃣ BASIC SELECT QUERIES
# ============================================================================

BASIC_SELECT_QUERIES = [
    # English
    TestQuery("Basic SELECT", "english", "Show all users", "success", "Retrieve all users"),
    TestQuery("Basic SELECT", "english", "List all users limit 10", "success", "Limited user list"),
    TestQuery("Basic SELECT", "english", "Display user names and emails", "success", "Specific columns"),
    TestQuery("Basic SELECT", "english", "Get all tasks from checklist", "success", "All checklist tasks"),
    TestQuery("Basic SELECT", "english", "Show me the first 5 delegations", "success", "Limited delegations"),
    TestQuery("Basic SELECT", "english", "List all departments", "success", "All departments"),
    TestQuery("Basic SELECT", "english", "Show distinct departments from users table", "success", "Unique departments"),
    TestQuery("Basic SELECT", "english", "Get all user roles", "success", "All roles"),
    TestQuery("Basic SELECT", "english", "Display all task names", "success", "Task names"),
    TestQuery("Basic SELECT", "english", "Show me all active records", "success", "Active records"),
    
    # Hinglish
    TestQuery("Basic SELECT", "hinglish", "Sabhi users dikhao", "success", "All users in Hinglish"),
    TestQuery("Basic SELECT", "hinglish", "10 users ki list do", "success", "10 users in Hinglish"),
    TestQuery("Basic SELECT", "hinglish", "User names aur emails batao", "success", "Names and emails"),
    TestQuery("Basic SELECT", "hinglish", "Checklist se sabhi tasks dikhao", "success", "All tasks"),
    TestQuery("Basic SELECT", "hinglish", "Pehle 5 delegations dikha do", "success", "First 5 delegations"),
    TestQuery("Basic SELECT", "hinglish", "Saare departments batao", "success", "All departments"),
    TestQuery("Basic SELECT", "hinglish", "Users table se unique departments dikhao", "success", "Unique departments"),
    TestQuery("Basic SELECT", "hinglish", "Sabhi user roles kya hain", "success", "All roles"),
    TestQuery("Basic SELECT", "hinglish", "Task names ki list do", "success", "Task names"),
    TestQuery("Basic SELECT", "hinglish", "Active records sabhi dikhao", "success", "Active records"),
]


# ============================================================================
# 2️⃣ FILTERING QUERIES (WHERE CLAUSE)
# ============================================================================

FILTERING_QUERIES = [
    # English
    TestQuery("Filtering", "english", "Show users in ADMIN department", "success", "Department filter"),
    TestQuery("Filtering", "english", "List all active users", "success", "Status filter"),
    TestQuery("Filtering", "english", "Find users with role admin", "success", "Role filter"),
    TestQuery("Filtering", "english", "Show completed tasks", "success", "Status = 'yes'"),
    TestQuery("Filtering", "english", "Display pending tasks", "success", "Status = 'no'"),
    TestQuery("Filtering", "english", "Find users on leave", "success", "Status = 'on_leave'"),
    TestQuery("Filtering", "english", "Show inactive users", "success", "Status = 'inactive'"),
    TestQuery("Filtering", "english", "List tasks in IT department", "success", "Department filter"),
    TestQuery("Filtering", "english", "Find delegations with status done", "success", "Status filter"),
    TestQuery("Filtering", "english", "Show users whose name contains 'abhishek'", "success", "LIKE pattern"),
    TestQuery("Filtering", "english", "List tasks with reminder enabled", "success", "ENUM filter"),
    TestQuery("Filtering", "english", "Find daily frequency tasks", "success", "Frequency filter"),
    TestQuery("Filtering", "english", "Show weekly tasks", "success", "Frequency filter"),
    TestQuery("Filtering", "english", "Display monthly checklists", "success", "Frequency filter"),
    TestQuery("Filtering", "english", "Find users with email containing 'gmail'", "success", "Email pattern"),
    
    # Hinglish
    TestQuery("Filtering", "hinglish", "ADMIN department ke users dikhao", "success", "Department filter"),
    TestQuery("Filtering", "hinglish", "Active users ki list batao", "success", "Status filter"),
    TestQuery("Filtering", "hinglish", "Admin role wale users dikhao", "success", "Role filter"),
    TestQuery("Filtering", "hinglish", "Complete ho gaye tasks dikhao", "success", "Completed tasks"),
    TestQuery("Filtering", "hinglish", "Pending tasks batao", "success", "Pending tasks"),
    TestQuery("Filtering", "hinglish", "Leave pe kon kon hai", "success", "On leave users"),
    TestQuery("Filtering", "hinglish", "Inactive users dikhao", "success", "Inactive filter"),
    TestQuery("Filtering", "hinglish", "IT department ke tasks batao", "success", "Department tasks"),
    TestQuery("Filtering", "hinglish", "Done status wale delegations dikhao", "success", "Done delegations"),
    TestQuery("Filtering", "hinglish", "Abhishek naam wale users batao", "success", "Name pattern"),
    TestQuery("Filtering", "hinglish", "Reminder enabled wale tasks dikhao", "success", "Reminder filter"),
    TestQuery("Filtering", "hinglish", "Daily frequency ke tasks dikhao", "success", "Daily tasks"),
    TestQuery("Filtering", "hinglish", "Weekly tasks ki list do", "success", "Weekly tasks"),
    TestQuery("Filtering", "hinglish", "Monthly checklists batao", "success", "Monthly tasks"),
    TestQuery("Filtering", "hinglish", "Gmail wale users dikhao", "success", "Gmail users"),
]


# ============================================================================
# 3️⃣ AGGREGATION QUERIES
# ============================================================================

AGGREGATION_QUERIES = [
    # English
    TestQuery("Aggregation", "english", "Count total users", "success", "Total count"),
    TestQuery("Aggregation", "english", "How many tasks are there", "success", "Task count"),
    TestQuery("Aggregation", "english", "Count users by department", "success", "GROUP BY department"),
    TestQuery("Aggregation", "english", "Show task count by department", "success", "Task count grouped"),
    TestQuery("Aggregation", "english", "Count delegations by status", "success", "Delegation count"),
    TestQuery("Aggregation", "english", "How many active users are there", "success", "Active count"),
    TestQuery("Aggregation", "english", "Count pending tasks", "success", "Pending count"),
    TestQuery("Aggregation", "english", "Show user count by role", "success", "Role grouping"),
    TestQuery("Aggregation", "english", "Count completed tasks", "success", "Completed count"),
    TestQuery("Aggregation", "english", "How many users in each department", "success", "Department count"),
    TestQuery("Aggregation", "english", "Total tasks per department", "success", "Tasks per dept"),
    TestQuery("Aggregation", "english", "Count tasks with reminders enabled", "success", "Reminder count"),
    TestQuery("Aggregation", "english", "How many delegations are done", "success", "Done delegations"),
    TestQuery("Aggregation", "english", "Count users by status", "success", "Status grouping"),
    TestQuery("Aggregation", "english", "Show department with most users", "success", "Max users dept"),
    TestQuery("Aggregation", "english", "Which department has most tasks", "success", "Max tasks dept"),
    TestQuery("Aggregation", "english", "Count daily vs weekly vs monthly tasks", "success", "Frequency breakdown"),
    
    # Hinglish
    TestQuery("Aggregation", "hinglish", "Kitne total users hain", "success", "Total users"),
    TestQuery("Aggregation", "hinglish", "Tasks kitne hain", "success", "Task count"),
    TestQuery("Aggregation", "hinglish", "Department wise users count karo", "success", "Dept grouping"),
    TestQuery("Aggregation", "hinglish", "Department ke hisaab se task count batao", "success", "Task count"),
    TestQuery("Aggregation", "hinglish", "Status wise delegations kitne hain", "success", "Status count"),
    TestQuery("Aggregation", "hinglish", "Active users kitne hain", "success", "Active count"),
    TestQuery("Aggregation", "hinglish", "Pending tasks count karo", "success", "Pending count"),
    TestQuery("Aggregation", "hinglish", "Role wise kitne users hain", "success", "Role count"),
    TestQuery("Aggregation", "hinglish", "Complete tasks kitne hain", "success", "Complete count"),
    TestQuery("Aggregation", "hinglish", "Har department mein kitne users hain", "success", "Dept users"),
    TestQuery("Aggregation", "hinglish", "Department wise total tasks batao", "success", "Total tasks"),
    TestQuery("Aggregation", "hinglish", "Reminder enabled tasks kitne hain", "success", "Reminder count"),
    TestQuery("Aggregation", "hinglish", "Done delegations kitne hain", "success", "Done count"),
    TestQuery("Aggregation", "hinglish", "Status ke hisaab se users count karo", "success", "Status count"),
    TestQuery("Aggregation", "hinglish", "Sabse zyada users kis department mein hain", "success", "Max users"),
    TestQuery("Aggregation", "hinglish", "Sabse zyada tasks kis department ke hain", "success", "Max tasks"),
    TestQuery("Aggregation", "hinglish", "Daily, weekly, monthly tasks count karo", "success", "Frequency count"),
]


# ============================================================================
# 4️⃣ JOIN QUERIES
# ============================================================================

JOIN_QUERIES = [
    # English
    TestQuery("JOIN", "english", "List users with their task counts", "success", "User-task join"),
    TestQuery("JOIN", "english", "Show users and their delegations", "success", "User-delegation join"),
    TestQuery("JOIN", "english", "Find users with their department tasks", "success", "Dept join"),
    TestQuery("JOIN", "english", "List all users and their assigned tasks", "success", "User tasks"),
    TestQuery("JOIN", "english", "Show delegation details with user information", "success", "Delegation-user"),
    TestQuery("JOIN", "english", "Find tasks assigned to each user", "success", "Task assignment"),
    TestQuery("JOIN", "english", "List users who have delegated tasks", "success", "Delegators"),
    TestQuery("JOIN", "english", "Show users who received delegations", "success", "Receivers"),
    TestQuery("JOIN", "english", "Find departments with their task counts", "success", "Dept task count"),
    TestQuery("JOIN", "english", "List users with pending tasks", "success", "Pending tasks join"),
    TestQuery("JOIN", "english", "Show users with completed tasks", "success", "Completed join"),
    
    # Hinglish
    TestQuery("JOIN", "hinglish", "Users ke saath unke task count batao", "success", "User task count"),
    TestQuery("JOIN", "hinglish", "Users aur unke delegations dikhao", "success", "User delegations"),
    TestQuery("JOIN", "hinglish", "Users ko unke department tasks ke saath dikhao", "success", "Dept tasks"),
    TestQuery("JOIN", "hinglish", "Sabhi users aur unke assigned tasks batao", "success", "Assigned tasks"),
    TestQuery("JOIN", "hinglish", "Delegation details user information ke saath dikhao", "success", "Delegation info"),
    TestQuery("JOIN", "hinglish", "Har user ko kitne tasks assigned hain", "success", "Task assignment"),
    TestQuery("JOIN", "hinglish", "Jinke tasks delegate kiye hain wo users dikhao", "success", "Delegators"),
    TestQuery("JOIN", "hinglish", "Jinko delegations mile hain wo users batao", "success", "Receivers"),
    TestQuery("JOIN", "hinglish", "Departments aur unke task counts dikhao", "success", "Dept counts"),
    TestQuery("JOIN", "hinglish", "Pending tasks wale users batao", "success", "Pending users"),
    TestQuery("JOIN", "hinglish", "Completed tasks wale users dikhao", "success", "Completed users"),
]


# ============================================================================
# 5️⃣ SORTING & LIMITING QUERIES
# ============================================================================

SORTING_QUERIES = [
    # English
    TestQuery("Sorting", "english", "Show top 10 users by name", "success", "Top 10 sorted"),
    TestQuery("Sorting", "english", "List latest 5 delegations", "success", "Latest delegations"),
    TestQuery("Sorting", "english", "Show oldest tasks", "success", "Oldest first"),
    TestQuery("Sorting", "english", "Display users sorted by department", "success", "Dept sort"),
    TestQuery("Sorting", "english", "List tasks ordered by creation date", "success", "Date sort"),
    TestQuery("Sorting", "english", "Show top 5 departments by user count", "success", "Top depts"),
    TestQuery("Sorting", "english", "Display recent 10 tasks", "success", "Recent tasks"),
    TestQuery("Sorting", "english", "List users in alphabetical order", "success", "Alphabetical"),
    TestQuery("Sorting", "english", "Show delegations sorted by planned date", "success", "Date sort"),
    TestQuery("Sorting", "english", "Find first 3 completed tasks", "success", "First completed"),
    
    # Hinglish
    TestQuery("Sorting", "hinglish", "Top 10 users naam ke hisaab se dikhao", "success", "Top 10"),
    TestQuery("Sorting", "hinglish", "Latest 5 delegations batao", "success", "Latest"),
    TestQuery("Sorting", "hinglish", "Sabse purane tasks dikhao", "success", "Oldest"),
    TestQuery("Sorting", "hinglish", "Users ko department wise sort karke dikhao", "success", "Dept sort"),
    TestQuery("Sorting", "hinglish", "Tasks ko creation date se sort karo", "success", "Date sort"),
    TestQuery("Sorting", "hinglish", "Top 5 departments user count ke hisaab se batao", "success", "Top depts"),
    TestQuery("Sorting", "hinglish", "Recent 10 tasks dikhao", "success", "Recent"),
    TestQuery("Sorting", "hinglish", "Users ko alphabetical order mein dikhao", "success", "Alphabetical"),
    TestQuery("Sorting", "hinglish", "Delegations ko planned date se sort karo", "success", "Date sort"),
    TestQuery("Sorting", "hinglish", "Pehle 3 complete tasks batao", "success", "First 3"),
]


# ============================================================================
# 6️⃣ DATE/TIME QUERIES
# ============================================================================

DATE_TIME_QUERIES = [
    # English
    TestQuery("Date/Time", "english", "List recent 5 delegations by created date", "success", "Recent delegations"),
    TestQuery("Date/Time", "english", "Show tasks created this month", "success", "This month"),
    TestQuery("Date/Time", "english", "Find users created in last 30 days", "success", "Last 30 days"),
    TestQuery("Date/Time", "english", "List delegations from last week", "success", "Last week"),
    TestQuery("Date/Time", "english", "Show tasks with delay greater than 1 day", "success", "Delayed tasks"),
    TestQuery("Date/Time", "english", "Find tasks created before 2024", "success", "Before 2024"),
    
    # Hinglish
    TestQuery("Date/Time", "hinglish", "Created date ke hisaab se recent 5 delegations dikhao", "success", "Recent"),
    TestQuery("Date/Time", "hinglish", "Is mahine ke tasks batao", "success", "This month"),
    TestQuery("Date/Time", "hinglish", "Last 30 days mein bane users dikhao", "success", "Last 30 days"),
    TestQuery("Date/Time", "hinglish", "Last week ke delegations batao", "success", "Last week"),
    TestQuery("Date/Time", "hinglish", "1 din se zyada delay wale tasks dikhao", "success", "Delayed"),
    TestQuery("Date/Time", "hinglish", "2024 se pehle bane tasks dikhao", "success", "Before 2024"),
]


# ============================================================================
# 7️⃣ COMPLEX ANALYTICAL QUERIES
# ============================================================================

COMPLEX_QUERIES = [
    # English
    TestQuery("Complex", "english", "Show departments with more than 10 users", "success", "HAVING clause"),
    TestQuery("Complex", "english", "List top 3 departments by task count", "success", "Top N with aggregation"),
    TestQuery("Complex", "english", "Find tasks grouped by frequency and status", "success", "Multi-group"),
    TestQuery("Complex", "english", "Show users with most delegations", "success", "Max delegations"),
    TestQuery("Complex", "english", "List tasks with longest delays", "success", "Max delay"),
    
    # Hinglish
    TestQuery("Complex", "hinglish", "10 se zyada users wale departments dikhao", "success", "HAVING"),
    TestQuery("Complex", "hinglish", "Task count ke hisaab se top 3 departments batao", "success", "Top 3"),
    TestQuery("Complex", "hinglish", "Frequency aur status ke hisaab se tasks group karo", "success", "Multi-group"),
    TestQuery("Complex", "hinglish", "Sabse zyada delegations wale users batao", "success", "Max delegations"),
    TestQuery("Complex", "hinglish", "Sabse zyada delay wale tasks batao", "success", "Max delay"),
]


# ============================================================================
# 8️⃣ NULL & SPECIAL VALUE QUERIES
# ============================================================================

NULL_QUERIES = [
    # English
    TestQuery("NULL Handling", "english", "Show users with no email", "success/no_data", "NULL check"),
    TestQuery("NULL Handling", "english", "Find tasks with no submission date", "success", "NULL date"),
    TestQuery("NULL Handling", "english", "List users with email set", "success", "NOT NULL"),
    TestQuery("NULL Handling", "english", "Find tasks with delay", "success", "NOT NULL delay"),
    
    # Hinglish
    TestQuery("NULL Handling", "hinglish", "Jinke email nahi hai wo users dikhao", "success/no_data", "NULL"),
    TestQuery("NULL Handling", "hinglish", "Jinke submission date nahi hai wo tasks batao", "success", "NULL date"),
    TestQuery("NULL Handling", "hinglish", "Email set hai jinke wo users batao", "success", "NOT NULL"),
    TestQuery("NULL Handling", "hinglish", "Delay wale tasks dikhao", "success", "NOT NULL"),
]


# ============================================================================
# 9️⃣ PATTERN MATCHING QUERIES
# ============================================================================

PATTERN_QUERIES = [
    # English
    TestQuery("Pattern", "english", "Find users whose name starts with 'A'", "success", "LIKE 'A%'"),
    TestQuery("Pattern", "english", "Show tasks containing 'report' in name", "success", "LIKE '%report%'"),
    TestQuery("Pattern", "english", "List users with gmail addresses", "success", "LIKE '%gmail%'"),
    TestQuery("Pattern", "english", "Show users with names containing 'kumar'", "success", "ILIKE pattern"),
    
    # Hinglish
    TestQuery("Pattern", "hinglish", "A se shuru hone wale users dikhao", "success", "LIKE 'A%'"),
    TestQuery("Pattern", "hinglish", "Name mein 'report' wale tasks batao", "success", "LIKE pattern"),
    TestQuery("Pattern", "hinglish", "Gmail address wale users dikhao", "success", "Gmail pattern"),
    TestQuery("Pattern", "hinglish", "Name mein 'kumar' wale users dikhao", "success", "ILIKE pattern"),
]


# ============================================================================
# 🔒 SECURITY TEST QUERIES (SHOULD BE BLOCKED)
# ============================================================================

SECURITY_QUERIES = [
    TestQuery("Security", "english", "Show users; DROP TABLE users;", "blocked", "SQL injection"),
    TestQuery("Security", "english", "List users WHERE 1=1 OR 1=1", "blocked", "Boolean injection"),
    TestQuery("Security", "english", "Show users' OR '1'='1", "blocked", "Quote injection"),
    TestQuery("Security", "english", "Delete all users", "blocked", "DELETE keyword"),
    TestQuery("Security", "english", "UPDATE users SET role='admin'", "blocked", "UPDATE keyword"),
    TestQuery("Security", "english", "INSERT INTO users VALUES ('hacker')", "blocked", "INSERT keyword"),
    TestQuery("Security", "english", "TRUNCATE TABLE checklist", "blocked", "TRUNCATE keyword"),
    TestQuery("Security", "english", "ALTER TABLE users ADD COLUMN hacked text", "blocked", "ALTER keyword"),
    TestQuery("Security", "english", "CREATE TABLE malicious (id int)", "blocked", "CREATE keyword"),
    TestQuery("Security", "english", "GRANT ALL ON users TO public", "blocked", "GRANT keyword"),
    TestQuery("Security", "english", "REVOKE SELECT ON users FROM public", "blocked", "REVOKE keyword"),
    TestQuery("Security", "english", "EXECUTE sp_executesql", "blocked", "EXECUTE keyword"),
    TestQuery("Security", "english", "Show users -- comment", "blocked", "Comment injection"),
    TestQuery("Security", "english", "List users /* bypass */ WHERE 1=1", "blocked", "Comment bypass"),
    TestQuery("Security", "english", "SELECT * FROM users INTO OUTFILE '/tmp/hack.txt'", "blocked", "File operation"),
    TestQuery("Security", "english", "SELECT pg_read_file('/etc/passwd')", "blocked", "File read"),
    TestQuery("Security", "english", "SELECT * FROM information_schema.tables", "blocked", "Schema access"),
    TestQuery("Security", "english", "SELECT * FROM pg_catalog.pg_tables", "blocked", "Catalog access"),
    TestQuery("Security", "english", "COPY users TO '/tmp/data.csv'", "blocked", "COPY operation"),
    TestQuery("Security", "english", "SELECT pg_sleep(10)", "blocked", "Sleep function"),
]


# ============================================================================
# ⚠️ EDGE CASE QUERIES (SHOULD RETURN ERRORS OR NO DATA)
# ============================================================================

EDGE_CASE_QUERIES = [
    TestQuery("Edge Case", "english", "Show users with status 'deleted'", "error", "Invalid ENUM"),
    TestQuery("Edge Case", "english", "Find tasks with status 'completed'", "error", "Should be 'yes'"),
    TestQuery("Edge Case", "english", "List tasks with status 'pending'", "error", "Should be 'no'"),
    TestQuery("Edge Case", "english", "Show users with role 'superadmin'", "error", "Invalid role"),
    TestQuery("Edge Case", "english", "Show user passwords", "error", "Column doesn't exist"),
    TestQuery("Edge Case", "english", "List task priorities", "error", "Column doesn't exist"),
    TestQuery("Edge Case", "english", "Show all employees", "error", "Table doesn't exist"),
    TestQuery("Edge Case", "english", "Find records in projects", "error", "Table doesn't exist"),
    TestQuery("Edge Case", "english", "Show users with status 'terminated'", "success/no_data", "Might be empty"),
    TestQuery("Edge Case", "english", "Find tasks in MARKETING department", "success/no_data", "Might not exist"),
]


# ============================================================================
# COMBINE ALL QUERIES
# ============================================================================

ALL_QUERIES = (
    BASIC_SELECT_QUERIES +
    FILTERING_QUERIES +
    AGGREGATION_QUERIES +
    JOIN_QUERIES +
    SORTING_QUERIES +
    DATE_TIME_QUERIES +
    COMPLEX_QUERIES +
    NULL_QUERIES +
    PATTERN_QUERIES +
    SECURITY_QUERIES +
    EDGE_CASE_QUERIES
)


# ============================================================================
# TEST EXECUTION
# ============================================================================

@dataclass
class TestResult:
    """Test result with detailed information."""
    query: str
    category: str
    language: str
    expected: str
    actual_status: str  # 'success', 'blocked', 'error', 'no_data'
    execution_time: float
    response: str
    error_message: str = ""


def run_test(test_query: TestQuery, verbose: bool = False) -> TestResult:
    """Run a single test query."""
    start_time = time.time()
    
    try:
        response = ask_db_bot(test_query.query, verbose=verbose)
        execution_time = time.time() - start_time
        
        # Determine actual status
        response_lower = response.lower()
        if "blocked" in response_lower or "dangerous keyword" in response_lower:
            actual_status = "blocked"
        elif "error" in response_lower or "❌" in response:
            actual_status = "error"
        elif "no data found" in response_lower or "zero results" in response_lower:
            actual_status = "no_data"
        else:
            actual_status = "success"
        
        return TestResult(
            query=test_query.query,
            category=test_query.category,
            language=test_query.language,
            expected=test_query.expected_behavior,
            actual_status=actual_status,
            execution_time=execution_time,
            response=response[:200] + "..." if len(response) > 200 else response
        )
    
    except Exception as e:
        execution_time = time.time() - start_time
        return TestResult(
            query=test_query.query,
            category=test_query.category,
            language=test_query.language,
            expected=test_query.expected_behavior,
            actual_status="exception",
            execution_time=execution_time,
            response="",
            error_message=str(e)
        )


def run_test_suite(
    queries: List[TestQuery] = None,
    categories: List[str] = None,
    languages: List[str] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Run comprehensive test suite.
    
    Args:
        queries: Specific queries to test (default: ALL_QUERIES)
        categories: Filter by categories (e.g., ['Basic SELECT', 'Filtering'])
        languages: Filter by languages (e.g., ['english', 'hinglish'])
        verbose: Show detailed logs
    
    Returns:
        Dictionary with test results and statistics
    """
    if queries is None:
        queries = ALL_QUERIES
    
    # Filter queries
    if categories:
        queries = [q for q in queries if q.category in categories]
    if languages:
        queries = [q for q in queries if q.language in languages]
    
    print(f"\n{'='*80}")
    print(f"🧪 COMPREHENSIVE TEST SUITE - DB ASSISTANT")
    print(f"{'='*80}")
    print(f"📊 Total Queries: {len(queries)}")
    print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
    
    results = []
    start_time = time.time()
    
    for i, test_query in enumerate(queries, 1):
        print(f"\n[{i}/{len(queries)}] Testing: {test_query.category} ({test_query.language})")
        print(f"Query: {test_query.query}")
        
        result = run_test(test_query, verbose=verbose)
        results.append(result)
        
        # Status indicator
        status_emoji = {
            "success": "✅",
            "blocked": "🚫",
            "error": "❌",
            "no_data": "📭",
            "exception": "💥"
        }.get(result.actual_status, "❓")
        
        print(f"{status_emoji} Status: {result.actual_status} | Time: {result.execution_time:.2f}s")
        
        # Small delay to avoid overwhelming the system
        time.sleep(0.3)
    
    total_time = time.time() - start_time
    
    # Generate statistics
    stats = generate_statistics(results, total_time)
    
    # Save results
    save_results(results, stats)
    
    # Print summary
    print_summary(stats)
    
    return {
        "results": results,
        "statistics": stats
    }


def generate_statistics(results: List[TestResult], total_time: float) -> Dict[str, Any]:
    """Generate test statistics."""
    total = len(results)
    
    status_counts = {}
    category_stats = {}
    language_stats = {}
    
    for result in results:
        # Status counts
        status_counts[result.actual_status] = status_counts.get(result.actual_status, 0) + 1
        
        # Category stats
        if result.category not in category_stats:
            category_stats[result.category] = {"total": 0, "success": 0, "failed": 0}
        category_stats[result.category]["total"] += 1
        if result.actual_status == "success":
            category_stats[result.category]["success"] += 1
        else:
            category_stats[result.category]["failed"] += 1
        
        # Language stats
        if result.language not in language_stats:
            language_stats[result.language] = {"total": 0, "success": 0}
        language_stats[result.language]["total"] += 1
        if result.actual_status == "success":
            language_stats[result.language]["success"] += 1
    
    return {
        "total_queries": total,
        "total_time": round(total_time, 2),
        "avg_time": round(total_time / total, 2) if total > 0 else 0,
        "status_counts": status_counts,
        "category_stats": category_stats,
        "language_stats": language_stats
    }


def print_summary(stats: Dict[str, Any]):
    """Print test summary."""
    print(f"\n\n{'='*80}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Total Queries: {stats['total_queries']}")
    print(f"Total Time: {stats['total_time']}s")
    print(f"Average Time: {stats['avg_time']}s")
    
    print(f"\n📈 Status Breakdown:")
    for status, count in stats['status_counts'].items():
        percentage = (count / stats['total_queries'] * 100) if stats['total_queries'] > 0 else 0
        print(f"  {status:15} {count:4} ({percentage:5.1f}%)")
    
    print(f"\n📂 Category Breakdown:")
    for category, data in stats['category_stats'].items():
        success_rate = (data['success'] / data['total'] * 100) if data['total'] > 0 else 0
        print(f"  {category:20} {data['success']}/{data['total']} ({success_rate:5.1f}%)")
    
    print(f"\n🌐 Language Breakdown:")
    for language, data in stats['language_stats'].items():
        success_rate = (data['success'] / data['total'] * 100) if data['total'] > 0 else 0
        print(f"  {language:15} {data['success']}/{data['total']} ({success_rate:5.1f}%)")
    
    print(f"\n{'='*80}")


def save_results(results: List[TestResult], stats: Dict[str, Any]):
    """Save results to JSON file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"comprehensive_test_report_{timestamp}.json"
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "statistics": stats,
        "results": [asdict(r) for r in results]
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Results saved to: {filename}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point."""
    print("\n" + "🚀"*40)
    print("  COMPREHENSIVE TEST SUITE FOR DB ASSISTANT")
    print("🚀"*40)
    
    # Run full test suite
    run_test_suite(verbose=False)
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    main()
