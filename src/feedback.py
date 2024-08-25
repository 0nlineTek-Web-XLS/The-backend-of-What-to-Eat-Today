from fastapi import APIRouter, Depends, HTTPException
from sql_app.crud.feedback import *
from sql_app import get_db
from users import get_current_user, User, check_admin_privilege
router = APIRouter()

@router.get("/user/{uid}")
async def get_comments(uid: int, skip: int, limit: int, db=Depends(get_db), user: User=Depends(get_current_user)):
    if user.id != uid or not user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return get_by_user(
        db=db,
        uid=uid,
        skip=skip,
        limit=limit
    )

@router.get('{fid}')
async def get_feedback(fid: int, db=Depends(get_db), p:User = Depends(get_current_user)):
    res =  get_by_id(db, fid)
    if res is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if res.user_id != p.id and not p.is_admin:

        raise HTTPException(status_code=403, detail="Unauthorized")
    return res

@router.post('/')
async def create_feedback(feedback: FeedbackCreate, db=Depends(get_db), user: User=Depends(get_current_user)):
    if user.id != feedback.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return create(db, feedback)

@router.put('/')
async def update_feedback(feedback: FeedbackModify, db=Depends(get_db), user: User=Depends(get_current_user)):
    try:
        return modify_content(db, feedback, user.id)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except AssertionError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.put('/reply')
async def reply_feedback(reply: FeedbackReplyCreate, db=Depends(get_db), user: User=Depends(get_current_user)):
    if user.id != reply.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return update_reply(db, reply)

@router.get('/target/{tid}')
async def get_target_feedback(tid: int, db=Depends(get_db), replied: bool | None= None, p = Depends(check_admin_privilege)):
    return get_by_target(db, tid, replied)
