from fastapi import APIRouter, Depends, HTTPException

from sql_app.crud import marks
from sql_app import get_db
from users import get_current_user, User

router = APIRouter()

@router.post('')
def add_mark(mark: marks.MarkCreate, db = Depends(get_db), user: User = Depends(get_current_user)):
    if user.id != mark.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return marks.add(db, mark)

@router.get('/user/{uid}')
def get_marks_by_user(uid: int, db = Depends(get_db), user: User = Depends(get_current_user)):
    if user.id != uid:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return marks.get_by_user(db, uid)

@router.get('/dish/{did}/marked_by')
def get_marks_by_dish(did: int, db = Depends(get_db)):
    return marks.get_by_dish(db, did)

@router.get('/{mid}')
def get_mark(mid: int, db = Depends(get_db), user: User = Depends(get_current_user)):
    res = marks.get_by_id(db, mid)
    if res is None:
        raise HTTPException(status_code=404, detail="Mark not found")
    if res.user_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return res

@router.delete('/{mid}')
def delete_mark(mid: int, db = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        res = marks.delete(db, mid, user.id)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    if res is None:
        raise HTTPException(status_code=404, detail="Mark not found")
    return res
