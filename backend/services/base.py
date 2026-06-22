from typing import Type, TypeVar, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import as_declarative

ModelType = TypeVar("ModelType", bound="Base")


@as_declarative()
class Base:
    id: Optional[int]


class CRUDService:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def create(self, db: Session, obj_in: dict) -> ModelType:
        try:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def read(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def update(self, db: Session, id: int, obj_in: dict) -> Optional[ModelType]:
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            return None
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        try:
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def delete(self, db: Session, id: int) -> bool:
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            return False
        try:
            db.delete(db_obj)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise e