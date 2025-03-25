from fastapi import FastAPI
from app.routes.accounts import router as account_router
from app.routes.courses import router as courses_router
from app.routes.lessons import router as lessons_router


def all_routers(app: FastAPI):
   app.include_router(account_router, prefix="/account", tags=['accounts'])
   app.include_router(courses_router, prefix="/courses", tags=['courses'])
   app.include_router(lessons_router, prefix="/courses/lessons", tags=['lessons'])