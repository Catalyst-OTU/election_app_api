from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal,engine
from _sockets import ConnectionManager
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI,Request,status,File,UploadFile
from crud.init_models import create_tables
from config.session import manager
# import utils
import os
from apis.routers import router as api_router
from config.session import session,get_db_connection


ROOT_DIR = os.path.dirname(os.path.relpath(__file__))
api = FastAPI(docs_url="/api/docs")
create_tables()
origins = ["*"]
api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


api.include_router(api_router)


@api.on_event("shutdown")
async def shutdown_event(websocket: WebSocket):
    await websocket.close(code=1000)
    print('server shutdown')

@api.on_event("startup")
async def startup_event():
    print('server started')

@api.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.broadcast(f"Client  says: h")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print('disconnected')

@api.get("/")
def welcome():
    return "Welcome to GBC FASTAPI link"







import time,logging

@api.middleware("http")
async def logs(request: Request, call_next):
    logger = get_logger()
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    try:
        logger.warning("{} {}: {} {} ".format(request.method, request.url, response.status_code, response.raw_headers))
    except:
        logger.error("failure on io middleware")
    return response

def get_logger():

    try:
        logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler = logging.FileHandler('io_logs.log', mode='a')
        handler.setLevel(level=logging.DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger
    except:
        pass





# Custom error handling middleware
@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_message = "Validation error occurred"
    # Optionally, you can log the error or perform additional actions here
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": error_message+f"{exc}"})

# Generic error handler for all other exceptions
@api.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    error_message = "An unexpected error occurred:\n"
    # Optionally, you can log the error or perform additional actions here
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": error_message+f"{exc}"})
    



