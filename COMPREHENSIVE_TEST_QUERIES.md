# 🧪 Comprehensive Test Queries for DB Assistant System

## 📋 Table of Contents
1. [System Overview](#system-overview)
2. [Database Schema](#database-schema)
3. [Query Categories](#query-categories)
4. [Test Queries by Category](#test-queries-by-category)
5. [Security Test Queries](#security-test-queries)
6. [Edge Cases & Error Scenarios](#edge-cases--error-scenarios)
7. [Performance Test Queries](#performance-test-queries)

---

## 🔍 System Overview

**DB Assistant** is a **READ-ONLY** database chatbot with the following characteristics:

### Core Features:
- ✅ **Bilingual Support**: English & Hinglish
- ✅ **LangGraph-based**: Multi-node processing pipeline
- ✅ **Security-First**: Hardcoded security validation (40+ blocked keywords)
- ✅ **PostgreSQL Backend**: AWS RDS database
- ✅ **OpenAI Integration**: GPT-4o-mini for NL to SQL conversion

### Available Tables:
1. **`public.users`** - User management
2. **`public.checklist`** - Task/checklist management
3. **`public.delegation`** - Task delegation tracking

### Security Constraints:
- ❌ **BLOCKED**: DELETE, UPDATE, INSERT, DROP, TRUNCATE, ALTER, CREATE, GRANT, REVOKE
- ✅ **ALLOWED**: SELECT queries only
- 🔒 **Max Query Length**: 2000 characters
- 📊 **Max Results**: 200 rows (auto-LIMIT)

---

## 📊 Database Schema

### Table: `public.users`
```
Columns:
  - user_id (integer) - Primary Key
  - user_name (text)
  - email (text)
  - department (text) - e.g., 'ADMIN', 'IT', 'HR', 'SALES', 'OPERATIONS'
  - role (ENUM: role_type) - Values: 'admin', 'manager', 'user', 'viewer'
  - status (ENUM: user_status) - Values: 'active', 'inactive', 'on_leave', 'terminated'
  - created_at (timestamp)
  - updated_at (timestamp)
```

### Table: `public.checklist`
```
Columns:
  - id (integer) - Primary Key
  - name (text) - Task name
  - department (text)
  - status (ENUM: enable_reminder) - Values: 'yes' (completed), 'no' (pending)
  - enable_reminder (ENUM: enable_reminder) - Values: 'yes', 'no'
  - frequency (text) - e.g., 'daily', 'weekly', 'monthly'
  - planned_date (text) - ⚠️ MIXED FORMATS (avoid using)
  - task_start_date (timestamp)
  - submission_date (timestamp)
  - created_at (timestamp)
  - delay (interval) - Time delay for overdue tasks
```

### Table: `public.delegation`
```
Columns:
  - id (integer) - Primary Key
  - task_name (text)
  - delegated_by (text) - User who delegated
  - delegated_to (text) - User who received delegation
  - status (text) - Values: 'done', 'Done', 'extend', 'pending'
  - planned_date (timestamp)
  - created_at (timestamp)
  - updated_at (timestamp)
```

---

## 🎯 Query Categories

### 1. **Basic SELECT Queries**
   - Simple data retrieval
   - Column selection
   - LIMIT usage

### 2. **Filtering Queries (WHERE)**
   - Equality conditions
   - ENUM value filtering
   - Text pattern matching (LIKE/ILIKE)
   - Date/time filtering
   - NULL checks

### 3. **Aggregation Queries**
   - COUNT, SUM, AVG, MIN, MAX
   - GROUP BY operations
   - HAVING clauses

### 4. **JOIN Queries**
   - INNER JOIN
   - LEFT JOIN
   - Multiple table joins

### 5. **Sorting & Limiting**
   - ORDER BY (ASC/DESC)
   - LIMIT & OFFSET
   - Top N queries

### 6. **Date/Time Queries**
   - Date comparisons
   - Date ranges
   - Recent data queries
   - Interval calculations

### 7. **Complex Analytical Queries**
   - Subqueries
   - CTEs (Common Table Expressions)
   - Window functions
   - CASE statements

### 8. **Hinglish Queries**
   - Mixed Hindi-English queries
   - Natural language variations

### 9. **Security Test Queries**
   - Malicious query attempts
   - SQL injection attempts
   - Bypass attempts

### 10. **Edge Cases**
   - Empty results
   - Invalid ENUM values
   - Type mismatches
   - Invalid column names

---

## 📝 Test Queries by Category

## 1️⃣ Basic SELECT Queries

### English Queries:
```
1. "Show all users"
2. "List all users limit 10"
3. "Display user names and emails"
4. "Get all tasks from checklist"
5. "Show me the first 5 delegations"
6. "List all departments"
7. "Show distinct departments from users table"
8. "Get all user roles"
9. "Display all task names"
10. "Show me all active records"
```

### Hinglish Queries:
```
1. "Sabhi users dikhao"
2. "10 users ki list do"
3. "User names aur emails batao"
4. "Checklist se sabhi tasks dikhao"
5. "Pehle 5 delegations dikha do"
6. "Saare departments batao"
7. "Users table se unique departments dikhao"
8. "Sabhi user roles kya hain"
9. "Task names ki list do"
10. "Active records sabhi dikhao"
```

---

## 2️⃣ Filtering Queries (WHERE Clause)

### English Queries:
```
1. "Show users in ADMIN department"
2. "List all active users"
3. "Find users with role admin"
4. "Show completed tasks" (status = 'yes')
5. "Display pending tasks" (status = 'no')
6. "Find users on leave"
7. "Show inactive users"
8. "List tasks in IT department"
9. "Find delegations with status done"
10. "Show users whose name contains 'abhishek'"
11. "List tasks with reminder enabled"
12. "Find daily frequency tasks"
13. "Show weekly tasks"
14. "Display monthly checklists"
15. "Find users with email containing 'gmail'"
```

### Hinglish Queries:
```
1. "ADMIN department ke users dikhao"
2. "Active users ki list batao"
3. "Admin role wale users dikhao"
4. "Complete ho gaye tasks dikhao" (status = 'yes')
5. "Pending tasks batao" (status = 'no')
6. "Leave pe kon kon hai"
7. "Inactive users dikhao"
8. "IT department ke tasks batao"
9. "Done status wale delegations dikhao"
10. "Abhishek naam wale users batao"
11. "Reminder enabled wale tasks dikhao"
12. "Daily frequency ke tasks dikhao"
13. "Weekly tasks ki list do"
14. "Monthly checklists batao"
15. "Gmail wale users dikhao"
```

---

## 3️⃣ Aggregation Queries

### English Queries:
```
1. "Count total users"
2. "How many tasks are there"
3. "Count users by department"
4. "Show task count by department"
5. "Count delegations by status"
6. "How many active users are there"
7. "Count pending tasks"
8. "Show user count by role"
9. "Count completed tasks"
10. "How many users in each department"
11. "Total tasks per department"
12. "Count tasks with reminders enabled"
13. "How many delegations are done"
14. "Count users by status"
15. "Show department with most users"
16. "Which department has most tasks"
17. "Average tasks per department"
18. "Count daily vs weekly vs monthly tasks"
```

### Hinglish Queries:
```
1. "Kitne total users hain"
2. "Tasks kitne hain"
3. "Department wise users count karo"
4. "Department ke hisaab se task count batao"
5. "Status wise delegations kitne hain"
6. "Active users kitne hain"
7. "Pending tasks count karo"
8. "Role wise kitne users hain"
9. "Complete tasks kitne hain"
10. "Har department mein kitne users hain"
11. "Department wise total tasks batao"
12. "Reminder enabled tasks kitne hain"
13. "Done delegations kitne hain"
14. "Status ke hisaab se users count karo"
15. "Sabse zyada users kis department mein hain"
16. "Sabse zyada tasks kis department ke hain"
17. "Department wise average tasks batao"
18. "Daily, weekly, monthly tasks count karo"
```

---

## 4️⃣ JOIN Queries

### English Queries:
```
1. "List users with their task counts"
2. "Show users and their delegations"
3. "Find users with their department tasks"
4. "List all users and their assigned tasks"
5. "Show delegation details with user information"
6. "Find tasks assigned to each user"
7. "List users who have delegated tasks"
8. "Show users who received delegations"
9. "Find departments with their task counts"
10. "List users with pending tasks"
11. "Show users with completed tasks"
12. "Find users with no tasks"
13. "List departments with active users"
14. "Show users and their task completion rate"
```

### Hinglish Queries:
```
1. "Users ke saath unke task count batao"
2. "Users aur unke delegations dikhao"
3. "Users ko unke department tasks ke saath dikhao"
4. "Sabhi users aur unke assigned tasks batao"
5. "Delegation details user information ke saath dikhao"
6. "Har user ko kitne tasks assigned hain"
7. "Jinke tasks delegate kiye hain wo users dikhao"
8. "Jinko delegations mile hain wo users batao"
9. "Departments aur unke task counts dikhao"
10. "Pending tasks wale users batao"
11. "Completed tasks wale users dikhao"
12. "Jinke koi tasks nahi hain wo users dikhao"
13. "Active users wale departments batao"
14. "Users ka task completion rate batao"
```

---

## 5️⃣ Sorting & Limiting Queries

### English Queries:
```
1. "Show top 10 users by name"
2. "List latest 5 delegations"
3. "Show oldest tasks"
4. "Display users sorted by department"
5. "List tasks ordered by creation date"
6. "Show top 5 departments by user count"
7. "Display recent 10 tasks"
8. "List users in alphabetical order"
9. "Show delegations sorted by planned date"
10. "Find first 3 completed tasks"
11. "List last 5 created users"
12. "Show tasks sorted by department and name"
```

### Hinglish Queries:
```
1. "Top 10 users naam ke hisaab se dikhao"
2. "Latest 5 delegations batao"
3. "Sabse purane tasks dikhao"
4. "Users ko department wise sort karke dikhao"
5. "Tasks ko creation date se sort karo"
6. "Top 5 departments user count ke hisaab se batao"
7. "Recent 10 tasks dikhao"
8. "Users ko alphabetical order mein dikhao"
9. "Delegations ko planned date se sort karo"
10. "Pehle 3 complete tasks batao"
11. "Last 5 created users dikhao"
12. "Tasks ko department aur name se sort karo"
```

---

## 6️⃣ Date/Time Queries

### English Queries:
```
1. "Show tasks created today"
2. "List delegations from last week"
3. "Find users created in last 30 days"
4. "Show tasks created this month"
5. "List recent 5 delegations by created date"
6. "Find tasks with submission date in 2024"
7. "Show delegations planned for this week"
8. "List tasks created before 2024"
9. "Find users created after January 1, 2024"
10. "Show tasks with delay greater than 1 day"
11. "List overdue tasks"
12. "Find tasks created between two dates"
```

### Hinglish Queries:
```
1. "Aaj ke tasks dikhao"
2. "Last week ke delegations batao"
3. "Last 30 days mein bane users dikhao"
4. "Is mahine ke tasks batao"
5. "Created date ke hisaab se recent 5 delegations dikhao"
6. "2024 mein submit hue tasks batao"
7. "Is hafte planned delegations dikhao"
8. "2024 se pehle bane tasks dikhao"
9. "1 January 2024 ke baad bane users batao"
10. "1 din se zyada delay wale tasks dikhao"
11. "Overdue tasks batao"
12. "Do dates ke beech ke tasks dikhao"
```

---

## 7️⃣ Complex Analytical Queries

### English Queries:
```
1. "Show departments with more than 10 users"
2. "Find users who have both completed and pending tasks"
3. "List departments with highest task completion rate"
4. "Show users with most delegations"
5. "Find tasks that are overdue by more than 3 days"
6. "List departments with no active users"
7. "Show users who delegated but never received delegations"
8. "Find tasks with no assigned users"
9. "List top 3 departments by task count"
10. "Show users with tasks in multiple departments"
11. "Find delegation chains (who delegated to whom)"
12. "List tasks grouped by frequency and status"
13. "Show user activity summary by department"
14. "Find tasks with longest delays"
15. "List users with their task distribution"
```

### Hinglish Queries:
```
1. "10 se zyada users wale departments dikhao"
2. "Jinke completed aur pending dono tasks hain wo users batao"
3. "Sabse zyada completion rate wale departments dikhao"
4. "Sabse zyada delegations wale users batao"
5. "3 din se zyada overdue tasks dikhao"
6. "Jinmein koi active user nahi hai wo departments batao"
7. "Jinke delegate kiya par kabhi mila nahi wo users dikhao"
8. "Jinke koi user assign nahi hai wo tasks batao"
9. "Task count ke hisaab se top 3 departments batao"
10. "Multiple departments mein tasks wale users dikhao"
11. "Delegation chain batao (kisne kisko delegate kiya)"
12. "Frequency aur status ke hisaab se tasks group karo"
13. "Department wise user activity summary dikhao"
14. "Sabse zyada delay wale tasks batao"
15. "Users ka task distribution dikhao"
```

---

## 8️⃣ NULL & Special Value Queries

### English Queries:
```
1. "Show users with no email"
2. "Find tasks with no submission date"
3. "List delegations with null planned date"
4. "Show users with email set"
5. "Find tasks with delay"
6. "List users with no department"
7. "Show tasks with empty names"
8. "Find delegations with no status"
```

### Hinglish Queries:
```
1. "Jinke email nahi hai wo users dikhao"
2. "Jinke submission date nahi hai wo tasks batao"
3. "Null planned date wale delegations dikhao"
4. "Email set hai jinke wo users batao"
5. "Delay wale tasks dikhao"
6. "Jinke department nahi hai wo users batao"
7. "Empty name wale tasks dikhao"
8. "Jinke status nahi hai wo delegations batao"
```

---

## 9️⃣ Pattern Matching Queries

### English Queries:
```
1. "Find users whose name starts with 'A'"
2. "Show tasks containing 'report' in name"
3. "List users with gmail addresses"
4. "Find tasks ending with 'review'"
5. "Show users with names containing 'kumar'"
6. "List delegations with 'urgent' in task name"
7. "Find users with department starting with 'IT'"
```

### Hinglish Queries:
```
1. "A se shuru hone wale users dikhao"
2. "Name mein 'report' wale tasks batao"
3. "Gmail address wale users dikhao"
4. "'review' se khatam hone wale tasks batao"
5. "Name mein 'kumar' wale users dikhao"
6. "Task name mein 'urgent' wale delegations batao"
7. "'IT' se shuru hone wale department ke users dikhao"
```

---

## 🔒 Security Test Queries (Should be BLOCKED)

### SQL Injection Attempts:
```
1. "Show users; DROP TABLE users;"
2. "List users WHERE 1=1 OR 1=1"
3. "Show users' OR '1'='1"
4. "Delete all users"
5. "UPDATE users SET role='admin'"
6. "INSERT INTO users VALUES ('hacker')"
7. "TRUNCATE TABLE checklist"
8. "ALTER TABLE users ADD COLUMN hacked text"
9. "CREATE TABLE malicious (id int)"
10. "GRANT ALL ON users TO public"
11. "REVOKE SELECT ON users FROM public"
12. "EXECUTE sp_executesql"
13. "CALL malicious_function()"
14. "SELECT * FROM users; SELECT * FROM pg_shadow"
15. "SELECT * FROM users UNION SELECT * FROM delegation"
```

### Bypass Attempts:
```
1. "Show users -- comment out security"
2. "List users /* bypass */ WHERE 1=1"
3. "SELECT * FROM users INTO OUTFILE '/tmp/hack.txt'"
4. "SELECT pg_read_file('/etc/passwd')"
5. "SELECT * FROM information_schema.tables"
6. "SELECT * FROM pg_catalog.pg_tables"
7. "COPY users TO '/tmp/data.csv'"
8. "SELECT pg_sleep(10)"
9. "SELECT * FROM users WHERE user_name = 'admin' AND pg_sleep(5)"
10. "SELECT BENCHMARK(1000000, MD5('test'))"
```

### Expected Behavior:
- ❌ All above queries should be **BLOCKED**
- 🚫 Error message: "Only SELECT queries allowed" or "Dangerous keyword detected"
- 🔒 Security validator should catch these before execution

---

## ⚠️ Edge Cases & Error Scenarios

### Invalid ENUM Values:
```
1. "Show users with status 'deleted'" (invalid status)
2. "Find tasks with status 'completed'" (should be 'yes')
3. "List tasks with status 'pending'" (should be 'no')
4. "Show users with role 'superadmin'" (invalid role)
5. "Find delegations with status 'cancelled'" (might be invalid)
```

### Invalid Column Names:
```
1. "Show user passwords" (column doesn't exist)
2. "List task priorities" (column doesn't exist)
3. "Find user salaries" (column doesn't exist)
4. "Show delegation deadlines" (column doesn't exist)
```

### Invalid Table Names:
```
1. "Show all employees" (table doesn't exist)
2. "List from tasks table" (wrong table name)
3. "Find records in projects" (table doesn't exist)
```

### Type Mismatches:
```
1. "Show users where user_id = 'abc'" (type mismatch)
2. "Find tasks where created_at = 'invalid-date'"
3. "List users where department = 123" (type mismatch)
```

### Empty Result Scenarios:
```
1. "Show users with status 'terminated'"
2. "Find tasks in MARKETING department" (if no such department)
3. "List delegations from 1990"
4. "Show users with email 'nonexistent@test.com'"
```

### Expected Behavior:
- 📭 "No data found" message
- ❌ Clear error messages for invalid queries
- 🔍 Helpful suggestions for corrections

---

## 🚀 Performance Test Queries

### Large Result Sets:
```
1. "Show all users without limit"
2. "List all tasks"
3. "Display all delegations"
4. "Show complete user and task data"
```

### Complex Joins:
```
1. "Show users with their tasks and delegations"
2. "List all relationships between users, tasks, and delegations"
3. "Find complete activity log for each user"
```

### Heavy Aggregations:
```
1. "Calculate comprehensive statistics for all departments"
2. "Show detailed task analysis by user, department, and status"
3. "Generate complete delegation report with all metrics"
```

### Expected Behavior:
- 📊 Auto-LIMIT to 200 rows
- ⏱️ Reasonable response time (< 5 seconds)
- 💾 Efficient query execution

---

## 📈 Summary Statistics

### Total Test Categories: 10
1. Basic SELECT: 20 queries (10 English + 10 Hinglish)
2. Filtering: 30 queries (15 English + 15 Hinglish)
3. Aggregation: 36 queries (18 English + 18 Hinglish)
4. JOIN: 28 queries (14 English + 14 Hinglish)
5. Sorting: 24 queries (12 English + 12 Hinglish)
6. Date/Time: 24 queries (12 English + 12 Hinglish)
7. Complex: 30 queries (15 English + 15 Hinglish)
8. NULL: 16 queries (8 English + 8 Hinglish)
9. Pattern: 14 queries (7 English + 7 Hinglish)
10. Security: 25 queries (should be blocked)

### **Total Valid Queries: ~222**
### **Total Security Tests: ~25**
### **Total Edge Cases: ~20**
### **GRAND TOTAL: ~267 Test Queries**

---

## 🎯 Testing Recommendations

### Priority 1 (Must Test):
- ✅ Basic SELECT queries (both languages)
- ✅ Filtering with ENUM values
- ✅ Aggregation queries
- ✅ Security blocking (all malicious queries)

### Priority 2 (Should Test):
- ✅ JOIN queries
- ✅ Date/time filtering
- ✅ Sorting and limiting
- ✅ Edge cases (invalid values)

### Priority 3 (Nice to Test):
- ✅ Complex analytical queries
- ✅ Pattern matching
- ✅ NULL handling
- ✅ Performance tests

---

## 📝 Notes

1. **ENUM Values**: Always use exact values:
   - `checklist.status`: 'yes' (completed), 'no' (pending)
   - `users.status`: 'active', 'inactive', 'on_leave', 'terminated'
   - `users.role`: 'admin', 'manager', 'user', 'viewer'

2. **Date Columns**: Prefer TIMESTAMP columns over TEXT:
   - Use `created_at`, `task_start_date`, `submission_date`
   - Avoid `checklist.planned_date` (mixed formats)

3. **Hinglish Support**: System should understand:
   - "dikhao" = show
   - "batao" = tell/show
   - "kitne" = how many
   - "sabhi" = all
   - "wale" = those who

4. **Security**: System should block ALL modification attempts

---

## 🏁 Conclusion

This comprehensive test suite covers:
- ✅ All SQL query types (SELECT, WHERE, JOIN, GROUP BY, ORDER BY)
- ✅ Both English and Hinglish queries
- ✅ Security validation
- ✅ Edge cases and error scenarios
- ✅ Performance considerations

**Use this document to systematically test the DB Assistant system and ensure robust, secure, and user-friendly operation.**
