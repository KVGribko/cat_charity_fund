from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation
from app.schemas import UserDonationModel
from .base import CRUDBase


class CRUDDonation(CRUDBase):
    def __init__(self):
        super().__init__(Donation)

    async def create(
        self,
        donation: UserDonationModel,
        user_id: int,
        session: AsyncSession,
    ):
        new_donation = self.model(**donation.dict(), user_id=user_id)
        session.add(new_donation)
        await session.commit()
        await session.refresh(new_donation)
        return new_donation


donation_crud = CRUDDonation()
