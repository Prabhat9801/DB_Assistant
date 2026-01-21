# 🛠️ DB Assistant Improvement Plan

Based on the analysis of recent chat logs, here are the recommended improvements:

## 1. Context Awareness for Follow-up Queries
- **Problem**: When user asked *"Total count karke batao"* after viewing Hem Kumar Jagat's tasks, the bot returned the total count of **Users** (604) instead of the tasks discussed.
- **Fix**: Implement context memory to understand what "total" refers to based on the previous turn. If the last query was about tasks, "total" should refer to tasks.

## 2. "Current Month" Logic Standardization
- **Problem**: Inconsistent counts for "current month" queries (72,294 vs 72,318) within seconds.
- **Fix**: Ensure the LLM generates consistent SQL for "current month".
  - *Preferred*: `WHERE date_col >= DATE_TRUNC('month', CURRENT_DATE)`
  - *Avoid*: Varied interpretations like `last 30 days` vs `calendar month`.

## 3. Ambiguous Typo Handling
- **Problem**: User asked *"hwo may complete"* (likely meaning "how many complete").
- **Outcome**: Bot interpreted it as *"how MAY [he] complete"* and gave generic productivity advice.
- **Fix**: Add a clarification step or strict strict SQL-only focus. Use LLM to rephrase ambiguous queries before SQL generation.

## 4. Response Language Alignment
- **Problem**: User used broken English (*"iw ant current month"*), but Bot replied in Hinglish.
- **Fix**: Improve language detection confidence. If the query is >50% English words (even typos), stick to English.

## 5. SQL Logic Logic for "Pending"
- **Problem**: Different queries for "pending" might be checking different columns (`status='no'` vs `status IS NULL` vs `completed_at IS NULL`).
- **Fix**: Hardcode the definition of "Pending" in the system prompt:
  - `Pending` = `status != 'yes'` (or specifically `status = 'no'`).

## 6. Logic Safety for OR Conditions
- **Status**: ✅ **Fixed** (Added "Logic Safety Cage" to prompt).
- **Verification**: Verify that `OR` conditions are continuously wrapped in parentheses.

---
**Next Actions:**
- [ ] Refine "current month" prompt instructions.
- [ ] Add previous-turn context to `analyze_intent`.
