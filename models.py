# models.py
import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# prefer DATABASE_URL (Postgres) in production; fallback to DB_PATH or sqlite file.
DB_URL = os.getenv("DATABASE_URL") or os.getenv("DB_PATH") or "sqlite:///news_summaries.db"
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
engine = create_engine(DB_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)

class Summary(Base):
    __tablename__ = "summaries"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(100), index=True)
    title = Column(String(500))
    summary_text = Column(Text)
    source_url = Column(String(1000))
    audio_file = Column(String(500))  # store relative path under static/, e.g. 'audio/xxx.mp3'
    published_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
