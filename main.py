from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy import create_engine, Column, String, DateTime, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import enum
import uuid
import os

# ---------------- Database Setup ----------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./lost_and_founds.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ---------------- Enums ----------------
class ItemStatus(str, enum.Enum):
    lost = "lost"
    found = "found"
    claimed = "claimed"

# ---------------- Models ----------------
class Item(Base):
    __tablename__ = "items"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    date_reported = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(ItemStatus), default=ItemStatus.lost)
    contact_email = Column(String, nullable=False)
    contact_phone = Column(String, nullable=True)
    is_lost_report = Column(Boolean, default=True)
    linked_item_id = Column(String, nullable=True)

# ---------------- Pydantic Schemas ----------------
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    location: str = Field(..., min_length=1, max_length=100)
    contact_email: str
    contact_phone: Optional[str] = None
    is_lost_report: bool = True

