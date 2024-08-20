from ..models import User, Admin
from sqlalchemy.orm import Session

def get_user(db: Session, id: int) -> User | None:
    return db.query(User).filter(User.id == id).first()

def get_user_by_sdu_id(db: Session, sdu_id: str) -> User | None:
    return db.query(User).filter(User.sdu_id == sdu_id).first()

def get_admin(db: Session, id: int) -> Admin | None:
    return db.query(Admin).filter(Admin.id == id).first()

def get_admin_by_username(db: Session, access_name:str) -> Admin | None:
    return db.query(Admin).filter(Admin.access_name == access_name).first()

def create_admin(db: Session, username: str, user_id: int, password: str) -> Admin:
    db_user = Admin(access_name=username, user_id=user_id, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_admin_by_user_id(db: Session, user_id: int) -> Admin | None:
    return db.query(Admin).filter(Admin.user_id == user_id).first()

def register_user(db: Session, username: str, sdu_id: str | None, is_admin: bool = False) -> User:
    db_user = User(username=username, sdu_id=sdu_id, is_admin=is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user