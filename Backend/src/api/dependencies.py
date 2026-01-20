from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from ..config.database import get_db
from ..core.security import verify_token

def get_current_user(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

def validate_query(query: str):
    blocked_keywords = ["delete", "update", "truncate", "drop", "insert", "alter", "create", "grant", "revoke"]
    if any(keyword in query.lower() for keyword in blocked_keywords):
        raise HTTPException(status_code=400, detail="Blocked query detected")