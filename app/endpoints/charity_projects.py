from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.schemas import (
    CharityProjectCreate,
    CharityProjectModel,
    CharityProjectUpdate,
)
from app.utils.charity_project import check_name, remove_project
from app.utils.charity_project import update_project as update_logic
from app.utils.investment import investment

router = APIRouter(
    prefix="/charity_project",
    tags=["Charity projects"],
)


@router.get(
    "/",
    response_model=list[CharityProjectModel],
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def get_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.post(
    "/",
    response_model=CharityProjectModel,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_projects(
    project: CharityProjectCreate = Body(...),
    session: AsyncSession = Depends(get_async_session),
):
    await check_name(project.name, session)
    project = await charity_project_crud.create(project, session)
    await investment(session)
    await session.refresh(project)
    return project


@router.delete(
    "/{project_id}",
    response_model=CharityProjectModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad parameters:",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
        },
    },
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await remove_project(project_id, session)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad parameters:",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
        },
    },
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    project: CharityProjectUpdate = Body(...),
    session: AsyncSession = Depends(get_async_session),
):
    return await update_logic(project_id, project, session)
