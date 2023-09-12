from app.models import CharityProject

from .base import CRUDBase


class CRUDCharityProject(CRUDBase):
    def __init__(self):
        super().__init__(CharityProject)


charity_project_crud = CRUDCharityProject()
