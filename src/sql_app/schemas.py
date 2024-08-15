from pydantic import BaseModel

from datetime import datetime
class DishBase(BaseModel):
    canteen: int
    floor: int
    window: int
    name: str
    
class DishItemPriced(DishBase):
    id: int
    measure: str = '份'
    price: float | None = None

class DishItem(DishItemPriced):
    average_vote: float
    image: bytes = b''
class PricingData(BaseModel):
    price: float
    measure: str = '份'
class CarouselItem(BaseModel):
    canteen: int = 1
    image: bytes = b''
    
class CommentItem(BaseModel):
    user_id: int = 666666
    dish_id: int = 1
    content: str
    vote: int = 3
    time: datetime = datetime.now()

# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []

#     class Config:
#         orm_mode = True