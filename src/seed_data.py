from src.database import SessionLocal, engine, Base
from src.models import User

def seed_users():
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:        
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("Admin user already exists. Skipping.")
            return
        
        admin = User(
            keycloak_id="admin-default-id",
            username="admin",
        )
        
        db.add(admin)
        db.commit()
        print("Admin user created successfully!")
        print(f"  Username: {admin.username}")
        print(f"  Keycloak ID: {admin.keycloak_id}")
        
    except Exception as e:
        print(f"Error seeding users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    seed_users()