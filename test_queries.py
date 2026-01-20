"""
Comprehensive test script for DB Assistant
Tests 10 essential READ-ONLY queries covering all query types
Includes both English and Hinglish queries
"""

from db_assistant import ask_db_bot
import time
import json
from datetime import datetime
from typing import Dict, List, Any

# 10 Essential Test Queries - 5 English + 5 Hinglish
TEST_QUERIES = {
    "1. Basic SELECT (English)": [
        "Show all users limit 10",
    ],
    
    "2. Basic SELECT (Hinglish)": [
        "Sabhi users dikhao limit 10",
    ],
    
    "3. Filtering (English)": [
        "Show users in ADMIN department",
    ],
    
    "4. Filtering (Hinglish)": [
        "ADMIN department ke users batao",
    ],
    
    "5. Aggregation (English)": [
        "Count tasks by department",
    ],
    
    "6. Aggregation (Hinglish)": [
        "Department wise kitne tasks hain",
    ],
    
    "7. JOIN Query (English)": [
        "List users with their task counts",
    ],
    
    "8. JOIN Query (Hinglish)": [
        "Users ke saath unke task count batao",
    ],
    
    "9. Date/Time (English)": [
        "List recent 5 delegations by created date",
    ],
    
    "10. Delegation (Hinglish)": [
        "Delegation status wise count karo",
    ],
}


class TestResult:
    """Class to store test result details."""
    def __init__(self, query: str, category: str):
        self.query = query
        self.category = category
        self.success = False
        self.execution_time = 0.0
        self.result = ""
        self.error_message = ""
        self.error_type = ""
        self.row_count = 0
        
    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "category": self.category,
            "success": self.success,
            "execution_time": round(self.execution_time, 2),
            "error_type": self.error_type,
            "error_message": self.error_message,
            "row_count": self.row_count,
        }


def analyze_error(result: str) -> tuple:
    """Analyze the error and categorize it."""
    result_lower = result.lower()
    
    # First check for ACTUAL errors (these are real failures)
    if "❌ error" in result_lower or "error:" in result_lower or "error ho gaya" in result_lower:
        if "invalid input value for enum" in result_lower:
            return "ENUM_ERROR", "Used invalid ENUM value"
        elif "date/time field value out of range" in result_lower:
            return "DATE_FORMAT_ERROR", "Date parsing failed due to format mismatch"
        elif "column" in result_lower and "does not exist" in result_lower:
            return "COLUMN_NOT_FOUND", "Referenced non-existent column"
        elif "relation" in result_lower and "does not exist" in result_lower:
            return "TABLE_NOT_FOUND", "Referenced non-existent table"
        elif "syntax error" in result_lower:
            return "SQL_SYNTAX_ERROR", "Invalid SQL syntax generated"
        elif "division by zero" in result_lower:
            return "DIVISION_BY_ZERO", "Attempted division by zero"
        elif "union types" in result_lower and "cannot be matched" in result_lower:
            return "TYPE_MISMATCH", "UNION/comparison between incompatible types"
        elif "permission denied" in result_lower:
            return "PERMISSION_ERROR", "Insufficient permissions"
        else:
            return "GENERAL_ERROR", "Database execution error"
    
    # Check for connection errors
    if "could not connect" in result_lower or "connection refused" in result_lower:
        return "CONNECTION_ERROR", "Database connection failed"
    
    if "timeout" in result_lower:
        return "TIMEOUT_ERROR", "Query execution timed out"
    
    # Check for empty response
    if result.strip() == "":
        return "EMPTY_RESPONSE", "Empty response from system"
    
    # Check for "no data found" messages (English & Hinglish)
    no_data_patterns = [
        "📭 no data found", "zero results", "koi data nahi mila",
        "0 found", "zero", "no results"
    ]
    for pattern in no_data_patterns:
        if pattern in result_lower:
            return "NO_DATA", "Query executed but returned no matching data"
    
    # If we have actual data indicators, it's a SUCCESS
    success_indicators = [
        "found", "mile", "users", "tasks", "delegations", "departments",
        "count", "total", "list", "here are", "showing", "yeh raha",
        "dikhao", "batao", "hain", "**", "1.", "2.", "3.",
    ]
    
    for indicator in success_indicators:
        if indicator in result_lower:
            return "SUCCESS", "Query executed successfully"
    
    return "SUCCESS", "No error detected"


