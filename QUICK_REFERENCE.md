# 🎯 Quick Reference Guide - DB Assistant Test Queries

## 📌 Quick Start

### Run All Tests:
```python
python comprehensive_test_suite.py
```

### Run Specific Categories:
```python
from comprehensive_test_suite import run_test_suite

# Test only basic queries
run_test_suite(categories=["Basic SELECT"])

# Test only filtering and aggregation
run_test_suite(categories=["Filtering", "Aggregation"])

# Test only security queries
run_test_suite(categories=["Security"])
```

### Run Specific Language:
```python
# Test only English queries
run_test_suite(languages=["english"])

# Test only Hinglish queries
run_test_suite(languages=["hinglish"])
```

---

## 📊 Query Categories Summary

| Category | English | Hinglish | Total | Description |
|----------|---------|----------|-------|-------------|
| Basic SELECT | 10 | 10 | 20 | Simple data retrieval |
| Filtering | 15 | 15 | 30 | WHERE clause queries |
| Aggregation | 17 | 17 | 34 | COUNT, GROUP BY, etc. |
| JOIN | 11 | 11 | 22 | Multi-table queries |
| Sorting | 10 | 10 | 20 | ORDER BY, LIMIT |
| Date/Time | 6 | 6 | 12 | Date filtering |
| Complex | 5 | 5 | 10 | Advanced analytics |
| NULL Handling | 4 | 4 | 8 | NULL checks |
| Pattern | 4 | 4 | 8 | LIKE/ILIKE queries |
| Security | 20 | 0 | 20 | Should be blocked |
| Edge Cases | 10 | 0 | 10 | Error scenarios |
| **TOTAL** | **112** | **82** | **194** | |

---

## 🔥 Top 20 Must-Test Queries

### 1. Basic Retrieval
```
"Show all users limit 10"
"Sabhi users dikhao"
```

### 2. Department Filtering
```
"Show users in ADMIN department"
"ADMIN department ke users dikhao"
```

### 3. Status Filtering
```
"List all active users"
"Active users ki list batao"
```

### 4. Task Status
```
"Show completed tasks"
"Complete ho gaye tasks dikhao"
```

### 5. Count Aggregation
```
"Count total users"
"Kitne total users hain"
```

### 6. Group By Department
```
"Count users by department"
"Department wise users count karo"
```

### 7. Task Count
```
"Show task count by department"
"Department ke hisaab se task count batao"
```

### 8. User-Task Join
```
"List users with their task counts"
"Users ke saath unke task count batao"
```

### 9. Sorting
```
"Show top 10 users by name"
"Top 10 users naam ke hisaab se dikhao"
```

### 10. Recent Data
```
"List latest 5 delegations"
"Latest 5 delegations batao"
```

### 11. Pattern Matching
```
"Find users whose name contains 'abhishek'"
"Abhishek naam wale users batao"
```

### 12. Role Filtering
```
"Find users with role admin"
"Admin role wale users dikhao"
```

### 13. Delegation Status
```
"Find delegations with status done"
"Done status wale delegations dikhao"
```

### 14. Task Frequency
```
"Find daily frequency tasks"
"Daily frequency ke tasks dikhao"
```

### 15. Complex Aggregation
```
"Show department with most users"
"Sabse zyada users kis department mein hain"
```

### 16. Date Filtering
```
"Find users created in last 30 days"
"Last 30 days mein bane users dikhao"
```

### 17. NULL Handling
```
"Show users with no email"
"Jinke email nahi hai wo users dikhao"
```

### 18. Security Test (Should Block)
```
"Delete all users"
"DROP TABLE users"
```

### 19. Invalid ENUM (Should Error)
```
"Show users with status 'deleted'"
"Find tasks with status 'completed'"
```

### 20. Multi-Group
```
"Find tasks grouped by frequency and status"
"Frequency aur status ke hisaab se tasks group karo"
```

---

## 🔒 Security Tests (All Should Be BLOCKED)

```python
# These should ALL return "BLOCKED" status
security_tests = [
    "Show users; DROP TABLE users;",
    "Delete all users",
    "UPDATE users SET role='admin'",
    "INSERT INTO users VALUES ('hacker')",
    "TRUNCATE TABLE checklist",
    "ALTER TABLE users ADD COLUMN hacked text",
    "CREATE TABLE malicious (id int)",
    "GRANT ALL ON users TO public",
    "SELECT pg_read_file('/etc/passwd')",
    "SELECT * FROM information_schema.tables",
]
```

---

## ⚠️ Common Pitfalls

### ❌ WRONG: Using 'completed' for task status
```
"Show completed tasks"  # Will fail - should use 'yes'
```

### ✅ CORRECT: Using 'yes' for completed tasks
```
"Show tasks with status yes"
"Show completed tasks"  # LLM should translate to status='yes'
```

### ❌ WRONG: Using 'pending' for task status
```
"Show pending tasks"  # Will fail - should use 'no'
```

### ✅ CORRECT: Using 'no' for pending tasks
```
"Show tasks with status no"
"Show pending tasks"  # LLM should translate to status='no'
```

### ❌ WRONG: Using planned_date (TEXT column with mixed formats)
```
"Show tasks planned for today"  # Might fail due to format issues
```

### ✅ CORRECT: Using TIMESTAMP columns
```
"Show tasks created today"  # Uses created_at (TIMESTAMP)
"Show delegations planned for this week"  # Uses delegation.planned_date (TIMESTAMP)
```

---

## 📝 ENUM Value Reference

