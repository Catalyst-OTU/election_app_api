from fastapi import APIRouter, Depends, HTTPException, Response, status
from config.session import get_db

from security.security import oauth2_scheme
from sqlalchemy.orm import Session
from domains.users.services import users as crud
from domains.users.schemas import users as schemas
from domains.users.models import users as models
from datetime import timedelta
from .users_tasks import create_reporter_task, create_user_task
import utils
import sys
import jwt

router = APIRouter()

# @router.post("/", description="create user", status_code=status.HTTP_201_CREATED)
# async def create_user(payload: schemas.UserBase, db: Session = Depends(get_db)):
#     user = await crud.create_user(payload,db)
#     if not user:
#         raise HTTPException(status_code=400)
#     return user

@router.post("/", description="create user", status_code=status.HTTP_202_ACCEPTED)
async def create_user(payload: schemas.UserBase):
    task = create_user_task.delay(payload.dict())
    return {"task_id": task.id, "status": "Task enqueued"}


# @router.post("/reporters", description="create reporters", status_code=status.HTTP_201_CREATED)
# async def create_reporter(payload: schemas.Reporter, db: Session = Depends(get_db)):
#     reporter = await crud.create_reporter(payload,db)
#     if not reporter:
#         raise HTTPException(status_code=400)
#     return reporter

@router.post("/reporters", description="create reporters", status_code=status.HTTP_202_ACCEPTED)
async def create_reporter(payload: schemas.Reporter):
    task = create_reporter_task.delay(payload.dict())
    return {"task_id": task.id, "status": "Task enqueued"}


# reporters
@router.get("/", description="get all reporters")
async def get_users( db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:str=None, value:str=None,):
    return await crud.get_users(db,skip,limit,search,value)
    


