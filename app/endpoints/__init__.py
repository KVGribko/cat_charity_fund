from .charity_projects import router as projects_router
from .donations import router as donation_router
from .user import router as user_router

list_of_routes = [
    donation_router,
    projects_router,
    user_router,
]


__all__ = [
    "list_of_routes",
]
