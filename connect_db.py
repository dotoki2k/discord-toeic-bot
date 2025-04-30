import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from question import Base

engine = create_engine("sqlite:///toeic_db.db", echo=True)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
Base.metadata.create_all(bind=engine)
