from celery.result import AsyncResult
from fastapi import APIRouter


task_api = APIRouter()

@task_api.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    return {"task_id": task_id, "status": task_result.status, "result": task_result.result}


@task_api.get("/task-status/{task_id}")
def get_status(task_id: str):
    task_result = AsyncResult(task_id)
    print("\ntask_result:: ", task_result)
    print("\ntask_result.state:: ", task_result.state)
    if task_result.state == "PENDING":
        response = {"task_id": task_id, "status": "pending"}
    elif task_result.state != "FAILURE":
        response = {"task_id": task_id, "status": task_result.state, "result": task_result.result}
    else:
        response = {"task_id": task_id, "status": "failed", "result": str(task_result.info)}
    
    print("\ntask response:: ", response)
    return response