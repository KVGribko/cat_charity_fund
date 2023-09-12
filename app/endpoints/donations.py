from typing import List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core import get_async_session
from app.core.user import current_superuser, current_user
from app.crud import donation_crud
from app.models import User
from app.schemas import AdminDonationModel, DonationCreate, UserDonationModel
from app.utils.investment import investment

router = APIRouter(
    prefix="/donation",
    tags=["Donations"],
)


@router.get(
    "/",
    response_model=List[AdminDonationModel],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.post(
    "/",
    response_model=UserDonationModel,
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate = Body(...),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    donation = await donation_crud.create(donation, user.id, session)
    await investment(session)
    await session.refresh(donation)
    return donation


@router.get(
    "/my",
    response_model=List[UserDonationModel],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(current_user)],
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi_by_attribute(
        "user_id",
        user.id,
        session,
    )
