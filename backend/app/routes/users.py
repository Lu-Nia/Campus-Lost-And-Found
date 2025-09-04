from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..auth import get_current_user
from ..routes.auth import get_password_hash
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

@router.patch("/password")
def update_password(
    password_data: PasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify current password
    from ..routes.auth import verify_password
    
    if not verify_password(password_data.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user.password = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}