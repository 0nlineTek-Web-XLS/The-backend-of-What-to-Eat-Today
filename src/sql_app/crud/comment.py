from typing import List
from sqlalchemy.orm import Session
from ..models import Comment, Dish
from ..schemas import CommentItem

def post_comment(db: Session, comment: CommentItem) -> Comment:
    # check if the user has already commented on the dish
    if db.query(Comment).filter(Comment.user_id == comment.user_id).filter(Comment.dish_id == comment.dish_id).first():
        raise ValueError("User has already commented on the dish")
    db_comment = Comment(user_id=comment.user_id,
                         dish_id=comment.dish_id,
                        vote=comment.vote,
                        content=comment.content, 
                        time=comment.time)
    db_dish: Dish | None = db.query(Dish).filter(Dish.id == comment.dish_id).first()
    assert db_dish, "No such dish"
    if comment.content:
        db_dish.count_of_comments += 1

    db_dish.average_vote = (db_dish.average_vote * db_dish.count_of_votes + comment.vote) / (db_dish.count_of_votes + 1)
    db_dish.count_of_votes += 1
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db: Session, comment_id: int) -> Comment | None:
    return db.query(Comment).filter(Comment.id == comment_id).first()

def get_comment_by_dish(db: Session, dish: int, skip: int = 0, limit: int = 100, filtered:bool=True) -> List[Comment]:
    return db.query(Comment).filter(Comment.dish_id == dish).filter(Comment.content_visible == filtered).offset(skip).limit(limit).all()

def delete(db: Session, comment_id: int):

    item: Comment | None = db.query(Comment).filter(Comment.id == comment_id).first()
    assert item, "No such comment"
    db_dish: Dish | None = db.query(Dish).filter(Dish.id == item.dish_id).first()
    assert db_dish, "No such dish"
    if item.content:
        db_dish.count_of_comments -= 1
    db_dish.average_vote = (db_dish.average_vote * db_dish.count_of_votes - item.vote) / (db_dish.count_of_votes - 1)
    db_dish.count_of_votes -= 1
    db.delete(item)
    db.commit()
    return True

def update(db: Session, comment_id: int, comment: CommentItem):
    db_comment: Comment | None = db.query(Comment).filter(Comment.id == comment_id).first()
    assert db_comment, "No such comment"
    original_vote = db_comment.vote
    db_comment.vote = comment.vote
    db_dish: Dish | None = db.query(Dish).filter(Dish.id == comment.dish_id).first()
    assert db_dish, "No such dish"
    db_dish.average_vote = (db_dish.average_vote * db_dish.count_of_votes - original_vote + comment.vote) / db_dish.count_of_votes
    db_comment.content = comment.content
    db_comment.dish_id = comment.dish_id
    db.commit()
    db.refresh(comment_id)
    return db_comment
