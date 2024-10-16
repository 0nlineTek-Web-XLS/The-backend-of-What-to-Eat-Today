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
    print("Warning: SECRET_KEY not found in environment variables, using default key")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


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
        raise HTTPException(# pylint: disable=raise-missing-from
            status_code=401, detail="Token has expired"
        )
    except:
        raise HTTPException(# pylint: disable=raise-missing-from
            status_code=401, detail="Could not validate credentials"
        )
    db_user: User | None = user.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def check_admin_privilege(token: str = Depends(oauth2_scheme), db=Depends(get_db), require: str = "ALL"):
    user_data: User = get_current_user(token, db)
    if not user_data.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")
    admin: Admin | None = user.get_admin_by_user_id(db, user_data.id)
    if admin is None:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if require not in admin.privileges.split(","):
        raise HTTPException(status_code=403, detail="Unauthorized")
    return user

def create_token(
    user_id: int, is_admin: bool, time_expire=timedelta(minutes=15)
) -> Token:
    payload = {
        "sub": user_id,
        "is_admin": is_admin,
        "exp": datetime.now() + time_expire,
    }
    payload_refresh = {
        "sub": user_id,
        "exp": datetime.now() + timedelta(days=14),
    }
    return Token(access_token=jwt.encode(payload, SECRET_KEY, algorithm="HS256"), refresh_token=jwt.encode(payload_refresh, SECRET_KEY, algorithm="HS256"))


def authenticate_user(username: str, password: str, db):
    # check if username exists
    user_in_db: User | None = user.get_user_by_sdu_id(db, username)
    if user_in_db is None:
        # This user has never logged in before, so we try to register the user via sdu sso.
        # But another situation is that this user is an admin with no sdu_id.
        # check if admin login system successful.
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
            return create_token(user_in_db.id, user_in_db.is_admin)
        else:
            # This is an admin, so we try to login via admin system.
            # check if password is correct.
            if verify_password(password, admin_in_db.password):
                return create_token(admin_in_db.user_id, True)
            raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        # This user has a record in users table, user_in_db not None
        # use sdu sso to login and return the token
        try:
            sTicket = sdu_sso.login(username, password)
            name, sdu_id = sdu_sso.get_user_name_and_id(sTicket)
        except:
            raise HTTPException(    # pylint: disable=raise-missing-from
                status_code=401, detail="Invalid credentials"
            )
        return create_token(user_in_db.id, user_in_db.is_admin)


@router.get("/me", response_model=UserData)
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@router.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db)
):
    return authenticate_user(form_data.username, form_data.password, db)

@router.post("/token/refresh")
def refresh_token(token: Token):
    try:
        payload = jwt.decode(token.access_token, SECRET_KEY, algorithms=["HS256"])
        user_id: int = payload.get("sub")
        assert user_id is not None
        payload_refresh = jwt.decode(token.refresh_token, SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials"
        )
    if user_id != payload_refresh.get("sub"):
        raise HTTPException(
            status_code=401, detail="Could not validate credentials"
        )
    return create_token(user_id, payload.get("is_admin"))


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
def create_admin_user(form_data: AdminCreate, db=Depends(get_db)) -> Admin:
    # check if user already exists
    if user.get_admin_by_username(db, form_data.access_name) is not None:
        raise HTTPException(status_code=400, detail="User already registered")
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

@router.patch("/me/image")
async def update_user_image(image: str, db=Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        user.update_user_image(db, current_user.id, image)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Image updated successfully"}

@router.put("/{uid}", response_model=UserData)
async def update_user(uid: int, data: UserData, db=Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin or current_user.id != uid or data.id != uid or data.id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        user.update_user(db, uid, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="User not found")
    return user.get_user(db, uid)
