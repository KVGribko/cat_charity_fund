from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud, donation_crud
from app.models import CharityProject, Donation


async def investment(session: AsyncSession):
    donations: List[Donation] = (
        await donation_crud.get_not_fully_invested(session)
    )
    projects: List[CharityProject] = (
        await charity_project_crud.get_not_fully_invested(session)
    )
    project_index = 0
    donation_index = 0
    while donation_index < len(donations) and project_index < len(projects):
        project = projects[project_index]
        donation = donations[donation_index]
        need_amount = project.full_amount - project.invested_amount
        donation_amount = donation.full_amount - donation.invested_amount
        if need_amount > donation_amount:
            project.invested_amount += donation_amount
            close_object(donation)
            donation_index += 1
        elif need_amount < donation_amount:
            donation.invested_amount += need_amount
            close_object(project)
            project_index += 1
        else:
            close_object(donation)
            close_object(project)
            donation_index += 1
            project_index += 1
    session.add_all(donations)
    session.add_all(projects)
    await session.commit()


def close_object(object):
    object.fully_invested = True
    object.close_date = datetime.now()
