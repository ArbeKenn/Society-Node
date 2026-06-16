from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import jwt

SECRET_KEY = os.getenv('SECRET_KEY','')
security = HTTPBearer()

def create_token(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token =credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истёк")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Неверный токен")