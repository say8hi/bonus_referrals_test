from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Purchase(BaseModel):
    id: int
    user_id: int
    package_id: int
    purchase_date: datetime

class User(BaseModel):
    id: int
    referal_id: Optional[int] = None
    created_at: datetime
    referrals: List["User"] = []
    purchases: List[Purchase] = []

class Package(BaseModel):
    id: int
    name: str
