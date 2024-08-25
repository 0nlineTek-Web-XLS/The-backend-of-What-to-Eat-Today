"""
This file contains the API endpoints for comments. They are used to give rates and comments to dishes.
"""

from fastapi import APIRouter, Depends, HTTPException
from sql_app.crud.comment import *
from sql_app.crud.dishes import get_by_id as check_dish
from sql_app.models import Comment
from users import get_current_user, User
from sql_app import get_db
router = APIRouter()

@router.get("/{comment_id}")
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment: Comment | None = get_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.post("/")
def create_comment(comment: CommentItem, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if comment.user_id != user.id and not user.is_admin:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if not check_dish(db, comment.dish_id):
        raise HTTPException(status_code=404, detail="Dish not found")
    # update the vote of the dish
    
    return post_comment(db, comment)

@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_comment = get_comment(db, comment_id)
    # if db_comment is None:
    #     raise HTTPException(status_code=404, detail="Comment not found")
    if not user.is_admin and user.id != db_comment.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if delete(db=db, comment_id=comment_id):
        return {"message": "Comment deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Comment not found")

@router.put("/{comment_id}")
def update_comment(comment_id: int, comment: CommentItem, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    db_comment = get_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if not user.is_admin and user.id != db_comment.user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return update(db=db, comment_id=comment_id, comment=comment)

@router.get("/dish/{dish_id}")
def read_comment_by_dish(dish_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    return get_comment_by_dish(db, dish_id, skip, limit)