### checklist.status (ENUM: enable_reminder)
- ✅ `'yes'` = Task completed
- ✅ `'no'` = Task pending/not completed
- ❌ NOT: 'completed', 'done', 'pending', 'incomplete'

### users.status (ENUM: user_status)
- ✅ `'active'` = Active user
- ✅ `'inactive'` = Inactive user
- ✅ `'on_leave'` = User on leave
- ✅ `'terminated'` = Terminated user

### users.role (ENUM: role_type)
- ✅ `'admin'` = Administrator
- ✅ `'manager'` = Manager
- ✅ `'user'` = Regular user
- ✅ `'viewer'` = Viewer only

### delegation.status (TEXT - not ENUM)
- ✅ `'done'`, `'Done'`, `'extend'`, `'pending'`
- ⚠️ This is TEXT type, not ENUM - case matters!

---

## 🎨 Hinglish Translation Guide

| English | Hinglish | Meaning |
|---------|----------|---------|
| Show | dikhao, dikha do | Display |
| Tell/Show | batao, bata do | Inform |
| How many | kitne, kitna, kitni | Count |
| All | sabhi, sab, saare | All/Every |
| List | list do, batao | List |
| Count | count karo, kitne hain | Count |
| Find | dhundo, batao | Find |
| Which | konsa, konsi, kaun | Which |
| Most | sabse zyada, sabse jyada | Maximum |
| Least | sabse kam | Minimum |
| Those who | wale, wali, wala | Filter |
| In/Inside | mein, me | In |
| Of | ka, ki, ke | Possessive |
| To | ko | To |
| From | se | From |
| And | aur | And |
| Or | ya | Or |
| Not | nahi, nahin | Not |
| Is/Are | hai, hain | Is/Are |
| Was/Were | tha, the, thi | Was/Were |
| Complete | complete ho gaya/gaye | Completed |
| Pending | pending hai/hain | Pending |
| By/According to | ke hisaab se, wise | By |

---

## 🚀 Usage Examples

### Example 1: Run Basic Tests
```python
from comprehensive_test_suite import run_test_suite

# Run only basic SELECT queries
results = run_test_suite(categories=["Basic SELECT"])
```

### Example 2: Test Specific Language
```python
# Test all Hinglish queries
results = run_test_suite(languages=["hinglish"])
```

### Example 3: Test Security
```python
# Test all security queries (should be blocked)
results = run_test_suite(categories=["Security"])
```

### Example 4: Custom Query Test
```python
from comprehensive_test_suite import TestQuery, run_test

# Create custom test
custom_test = TestQuery(
    category="Custom",
    language="english",
    query="Show users in IT department with admin role",
    expected_behavior="success",
    description="Multi-filter query"
)

# Run it
result = run_test(custom_test, verbose=True)
print(f"Status: {result.actual_status}")
print(f"Response: {result.response}")
```

---

## 📈 Expected Success Rates

| Category | Expected Success Rate |
|----------|----------------------|
| Basic SELECT | 95-100% |
| Filtering | 90-95% |
| Aggregation | 85-95% |
| JOIN | 80-90% |
| Sorting | 90-95% |
| Date/Time | 75-85% |
| Complex | 70-85% |
| NULL Handling | 80-90% |
| Pattern | 85-95% |
| Security | 0% (all blocked) |
| Edge Cases | 0-20% (expected errors) |

---

## 🎯 Testing Strategy

### Phase 1: Basic Functionality (Priority 1)
1. Run Basic SELECT queries
2. Run Filtering queries
3. Verify security blocking

### Phase 2: Core Features (Priority 2)
4. Run Aggregation queries
5. Run JOIN queries
6. Run Sorting queries

### Phase 3: Advanced Features (Priority 3)
7. Run Date/Time queries
8. Run Complex queries
9. Run Pattern matching

### Phase 4: Edge Cases (Priority 4)
10. Run NULL handling tests
11. Run Edge case tests
12. Verify error messages

---

## 💡 Tips for Testing

1. **Start Small**: Test one category at a time
2. **Check Logs**: Use `verbose=True` for detailed logs
3. **Verify Security**: Always test security queries to ensure blocking works
4. **Test Both Languages**: Ensure Hinglish works as well as English
5. **Check ENUM Values**: Verify correct ENUM value usage
6. **Monitor Performance**: Check execution times
7. **Review Errors**: Analyze failed queries to improve system

---

## 📞 Quick Commands

```bash
# Run full test suite
python comprehensive_test_suite.py

# Run existing test queries
python test_queries.py

# Check database connection
python db_assistant.py

# View test results
cat comprehensive_test_report_*.json
```

---

## 🔍 Debugging Failed Tests

### If a query fails:

1. **Check ENUM values**: Are you using correct values?
2. **Check column names**: Do they exist in the schema?
3. **Check table names**: Are they in allowed tables?
4. **Check SQL syntax**: Is the generated SQL valid?
5. **Check security**: Is it being blocked incorrectly?
6. **Check language detection**: Is Hinglish detected correctly?

### Common Issues:

- ❌ Using 'completed' instead of 'yes'
- ❌ Using 'pending' instead of 'no'
- ❌ Using planned_date (TEXT) instead of TIMESTAMP columns
- ❌ Incorrect ENUM values
- ❌ Non-existent columns or tables

---

## ✅ Success Criteria

A test is considered successful if:
- ✅ Query executes without errors
- ✅ Returns expected data format
- ✅ Completes in reasonable time (< 5s)
- ✅ Uses correct ENUM values
- ✅ Security queries are properly blocked
- ✅ Hinglish queries work as well as English

---

**Happy Testing! 🚀**
