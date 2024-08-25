from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, not_
from ..models import Feedback
from ..schemas import FeedbackCreate, FeedbackReplyCreate, FeedbackModify

def create(db: Session, feedback: FeedbackCreate):
    db_feedback = Feedback(
        user_id = feedback.user_id,
        content = feedback.content,
        time = feedback.time,
        towards = feedback.towards,
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def update_reply(db: Session, reply: FeedbackReplyCreate):
    db_feedback = db.query(Feedback).filter(Feedback.id == reply.to).first()
    assert db_feedback, 'No such feedback'
    db_feedback.reply = reply.content
    db_feedback.reply_time = reply.time
    db_feedback.reply_uid = reply.user_id
    db.refresh(db_feedback)
    db.commit()
    return db_feedback

def modify_content(db: Session, content: FeedbackModify, uid: int):
    db_feedback: Feedback | None = db.query(Feedback).filter(Feedback.id == content.id).first()
    assert db_feedback, 'No such feedback'
    if db_feedback.user_id != uid:
        raise ValueError('Unauthorized')
    db_feedback.content = content.content
    db_feedback.time = content.time
    db_feedback.towards = content.towards
    return db_feedback

def get_by_id(db: Session, fb_id: int):
    return db.query(Feedback).filter(Feedback.id == fb_id).first()

def get_by_user(db: Session, uid: int, skip: int = 0, limit: int = 100):
    return db.query(Feedback).filter(Feedback.user_id == uid).offset(skip).limit(limit=limit).all()

def get_by_target(db: Session, tid: int, filter_replied: bool|None = None):
    r =  db.query(Feedback).filter(Feedback.towards == tid)
    if filter_replied is None:
        return r.all()
    
    if filter_replied:
        return r.filter(not_(Feedback.content == None)).all()
    
    return r.filter(Feedback.content == None).all()
