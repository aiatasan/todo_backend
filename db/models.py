from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import database
from datetime import datetime
# from jose import JWTError, jwt


class User(database.Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), unique=True, nullable=False)
    # password is set to contain 160 chars as for bcrypt hashing
    password = Column(String(160), nullable=False)
    # cascade="all, delete-orphan" ensures that when a user is deleted, all their associated todos will also be deleted.
    is_activated = Column(Boolean, default=False)
    todos = relationship("TodoList", back_populates="owner",
                         cascade="all, delete-orphan")
    tokens = relationship("Authentication", back_populates="user",
                          cascade="all, delete-orphan")


class TodoList(database.Base):
    __tablename__ = "todo_list"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    description = Column(String(1000), nullable=True)
    created_date = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime, nullable=True)
    # False - not done, True - completed
    status = Column(Boolean, default=False)

    owner = relationship("User", back_populates="todos")


class Authentication(database.Base):
    __tablename__ = "authentication"
    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="tokens")
