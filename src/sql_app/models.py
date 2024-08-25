from sqlalchemy import Boolean, ForeignKey, Integer, String, Numeric,Text, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import DeclarativeBase
import datetime


class Base(DeclarativeBase):
    pass

class User(Base):
    """
    This class is to be used for user management

    Attributes:
    id: The id of the user
    username: The username of the user
    sdu_id: The sdu_id of the user
    is_admin: The boolean value of whether the user is an admin
    """
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    username:Mapped[str] = mapped_column(String(20), index=True)
    sdu_id:Mapped[str | None] = mapped_column(String(20), index=True, unique=True, nullable=True)
    is_admin:Mapped[bool] = mapped_column(Boolean, default=False)
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")

class Admin(Base):
    """
    This class is to be used for registering admins
    """
    __tablename__ = "admins"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True, nullable=False, unique=True)
    access_name:Mapped[str] = mapped_column(String(20), index=True, unique=True, nullable=False)
    password:Mapped[str] = mapped_column(String(64), index=True)


class Comment(Base):   # This class is to be used in the future
    __tablename__ = "comments"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    dish_id:Mapped[int] = mapped_column(Integer, ForeignKey("dishes.id"), index=True)
    content:Mapped[str] = mapped_column(Text, nullable=True)  # The content of the comment, can be empty with only a vote
    vote:Mapped[float] = mapped_column(Numeric)  
    content_visible:Mapped[bool] = mapped_column(Boolean, default=False)
    time:Mapped[datetime.datetime] = mapped_column(DateTime, index=True)
    reply_to:Mapped[int | None] = mapped_column(Integer, ForeignKey("comments.id"), nullable=True, index=True, default=None)
    user:Mapped['User'] = relationship("User")
    dish:Mapped['Dish'] = relationship("Dish")
    reply:Mapped[list["Comment"]] = relationship("Comment", back_populates="reply_to")



class Canteen(Base):  
    __tablename__ = "canteens"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(8), index=True, nullable=False, unique=True)
    description:Mapped[str] = mapped_column(Text, index=True)
    image:Mapped[str|None] = mapped_column(Text, nullable = True)
    campus:Mapped[str] = mapped_column(String(8), index=True, nullable=False)
    icon:Mapped[str] = mapped_column(Text, nullable = True)
    dishes: Mapped[list["Dish"]] = relationship(back_populates="canteen_obj")
    carousels: Mapped[list["Carousel"]] = relationship(back_populates="canteen_obj")



class Dish(Base):
    __tablename__ = "dishes"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    canteen:Mapped[int] = mapped_column(Integer, ForeignKey("canteens.id"), index=True)
    floor:Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    window:Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    name:Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    price:Mapped[float | None] = mapped_column(Numeric, nullable=True)
    measure:Mapped[str] = mapped_column(String(4), default="份")
    image:Mapped[str] = mapped_column(Text, nullable = True)
    average_vote:Mapped[float] = mapped_column(Numeric, default=2.5, index=True)
    canteen_obj:Mapped['Canteen'] = relationship(back_populates="dishes")
    new_dishes: Mapped[list["NewDish"]] = relationship("NewDish", back_populates="dish")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="dish")
    count_of_comments:Mapped[int] = mapped_column(Integer, default=0)
    count_of_votes:Mapped[int] = mapped_column(Integer, default=0)
    count_of_mark:Mapped[int] = mapped_column(Integer, default=0)

class NewDish(Base):
    __tablename__ = "new_dishes"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    dish_id:Mapped[int] = mapped_column(Integer, ForeignKey("dishes.id"), index=True)
    dish = relationship("Dish", back_populates="new_dishes")


class Carousel(Base):
    __tablename__ = "carousels"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    canteen:Mapped[int] = mapped_column(Integer, ForeignKey("canteens.id"), index=True)
    image:Mapped[str] = mapped_column(Text)
    canteen_obj:Mapped['Canteen'] = relationship(back_populates="carousels")

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    content:Mapped[str] = mapped_column(Text)
    time:Mapped[datetime.datetime] = mapped_column(DateTime, index=True)
    user:Mapped['User'] = relationship("User")
    towards:Mapped[int] = mapped_column(Integer, index=True)
    reply:Mapped[str | None] = mapped_column(Text, nullable=True)
    reply_time:Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
    reply_uid:Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    reply_user:Mapped['User'] = relationship("User", foreign_keys=[reply_uid])

class Mark(Base):
    __tablename__ = "marks"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    dish_id:Mapped[int] = mapped_column(Integer, ForeignKey("dishes.id"), index=True)
    time:Mapped[datetime.datetime] = mapped_column(DateTime, index=True)
    user:Mapped['User'] = relationship("User")
    dish:Mapped['Dish'] = relationship("Dish")
