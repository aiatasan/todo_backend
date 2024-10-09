# crud.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models
import schemas
from db.database import SessionLocal, engine, get_db
from typing import Optional
from fastapi import Request
from jose import JWTError, jwt


def create_user(db: Session, user: schemas.AddUserToDb):
    db.add(user)
    db.commit()
    db.refresh(user)

def create_item(db: Session, item: schemas.CreateItem):
    db.add(item)
    db.commit()
    db.refresh(item)

def create_user_item(db: Session, item: schemas.CreateItem, user_id: int):
    db_item = models.Item(**item.dict(), user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_user_items(db: Session, user_id: int, title_filter: Optional[str] = None):
    query = db.query(models.Item).filter(models.Item.user_id == user_id)
    if title_filter:
        query = query.filter(models.Item.title.ilike(f"%{title_filter}%"))
    return query.all()


def update_user_item(db: Session, item_id: int, item: schemas.UpdateItem, user_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id, models.Item.user_id == user_id).first()
    if db_item is None:
        return None
    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.name == username).first()


def get_user_by_username_or_email(db: Session, name: str = None, email: str = None):
    if not name and not email:
        return None

    query = db.query(models.User).filter(models.User.is_activated == True)
    print("checking")
    if name:
        query = query.filter(models.User.name == name)
        return query.first()
    if email:
        query = query.filter(models.User.email == email)
    return query.first()
