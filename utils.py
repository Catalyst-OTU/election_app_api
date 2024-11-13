from fastapi import Depends, HTTPException
from datetime import datetime, timedelta, timezone
from security.security import oauth2_scheme
from typing import Optional
import logging
import random
import string
import json
import jwt
import os
import utils
from config.settings import Settings

SECRET_KEY = os.environ.get('SECRET_KEY') or "fsdfsdfsdfsdflhiugysadf87w940e-=r0werpolwe$16$5*dfsdfsdf&&#$rrr$$)7a9563OO93f7099f6f0f4caa6cf63b88e8d3e7"

ALGORITHM = os.environ.get('ALGORITHM') or "HS256"


def create_jwt_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = utcnow() + (expires_delta or timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, Settings.JWT_SECRET_KEY, algorithm=Settings.ALGORITHM)

def decode_jwt_token(token: str):
    return jwt.decode(token, Settings.JWT_SECRET_KEY, algorithms=[Settings.ALGORITHM])


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=40)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(*, data: str):
    try:
        to_decode = data
        return jwt.decode(to_decode, SECRET_KEY, algorithm=ALGORITHM)
    except jwt.exceptions.DecodeError: 
        raise HTTPException(status_code=500, detail="Not enough segments")
        
def verify_token(token : str = Depends(oauth2_scheme) ):
    try:
        token_data = utils.decode_access_token(data=token)
        if token_data:
            del token_data['exp']
            return token_data
            
    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException( status_code=401, detail="access token expired", headers={"WWW-Authenticate": "Bearer"})

    except jwt.exceptions.DecodeError as e:
        raise HTTPException( status_code=500, detail="decode error not enough arguments", headers={"WWW-Authenticate": "Bearer"})

# def synthesize_r_proxy(r_proxy):
#     key = r_proxy.keys()[0]
#     rows = [dict(row) for row in r_proxy]
#     return  rows[0][r_proxy.keys()[0]]


def synthesize_r_proxy(r_proxy):
    key = list(r_proxy.keys())[0]
    rows = [dict(row._mapping) for row in r_proxy]
    return rows[0][key]

    

# def timestamp_to_datetime(timestamp):
#     dt_obj = datetime.fromtimestamp(timestamp)
#     return dt_obj

def utcnow():
    return datetime.now(timezone.utc)

def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp, timezone.utc)

def stringify_json(data):
    hldr = ''
    i =  0

    for k,v in data.items():
        gp = """ "%s": "%s" """%(k,v)
        hldr += gp
        i += 1
        if i != len(data):
            hldr += ','

    hldr = "{"+hldr+"}"

    return hldr

def stringify_array_json(data):
    hldr = ''
    i =  0

    for item in data:
        gp = json.dumps(item)
        hldr += gp
        i += 1
        if i != len(data):
            hldr += ','

    hldr = "["+hldr+"]"

    return hldr


def get_logger():
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler = logging.FileHandler('logs.log', mode='a')
    handler.setLevel(level=logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
