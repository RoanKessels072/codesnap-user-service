from sqlalchemy.orm import Session
from datetime import datetime, timezone
from src.models import User

def get_user_by_keycloak_id(db: Session, keycloak_id: str):
    return db.query(User).filter(User.keycloak_id == keycloak_id).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def sync_user(db: Session, keycloak_id: str, username: str):
    user = get_user_by_keycloak_id(db, keycloak_id)

    if not user:
        user = User(
            keycloak_id=keycloak_id,
            username=username,
            last_login=datetime.now(timezone.utc)
        )
        db.add(user)
    else:
        user.last_login = datetime.now(timezone.utc)
        if username and user.username != username:
            user.username = username

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, keycloak_id: str):
    user = get_user_by_keycloak_id(db, keycloak_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True