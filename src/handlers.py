from src.models import User
from src.database import get_session_local
from src.schemas import UserResponse, CreateUserMessage, GetUserMessage, UpdateUserMessage
from datetime import datetime, timezone

async def handle_get_user(data: dict):
    msg = GetUserMessage(**data)
    SessionLocal = get_session_local()
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.keycloak_id == msg.keycloak_id).first()
        if not user:
            return {"error": "User not found"}
        
        return UserResponse.model_validate(user).model_dump(mode='json')
    finally:
        db.close()

async def handle_create_user(data: dict):
    msg = CreateUserMessage(**data)
    SessionLocal = get_session_local()
    db = SessionLocal()
    
    try:
        existing = db.query(User).filter(User.keycloak_id == msg.keycloak_id).first()
        if existing:
            return {"error": "User already exists"}
        
        user = User(
            keycloak_id=msg.keycloak_id,
            username=msg.username,
            last_login=datetime.now(timezone.utc)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return UserResponse.model_validate(user).model_dump(mode='json')
    finally:
        db.close()

async def handle_update_user(data: dict):
    msg = UpdateUserMessage(**data)
    SessionLocal = get_session_local()
    db = SessionLocal()
    
    try:
        user = db.query(User).filter(User.keycloak_id == msg.keycloak_id).first()
        if not user:
            return {"error": "User not found"}
        
        if msg.username:
            user.username = msg.username
        user.last_login = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(user)
        
        return UserResponse.model_validate(user).model_dump(mode='json')
    finally:
        db.close()

async def handle_list_users(data: dict):
    SessionLocal = get_session_local()
    db = SessionLocal()
    
    try:
        users = db.query(User).all()
        return {
            "users": [UserResponse.model_validate(u).model_dump(mode='json') for u in users]
        }
    finally:
        db.close()