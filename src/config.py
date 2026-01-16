from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/users_db"
    
    nats_url: str = "nats://localhost:4222"
    
    keycloak_url: str = "http://localhost:8080"
    keycloak_realm: str = "codesnap"
    
    service_name: str = "user-service"
    port: int = 8001
    logfire_token: str | None = None
    logfire_service_name: str | None = None
    
    class Config:
        env_file = ".env"

settings = Settings()