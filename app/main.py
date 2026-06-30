from fastapi import FastAPI ,HTTPException,Depends
from pydantic import BaseModel
from typing import List,Annotated
from database import get_database_url
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL = get_database_url()

# Create a new SQLAlchemy engine instance
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        
app = FastAPI()


class DemandeBase(BaseModel):
    Num_Compte :int
    demande_id :
