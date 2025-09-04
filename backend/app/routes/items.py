from fastapi import APIRouter, Depends, Form, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Item, User, ItemStatus, ItemCategory, Log
from ..auth import get_current_user
from pydantic import BaseModel
from datetime import datetime
import uuid
import os
from fastapi.staticfiles import StaticFiles

router = APIRouter(prefix="/items", tags=["items"])

# Mount static files directory for images
#router.mount("/static", StaticFiles(directory="static"), name="static")

# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_DIR = os.path.join(BASE_DIR, "static", "images")

# Create the static images directory if it doesn't exist
os.makedirs(STATIC_DIR, exist_ok=True)


class ItemBase(BaseModel):
    title: str
    description: str
    category: ItemCategory
    location: str
    contact_phone: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    status: ItemStatus
    image_url: Optional[str]
    user_id: int
    owner_name: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ItemUpdate(BaseModel):
    status: Optional[ItemStatus] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ItemCategory] = None
    location: Optional[str] = None

class StatsResponse(BaseModel):
    total_items: int
    lost_items: int
    found_items: int
    claimed_items: int

@router.post("/", response_model=ItemResponse)
def create_item(
    title: str = Form(...),
    description: str = Form(...),
    category: ItemCategory = Form(...),
    location: str = Form(None),
    contact_phone: str = Form(None),  # Add this parameter
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        category_enum = ItemCategory(category)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid category. Must be one of: {[e.value for e in ItemCategory]}"
        )
    
    image_url = None
    if image:
        # Generate unique filename
        file_extension = image.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        
        #  Save image to static directory using absolute path
        image_path = os.path.join(STATIC_DIR, filename)

        with open(image_path, "wb") as buffer:
            buffer.write(image.file.read())
        
        image_url = f"/static/images/{filename}"
        print(f"Image saved to: {image_path}")
        print(f"Image URL: {image_url}")
    
    # Create the item data dict
    item_data = {
        "title": title,
        "description": description,
        "category": category,
        "location": location

    }

     # Use provided contact phone or default to user's email
    final_contact_phone = contact_phone

    db_item = Item(
        **item_data,
        user_id=current_user.id,
        image_url=image_url,
        contact_phone=final_contact_phone  # Set the contact phone
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    item_dict = db_item.__dict__.copy()
    item_dict['owner_name'] = current_user.name  # Add owner's name
    
    # Log the creation
    log = Log(
        item_id=db_item.id,
        action="CREATE",
        new_status=db_item.status,
        changed_by=current_user.id
    )
    db.add(log)
    db.commit()
    
    return db_item

@router.get("/", response_model=List[ItemResponse])
def get_items(
    category: Optional[ItemCategory] = None,
    status: Optional[ItemStatus] = None,
    location: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Join with users table to get owner information
    query = db.query(Item, User.name).join(User, Item.user_id == User.id)
    
    if category:
        query = query.filter(Item.category == category)
    if status:
        query = query.filter(Item.status == status)
    if location:
        query = query.filter(Item.location.ilike(f"%{location}%"))
    if search:
        query = query.filter(
            (Item.title.ilike(f"%{search}%")) | 
            (Item.description.ilike(f"%{search}%"))
        )
    
    results = query.order_by(Item.created_at.desc()).all()
    
    # Transform the results to include owner information
    items_with_owner = []
    for item, owner_name in results:
        item_dict = item.__dict__.copy()
        item_dict['owner_name'] = owner_name  # Add owner's name to the response
        items_with_owner.append(item_dict)
    
    return items_with_owner
    

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Join with users table to get owner information
    result = db.query(Item, User.name)\
               .join(User, Item.user_id == User.id)\
               .filter(Item.id == item_id)\
               .first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item, owner_name = result
    
    # Add owner information to the response
    item_dict = item.__dict__.copy()
    item_dict['owner_name'] = owner_name
    
    return item_dict

@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this item")
    
    old_status = item.status
    
    update_data = item_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(item)
    
    # Log the status change if it occurred
    if "status" in update_data and old_status != item.status:
        log = Log(
            item_id=item.id,
            action="UPDATE_STATUS",
            old_status=old_status,
            new_status=item.status,
            changed_by=current_user.id
        )
        db.add(log)
        db.commit()
    
    return item

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")
    
    # Only allow deletion if status is found or claimed
    if item.status not in [ItemStatus.FOUND, ItemStatus.CLAIMED]:
        raise HTTPException(
            status_code=400, 
            detail="Can only delete items with status 'found' or 'claimed'"
        )
    
    # Log the deletion
    log = Log(
        item_id=item.id,
        action="DELETE",
        old_status=item.status,
        changed_by=current_user.id
    )
    db.add(log)
    
    db.delete(item)
    db.commit()
    
    return {"message": "Item deleted successfully"}

@router.get("/stats/overview", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_items = db.query(Item).count()
    lost_items = db.query(Item).filter(Item.status == ItemStatus.LOST).count()
    found_items = db.query(Item).filter(Item.status == ItemStatus.FOUND).count()
    claimed_items = db.query(Item).filter(Item.status == ItemStatus.CLAIMED).count()
    
    return StatsResponse(
        total_items=total_items,
        lost_items=lost_items,
        found_items=found_items,
        claimed_items=claimed_items
    )