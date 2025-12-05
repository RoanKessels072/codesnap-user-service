from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    keycloak_id: str
    username: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    keycloak_id: str
    username: Optional[str]
    created_at: datetime
    last_login: datetime
    
    class Config:
        from_attributes = True

class GetUserMessage(BaseModel):
    keycloak_id: str

class CreateUserMessage(BaseModel):
    keycloak_id: str
    username: Optional[str] = None

class UpdateUserMessage(BaseModel):
    keycloak_id: str
    username: Optional[str] = None