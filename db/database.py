# database.py
# Set up of the todo.db connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

# engine is responsible to communicate with the todo.db
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# session for interactiog with the db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# all tables will inherit from this Base class
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

