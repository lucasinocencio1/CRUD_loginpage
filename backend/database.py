from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite:///./database.db"

#create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
#create a session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#create a base class
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
