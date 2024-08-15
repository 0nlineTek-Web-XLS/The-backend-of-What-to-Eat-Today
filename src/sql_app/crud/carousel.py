from sqlalchemy.orm import Session

from ..models import Carousel
from ..schemas import CarouselItem

def add(db: Session, carousel: CarouselItem):
    db_carousel = Carousel(canteen=carousel.canteen, 
                          image=carousel.image)
    db.add(db_carousel)
    db.commit()
    db.refresh(db_carousel)
    return db_carousel

def get(db: Session, canteen: int):
    return db.query(Carousel).filter(Carousel.canteen == canteen).all()

def delete(db: Session, carousel: CarouselItem):
    db.query(Carousel).filter(Carousel.canteen == carousel.canteen) \
        .filter(Carousel.image == carousel.image).delete()
    db.commit()