def extract_row_count(result: str) -> int:
    """Try to extract row count from result."""
    import re
    
    patterns = [
        r'(\d+)\s*(?:found|mile|results?|rows?|records?|items?|users?|tasks?)',
        r'(?:found|showing|returned|total|dikha)[:\s]*(\d+)',
        r'there are (\d+)',
        r'(\d+)\s*(?:hain|hai)',
        r'count[:\s]*(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, result.lower())
        if match:
            return int(match.group(1))
    
    lines = result.split('\n')
    bullet_count = sum(1 for line in lines if line.strip().startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.')))
    if bullet_count > 0:
        return bullet_count
    
    return 0


def run_single_test(query: str, category: str, test_num: int, total: int) -> TestResult:
    """Run a single test and collect detailed results."""
    result = TestResult(query, category)
    
    # Detect if Hinglish
    is_hinglish = "hinglish" in category.lower()
    
    print(f"\n{'='*70}")
    print(f"🧪 TEST [{test_num}/{total}] - {category}")
    if is_hinglish:
        print(f"🌐 Language: HINGLISH")
    else:
        print(f"🌐 Language: ENGLISH")
    print(f"{'='*70}")
    print(f"📝 Query: {query}")
    print(f"{'─'*70}")
    
    start_time = time.time()
    try:
        response = ask_db_bot(query, verbose=False)
        result.execution_time = time.time() - start_time
        result.result = response
        
        error_type, error_msg = analyze_error(response)
        
        if error_type == "SUCCESS":
            result.success = True
            result.row_count = extract_row_count(response)
        else:
            result.success = False
            result.error_type = error_type
            result.error_message = error_msg
        
        if result.success:
            print(f"✅ SUCCESS | ⏱️ {result.execution_time:.2f}s | 📊 ~{result.row_count} rows")
            print(f"{'─'*70}")
            preview = response[:500] + "..." if len(response) > 500 else response
            print(f"📋 Response:\n{preview}")
        else:
            print(f"❌ FAILED | ⏱️ {result.execution_time:.2f}s")
            print(f"🔴 Error Type: {result.error_type}")
            print(f"🔴 Reason: {result.error_message}")
            print(f"{'─'*70}")
            print(f"📋 Response:\n{response[:400]}...")
                
    except Exception as e:
        result.execution_time = time.time() - start_time
        result.success = False
        result.error_type = "EXCEPTION"
        result.error_message = str(e)
        result.result = str(e)
        
        print(f"❌ EXCEPTION | ⏱️ {result.execution_time:.2f}s")
        print(f"🔴 {str(e)}")
    
    return result


def run_all_tests() -> tuple:
    """Run all 10 tests and collect results."""
    all_results = {}
    total_queries = sum(len(queries) for queries in TEST_QUERIES.values())
    current_query = 0
    
    print("\n" + "🤖"*35)
    print("       DB ASSISTANT - 10 ESSENTIAL TESTS")
    print("       (English + Hinglish Support)")
    print("🤖"*35)
    print(f"\n📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Total queries: {total_queries}")
    print(f"📂 Categories: {len(TEST_QUERIES)}")
    print(f"🌐 Languages: English (5) + Hinglish (5)")
    
    overall_start = time.time()
    
    for category, queries in TEST_QUERIES.items():
        category_results = []
        
        for query in queries:
            current_query += 1
            result = run_single_test(query, category, current_query, total_queries)
            category_results.append(result)
            time.sleep(0.5)
        
        all_results[category] = category_results
    
    total_time = time.time() - overall_start
    return all_results, total_time


def generate_report(all_results: Dict[str, List[TestResult]], total_time: float):
    """Generate comprehensive test report."""
    
    total_tests = 0
    total_passed = 0
    english_passed = 0
    english_total = 0
    hinglish_passed = 0
    hinglish_total = 0
    all_failures = []
    all_successes = []
    error_types = {}
    category_stats = []
    
    for category, results in all_results.items():
        is_hinglish = "hinglish" in category.lower()
        passed = sum(1 for r in results if r.success)
        failed = len(results) - passed
        total_tests += len(results)
        total_passed += passed
        
        if is_hinglish:
            hinglish_total += len(results)
            hinglish_passed += passed
        else:
            english_total += len(results)
            english_passed += passed
        
        category_stats.append({
            "category": category,
            "language": "Hinglish" if is_hinglish else "English",
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / len(results) * 100) if results else 0,
            "avg_time": sum(r.execution_time for r in results) / len(results) if results else 0
        })
        
        for r in results:
            if r.success:
                all_successes.append(r)
            else:
                all_failures.append(r)
                error_types[r.error_type] = error_types.get(r.error_type, 0) + 1
    
    total_failed = total_tests - total_passed
    pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    # Print Report
    print("\n\n" + "="*70)
    print("📊 TEST REPORT SUMMARY")
    print("="*70)
    print(f"📅 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️  Total Time: {total_time:.1f}s")
    
    if pass_rate == 100:
        status_emoji = "🎉"
    elif pass_rate >= 80:
        status_emoji = "👍"
    elif pass_rate >= 50:
        status_emoji = "⚠️"
    else:
        status_emoji = "🚨"
    
    print(f"""
    {status_emoji} OVERALL RESULTS:
    ┌─────────────────────────────────┐
    │  ✅ Passed:     {total_passed:>3} / {total_tests:<3}        │
    │  ❌ Failed:     {total_failed:>3} / {total_tests:<3}        │
    │  📈 Pass Rate:  {pass_rate:>5.1f}%         │
    │  ⚡ Avg Time:   {total_time/total_tests:>5.2f}s        │
    └─────────────────────────────────┘
    
    🌐 LANGUAGE BREAKDOWN:
    ┌─────────────────────────────────┐
    │  🇬🇧 English:   {english_passed:>3} / {english_total:<3} passed   │
    │  🇮🇳 Hinglish:  {hinglish_passed:>3} / {hinglish_total:<3} passed   │
    └─────────────────────────────────┘
    """)
    
    # Category Breakdown
    print("─"*70)
    print("📂 CATEGORY RESULTS")
    print("─"*70)
    
    for stat in category_stats:
        icon = "✅" if stat["failed"] == 0 else "❌"
        lang_icon = "🇮🇳" if stat["language"] == "Hinglish" else "🇬🇧"
        print(f"{icon} {lang_icon} {stat['category']:<35} {stat['avg_time']:>6.2f}s")
    
    # Failures
    if all_failures:
        print("\n" + "─"*70)
        print(f"❌ FAILURES ({len(all_failures)})")
        print("─"*70)
        
        for f in all_failures:
            print(f"  ❌ {f.query}")
            print(f"     → {f.error_type}: {f.error_message}")
    
    # Successes
    print("\n" + "─"*70)
    print(f"✅ SUCCESSES ({len(all_successes)})")
    print("─"*70)
    
    for s in all_successes:
        lang = "🇮🇳" if "hinglish" in s.category.lower() else "🇬🇧"
        print(f"  ✅ {lang} [{s.execution_time:.1f}s] {s.query}")
    
    # Save report
    report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_data = {
        "test_date": datetime.now().isoformat(),
        "total_time": round(total_time, 2),
        "summary": {
            "total": total_tests,
            "passed": total_passed,
            "failed": total_failed,
            "pass_rate": round(pass_rate, 1),
            "english_passed": english_passed,
            "english_total": english_total,
            "hinglish_passed": hinglish_passed,
            "hinglish_total": hinglish_total,
        },
        "category_stats": category_stats,
        "error_types": error_types,
        "failures": [f.to_dict() for f in all_failures],
        "successes": [s.to_dict() for s in all_successes]
    }
    
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Report saved: {report_file}")
    print("\n" + "="*70)
    print("🏁 TEST COMPLETE")
    print("="*70)
    
    return report_data


def main():
    """Main entry point."""
    all_results, total_time = run_all_tests()
    generate_report(all_results, total_time)


if __name__ == "__main__":
    main()