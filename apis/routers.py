from domains.auth.apis import auth
from domains.users.apis import users
from domains.aiti.apis import aiti
from domains.logs.apis import logs
from domains.monitor import enqueued_tasks
from domains.query_router import main
from fastapi import APIRouter


router = APIRouter()
router.include_router(auth.router,prefix="/api/auth",tags=["auth"])
router.include_router(users.router,prefix="/api/users",tags=["user"])
router.include_router(aiti.router,prefix="/api/aiti",tags=["aiti"])
router.include_router(logs.router,prefix="/api/logs",tags=["logs"])
router.include_router(enqueued_tasks.task_api,prefix="/api/monitor_task",tags=["Queued Tasks"])
router.include_router(main.router,prefix="/api/setup-data",tags=["Upload SQL File"])


