from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class CharityProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2)
    full_amount: PositiveInt


class CharityProjectModel(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, min_length=2)
    full_amount: Optional[PositiveInt] = None

    class Config:
        extra = Extra.forbid
