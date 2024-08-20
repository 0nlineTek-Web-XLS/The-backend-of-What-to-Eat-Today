from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sql_app.models import User, Admin
from sql_app import get_db
from sql_app.schemas import UserData, AdminCreate, AdminData
from sql_app.crud import user
from passlib.context import CryptContext
import jwt
import sdu_sso
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
import os
from pydantic import BaseModel

router = APIRouter()

# read secret_key from env vars
SECRET_KEY = os.getenv("SECRET_KEY")
if SECRET_KEY is None:
    SECRET_KEY = "test"  # fallback to development key
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        assert user_id is not None
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token has expired"
        )  # pylint: disable=raise-missing-from
    except:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials"
        )  # pylint: disable=raise-missing-from
    db_user: User | None = user.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def check_admin_privilege(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    user: User = get_current_user(token, db)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")


def create_token(
    user_id: int, is_admin: bool, time_expire=timedelta(minutes=15)
) -> Token:
    payload = {
        "sub": user_id,
        "is_admin": is_admin,
        "exp": datetime.now() + time_expire,
    }
    return Token(access_token=jwt.encode(payload, SECRET_KEY, algorithm="HS256"))


def authenticate_user(username: str, password: str, db):
    # check if username exists
    user_in_db: User | None = user.get_user_by_sdu_id(db, username)
    if user_in_db is None:
        # check if admin login system successful
        admin_in_db: Admin | None = user.get_admin_by_username(db, username)
        if admin_in_db is None:
            # This is not an admin, so we try to register the user via sdu sso
            try:
                name, sdu_id = sdu_sso.get_user_name_and_id(
                    sdu_sso.login(username, password)
                )
            except:
                raise HTTPException(  # pylint: disable=raise-missing-from
                    status_code=401, detail="Invalid credentials"
                )  
            user_in_db = user.register_user(db, name, sdu_id)
        else:
            # check if password is correct
            if verify_password(password, admin_in_db.password):
                return create_token(admin_in_db.user_id, True)

            raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        # use sdu sso to login and return the token
        try:
            sTicket = sdu_sso.login(username, password)
            name, sdu_id = sdu_sso.get_user_name_and_id(sTicket)
        except:
            raise HTTPException(    # pylint: disable=raise-missing-from
                status_code=401, detail="Invalid credentials"
            )  
        return create_token(user_in_db.id, False)


@router.get("/me", response_model=UserData)
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)
):
    return authenticate_user(form_data.username, form_data.password, db)


@router.get("/users/{user_id}", response_model=UserData)
def read_user(
    user_id: int, db=Depends(get_db), current_user: User = Depends(get_current_user)
) -> User:

    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=401, detail="Unauthorized")
    db_user = user.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/admin/register", response_model=AdminData)
def create_admin_user(form_data: AdminCreate = Depends(), db=Depends(get_db)) -> Admin:
    new_user: User = user.register_user(
        db, username=form_data.access_name, sdu_id=None, is_admin=True
    )
    new_admin = user.create_admin(
        db, form_data.access_name, new_user.id, get_password_hash(form_data.password)
    )
    return new_admin


@router.get("/admin/me", response_model=AdminData)
def read_admin_me(
    current_user: User = Depends(get_current_user),
    privileged=Depends(check_admin_privilege),
    db=Depends(get_db),
) -> Admin:
    ret = user.get_admin_by_user_id(db=db, user_id=current_user.id)
    if ret is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return ret
