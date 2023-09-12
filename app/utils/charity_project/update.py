from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdate

from .common import check_closed, get_project


async def update_project(
    project_id: int,
    new_data: CharityProjectUpdate,
    session: AsyncSession,
) -> CharityProject:
    project = await get_project(project_id, session)
    check_closed(project, "Закрытый проект нельзя редактировать!")
    if new_data.name:
        await check_name(new_data.name, session)
    if new_data.full_amount and new_data.full_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "При редактировании проекта нельзя "
                "устанавливать требуемую сумму меньше внесённой."
            ),
        )
    return await charity_project_crud.update(project, new_data, session)


async def check_name(name: str, session: AsyncSession):
    project_wiht_this_name = await charity_project_crud.get_by_attribute(
        "name",
        name,
        session,
    )
    if project_wiht_this_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Проект с таким именем уже существует!",
        )
