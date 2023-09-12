from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud import charity_project_crud
from app.models import CharityProject

from .common import check_closed, get_project


async def remove_project(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await get_project(project_id, session)
    error_detail = "В проект были внесены средства, не подлежит удалению!"
    check_closed(project, error_detail)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail,
        )
    return await charity_project_crud.remove(project, session)
