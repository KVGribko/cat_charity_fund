from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.crud import charity_project_crud
from app.models import CharityProject


async def get_project(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    if project := await charity_project_crud.get(project_id, session):
        return project
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Charity project with id={project_id} not found",
    )


def check_closed(project: CharityProject, detail: str = ""):
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
