from fastapi import FastAPI
from app.routes.account import router as account_router
from app.routes.courses import router as courses_router


def all_routers(app: FastAPI):
   app.include_router(account_router, prefix="/account", tags=['account'])
   app.include_router(courses_router, prefix="/courses", tags=['courses'])