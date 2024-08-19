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

def get_comment(db: Session, dish: int):
    return db.query(Comment).filter(Comment.dish_id == dish).all()
