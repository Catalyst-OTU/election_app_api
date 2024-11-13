from fastapi import APIRouter, Depends, HTTPException, Response, status
from config.session import get_db
from security.security import oauth2_scheme
from sqlalchemy.orm import Session
from domains.auth.services import auth as crud
from domains.auth.schemas import auth as schemas
from domains.auth.models import auth as models

from typing import List, Optional
from datetime import timedelta
import utils
import jwt
import sys

router = APIRouter()

logger = utils.get_logger()

@router.post("/login")
async def login(payload: schemas.Auth, api_key: Optional[str] = None, db: Session = Depends(get_db)):
    return crud.authenticate_user(payload, api_key, db)

@router.post("/refresh", response_model=schemas.Tokens)
async def refresh_user_token(payload: schemas.Tokens, db: Session = Depends(get_db)):
    data = utils.decode_access_token(data=payload.refresh_token)

    if not await crud.revoke_token(payload.refresh_token, db):
        raise HTTPException(status_code=500,detail="failed to revoke refresh token")

    if not await crud.revoke_token(payload.token, db):
        raise HTTPException(status_code=500,detail="failed to revoke access token")

    new_access_token = utils.create_access_token(data = {'phone_number': data.get('phone_number')}, expires_delta=timedelta(minutes=1440))
    new_refresh_token = utils.create_refresh_token(data = {"phone_number":data.get('phone_number')})
    
    return { 'token': new_access_token, 'refresh_token': new_refresh_token }

@router.post("/logout")
async def logout(payload: schemas.Tokens, db: Session = Depends(get_db)):
    access_token_revoke = await crud.revoke_token(payload.token, db)
    refresh_token_revoke = await crud.revoke_token(payload.refresh_token, db)
    if not access_token_revoke and refresh_token_revoke:
        return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
    return Response(status_code=status.HTTP_200_OK)

async def verify_token(token : str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    res = await crud.is_token_blacklisted(token, db)

    if res:
        raise HTTPException(status_code=401, detail="access unauthorised")

    try:
        token_data = utils.decode_access_token(data=token)
        if token_data:
            del token_data['exp']
            return token_data
        
    except jwt.exceptions.ExpiredSignatureError:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})

    except jwt.exceptions.DecodeError:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})