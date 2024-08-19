from fastapi import APIRouter, Depends, HTTPException

from sql_app.models import User, 
from sql_app.crud import user
from passlib.context import CryptContext
import jwt

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    return pwd_context.hash(password)

def get_user(db, id: int) -> User | None:
    return user.get_user(db, id)


@router.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user