from datetime import datetime
from typing import Optional

from pydantic import BaseModel, NonNegativeInt, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None


class UserDonationModel(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        from_attributes = True


class AdminDonationModel(UserDonationModel):
    user_id: Optional[int]
    invested_amount: NonNegativeInt = 0
    fully_invested: bool = False
    close_date: Optional[datetime]

    class Config:
        from_attributes = True
