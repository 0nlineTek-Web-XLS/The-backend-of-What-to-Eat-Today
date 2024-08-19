from sqlalchemy.orm import Session

from ..models import Comment
from ..schemas import CommentItem

def post_comment(db: Session, comment: CommentItem):
    db_comment = Comment(user_id=comment.user_id,
                         dish_id=comment.dish_id,
                        vote=comment.vote,
                        content=comment.content, 
                        time=comment.time)
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def get_comment_by_dish(db: Session, dish: int):
    return db.query(Comment).filter(Comment.dish_id == dish).all()

def delete_comment(db: Session, comment_id: int):
    db.query(Comment).filter(Comment.id == comment_id).delete()
    db.commit()
    return True

def update_comment(db: Session, comment_id: int, comment: CommentItem):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise Exception('No such comment')
    db_comment.content = comment.content
    db_comment.dish_id = comment.dish_id
    db.commit()
    db.refresh(comment_id)
    return db_comment