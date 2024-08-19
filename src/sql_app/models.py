from typing import Any
from sqlalchemy import Boolean, ForeignKey, Integer, String, Numeric,LargeBinary, Text, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import DeclarativeBase
import datetime


class Base(DeclarativeBase):
    pass

class User(Base):   # This class is to be used in the future for user management
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    username:Mapped[str] = mapped_column(String(20), index=True)
    sdu_id:Mapped[str] = mapped_column(String(20), index=True, unique=True)
    is_admin:Mapped[str] = mapped_column(Boolean, default=False)

class Admin(Base):   # The users with privileges to do data modification, whose login should be different from the normal users
    __tablename__ = "admins"

    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    access_name:Mapped[str] = mapped_column(String(20), index=True)
    hashed_password:Mapped[str] = mapped_column(String(64), index=True)


class Comment(Base):   # This class is to be used in the future
    __tablename__ = "comments"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    dish_id:Mapped[int] = mapped_column(Integer, ForeignKey("dishes.id"))
    content:Mapped[str] = mapped_column(Text)
    vote:Mapped[int] = mapped_column(Integer)
    time:Mapped[datetime.datetime] = mapped_column(DateTime, index=True)



class Canteen(Base):  
    __tablename__ = "canteens"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(8), index=True, nullable=False, unique=True)
    description:Mapped[str] = mapped_column(Text, index=True)
    image:Mapped[bytes] = mapped_column(LargeBinary)
    campus:Mapped[str] = mapped_column(String(8), index=True, nullable=False)



class Dish(Base):
    __tablename__ = "dishes"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    canteen:Mapped[int] = mapped_column(Integer, ForeignKey("canteens.id"), index=True)
    floor:Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    window:Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    name:Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    price:Mapped[float | None] = mapped_column(Numeric, nullable=True)
    measure:Mapped[str] = mapped_column(String(4), default="份")
    image:Mapped[bytes] = mapped_column(LargeBinary, default=b'')
    average_vote:Mapped[float] = mapped_column(Numeric, default=2.5, index=True)
    
    
    

class NewDish(Base):
    __tablename__ = "new_dishes"
    
    id:Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    dish_id:Mapped[int] = mapped_column(Integer, ForeignKey("dishes.id"), index=True)
    dish = relationship("Dish", back_populates="new_dishes")


class Carousel(Base):
    __tablename__ = "carousels"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    canteen:Mapped[int] = mapped_column(Integer, ForeignKey("canteens.id"), index=True)
    image:Mapped[bytes] = mapped_column(LargeBinary)

