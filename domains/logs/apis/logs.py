from fastapi import APIRouter, HTTPException, Response, status
import utils

router = APIRouter()

@router.get("/")
async def show_logs():
    try:
        with open("logs.log", "r") as logger:
            logs = ""
            logger.seek(0)
            for log in logger.readlines():
                logs = logs + log
            return logs
    except:
        raise HTTPException(status_code=307, detail="Temporary Redirect .... could not open file")

@router.get("/io")
async def show_io_logs():
    try:
        with open("io_logs.log", "r") as logger:
            logs = ""
            logger.seek(0)
            for log in logger.readlines():
                logs = logs + log
            return logs
    except:
        raise HTTPException(status_code=307, detail="Temporary Redirect .... could not open file")