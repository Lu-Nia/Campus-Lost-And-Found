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


class ItemUpdate(BaseModel):
    status: ItemStatus

class ItemResponse(BaseModel):
    id: str
    name: str
    description: str
    location: str
    date_reported: datetime
    status: ItemStatus
    contact_email: str
    contact_phone: Optional[str]
    is_lost_report: bool
    linked_item_id: Optional[str]
    
    class Config:
        from_attributes = True

# ---------------- Create Tables ----------------
Base.metadata.create_all(bind=engine)

# ---------------- FastAPI App ----------------
app = FastAPI(
    title="Campus Digital Lost & Found API",
    description="API for managing lost and found items on campus",
    version="1.0.0"
)

# ---------------- Static Files ----------------
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------- Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Helper Functions ----------------
def generate_item_id():
    return str(uuid.uuid4())[:8].upper()

# ---------------- Serve HTML Interface ----------------
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_path = os.path.join("static", "index.html")
    return FileResponse(html_path)
# ---------------- Health Check ----------------
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running successfully"}

# ---------------- CRUD Routes ----------------
@app.post("/api/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    existing = db.query(Item).filter(
        Item.name.ilike(f"%{item.name}%"),
        Item.contact_email == item.contact_email,
        Item.is_lost_report == item.is_lost_report,
        Item.status != ItemStatus.claimed
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A similar item has already been reported by this user"
        )
    
    db_item = Item(
        id=generate_item_id(),
        **item.dict(),
        status=ItemStatus.found if not item.is_lost_report else ItemStatus.lost
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item

@app.get("/api/items", response_model=List[ItemResponse])
def get_items(
    name: Optional[str] = None,
    location: Optional[str] = None,
    status: Optional[ItemStatus] = None,
    item_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Item)
    if name:
        query = query.filter(Item.name.ilike(f"%{name}%"))
    if location:
        query = query.filter(Item.location.ilike(f"%{location}%"))
    if status:
        query = query.filter(Item.status == status)
    if item_type == "lost":
        query = query.filter(Item.is_lost_report == True)
    elif item_type == "found":
        query = query.filter(Item.is_lost_report == False)
    
    return query.order_by(Item.date_reported.desc()).all()


