from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.users import User, UserRole
from app.core.security import hash_password
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def create_default_admin():
    db: Session = SessionLocal()

    admin_email = getenv("ADMIN_EMAIL")
    admin_password = getenv("ADMIN_PASSWORD")
    admin_username = getenv("Admin_Username")

    if not admin_email or not admin_password or not admin_username:
        print("ADMIN_EMAIL, ADMIN_PASSWORD ou Admin_Username non défini")
        return

    existing_admin = db.query(User).filter(User.role == UserRole.ADMIN).first()

    if not existing_admin:
        admin = User(
            username=admin_username,
            email=admin_email,
            password=hash_password(admin_password),
            role=UserRole.ADMIN,
        )
        print(hash_password(admin_password))


        db.add(admin)
        db.commit()

        print("Admin créé automatiquement")

    db.close()
