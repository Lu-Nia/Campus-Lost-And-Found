from sqlalchemy import create_engine, Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"
    
class ItemStatus(enum.Enum):
    LOST = "lost"
    FOUND = "found"
    CLAIMED = "claimed"

class ItemCategory(enum.Enum):
    ACCESSORIES = "Accessories"
    CARDS = "Cards"
    CLOTHING = "Clothing"
    ELECTRONICS = "Electronics"
    OTHERS = "Others"

class RegisteredStudent(Base):
    __tablename__ = "registered_students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_number = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100))

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    student_number = Column(String(20), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100))
    role = Column(String(20), default="student")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = relationship("Item", back_populates="owner")
    logs = relationship("Log", back_populates="changed_by_user")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    #category = Column(Enum(ItemCategory), nullable=False)
    category = Column(Enum(ItemCategory, values_callable=lambda x: [e.value for e in x]), nullable=False)
    #status = Column(Enum(ItemStatus), default=ItemStatus.LOST)
    status = Column(Enum(ItemStatus, values_callable=lambda obj: [e.value for e in obj]), default=ItemStatus.LOST.value)
    location = Column(String(255))
    image_url = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    contact_phone = Column(String(20))  # Add this field
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="items")
    logs = relationship("Log", back_populates="item")

class Log(Base):
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    action = Column(String(50), nullable=False)
    old_status = Column(Enum(ItemStatus))
    new_status = Column(Enum(ItemStatus))
    changed_by = Column(Integer, ForeignKey("users.id"))
    changed_at = Column(DateTime, default=datetime.utcnow)
    
    item = relationship("Item", back_populates="logs")
    changed_by_user = relationship("User", back_populates="logs")