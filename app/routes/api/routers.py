from fastapi import APIRouter

from app.Config import ENV_PROJECT
from app.routes.api.v1.auth import router as auth_endpoints
# from app.routes.api.v1.admin import admin as admin_endponits
from app.routes.api.v1.user import user as user_endponits
from app.routes.api.v1.university import university as university_endponits
from app.routes.api.v1.college import college as college_endponits
# from app.routes.api.v1.sales import sales as sales_endpoints
routers = APIRouter()

routers.include_router(
    auth_endpoints,
    prefix=ENV_PROJECT.BASE_API_V1 + "/auth",
    tags=["Authentication"],
)

routers.include_router(
    user_endponits, prefix=ENV_PROJECT.BASE_API_V1 + "/user", tags=["user"]
)

routers.include_router(
    university_endponits, prefix=ENV_PROJECT.BASE_API_V1 + "/university", tags=["university"]
)

routers.include_router(
    college_endponits, prefix=ENV_PROJECT.BASE_API_V1 + "/college", tags=["college"]
)
# routers.include_router(
#     admin_endponits, prefix=ENV_PROJECT.BASE_API_V1 + "/admin", tags=["Admin"]
# )
