import requests
import json
import time

BASE_URL = "http://localhost:8000/chat"

# We use a fixed session ID to test context persistence
SESSION_ID = "test_session_validator_001"

TEST_QUERIES = [
    # 1. Basic Count
    "Dinesh ka kitna task pending hai",
    
    # 2. Context Resolution (Iska -> Dinesh) + CTE Date Logic
    "Iska iss month ka performance report do",
    
    # 3. Late Logic (delay column)
    "Amit ke kitne task late hain",
    
    # 4. Delegation
    "Kaun kiska kaam cover kar raha hai",
    
    # 5. Department Filter
    "Accounts department me kitne task hain",
    
    # 6. Specific Status
    "Abhishek ke total completed tasks dikhao",
    
    # 7. Overdue Logic (Pending + Date Passed)
    "Ravi ke overdue tasks batao",
    
    # 8. Date Logic (Today)
    "Aaj ke saare tasks dikhao",
    
    # 9. Date Range
    "January 2026 me kitne task banaye gaye",
    
    # 10. Aggregation
    "Shivraj ka completion percentage kya hai",
    
    # 11. General Late
    "Kaunse task delay huye hain",
    
    # 12. "Wale" logic
    "Pending wale task dikhao",
    
    # 13. User Status
    "Sabhi active users ki list do",
    
    # 14. Complex Aggregation
    "Kiska task sabse zyada pending hai",
    
    # 15. Relationship (Given By)
    "Abhay Lilhare ko kisne task diya",
    
    # 16. Context Switch (Iska -> Abhay)
    "Iska work kaisa chal raha hai",
    
    # 17. Column Filter
    "Daily frequency wale task kitne hain",
    
    # 18. Department Report
    "Security department ka report do",
    
    # 19. Negative Logic
    "Kisne task complete nahi kiya",
    
    # 20. Access Table
    "System access kiske paas hai"
]

def run_tests():
    print(f"🚀 Starting Validation of {len(TEST_QUERIES)} Queries on {BASE_URL}...\n")
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"--------------------------------------------------")
        print(f"📝 Test {i}: '{query}'")
        
        payload = {
            "question": query,
            "session_id": SESSION_ID
        }
        
        try:
            # Note: The main endpoint returns a stream. 
            # For testing, we might want the non-streaming response if available, 
            # but usually /chat implies streaming in this app?
            # Let's check main.py. Usually /chat or /chat/stream.
            # Assuming /chat is the POST endpoint for standard JSON (non-streaming)
            # If valid endpoint is /chat/message then use that.
            # Let's try standard POST to /chat/stream and handle stream, 
            # OR better, use the internal service or just curl payload.
            # Actually, previous logs showed POST /chat/stream.
            
            # Let's try to hit the NON-streaming endpoint if it exists.
            # In chat_service.py 'process_query' exists.
            # Let's look for main.py routes. 
            # I will assume /chat/ask exists or I'll just parse the stream.
            
            # For simplicity, assuming there is a JSON endpoint. 
            # If not, I will do a quick check.
            # Log shows: "POST /chat/stream HTTP/1.1" 200 OK
            
            # I will interpret stream chunks.
            response = requests.post(f"{BASE_URL}/stream", json=payload, stream=True)
            
            generated_sql = "Not Found"
            full_answer = ""
            
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data: "):
                        data_content = decoded_line[6:]
                        try:
                            # Parse JSON
                            # The stream usually sends JSON strings or partial text.
                            # Based on chat_service.py: yield json.dumps(...)
                            json_data = json.loads(data_content)
                            
                            if json_data.get("type") == "sql":
                                generated_sql = json_data.get("sql")
                            
                            if json_data.get("type") == "content":
                                full_answer += json_data.get("content", "")
                                
                        except:
                            pass
            
            print(f"✅ SQL Generated:\n{generated_sql}")
            print(f"🤖 Answer Snippet: {full_answer[:100]}...")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
        time.sleep(1) # Polite delay

if __name__ == "__main__":
    run_tests()
