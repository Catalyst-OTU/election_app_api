import re
import logging
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException,  BackgroundTasks
from sqlalchemy import text, inspect, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError
# from database import engine, SessionLocal, database, metadata
import sqlparse
from _sockets import ConnectionManager
from celery.result import AsyncResult
from celery_worker import celery_app
import psycopg2
from psycopg2 import connect, sql, DatabaseError
import asyncpg
from .tasks import execute_sql_task
import time

router = APIRouter()
manager = ConnectionManager()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/execute-sql/")
async def execute_sql(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.endswith('.sql'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an SQL file.")
    
    try:
        content = (await file.read()).decode('utf-8')
        task = execute_sql_task.delay(content)
        background_tasks.add_task(monitor_task, task.id)
        return {"task_id": task.id, "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/task-status/{task_id}")
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

def monitor_task(task_id: str):
    result = AsyncResult(task_id)
    print("\nmonitored task id: ", task_id)
    print("\nresult: ", result)
    while not result.ready():
        time.sleep(1)  # Sleep to prevent busy-waiting
        # pass
    # Additional handling or logging can be added here if necessary



# @router.post("/execute-sql/")
# async def execute_sql(file: UploadFile = File(...)):
#     if not file.filename.endswith('.sql'):
#         raise HTTPException(status_code=400, detail="Invalid file type. Please upload an SQL file.")
    
#     try:
#         await execute_sql_file(file)
#         return {"message": "SQL file executed successfully."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))





# DATABASE_URL = SQLALCHEMY_DATABASE_URL

# Helper functions
# async def execute_sql_file(file: UploadFile):
#     content = (await file.read()).decode('utf-8')
#     statements = split_sql_statements(content)
#     print("\ndatabase: ", database)
#     async with database.transaction():
#         for statement in statements:
#             if statement.strip():
#                 statement = transform_sql_to_postgresql(statement)
#                 try:
#                     await database.execute(statement)
#                 except asyncpg.exceptions.DuplicateTableError:
#                     # Skip existing CREATE TABLE or SCHEMA errors
#                     continue
#                 except asyncpg.exceptions.UniqueViolationError:
#                     # Handle unique violations gracefully
#                     continue
#                 except Exception as e:
#                     raise HTTPException(status_code=400, detail=f"SQL execution error: {str(e)}")

# def split_sql_statements(content: str):
#     # Split the content into individual SQL statements, taking care of comments and multi-line commands
#     statements = re.split(r';\s*(?=(?:[^\'"]*["\'][^\'"]*["\'])*[^\'"]*$)', content)
#     return [stmt.strip() for stmt in statements if stmt.strip()]

# def transform_sql_to_postgresql(statement: str) -> str:
#     """
#     Transforms general SQL syntax to be compatible with PostgreSQL, covering various SQL constructs.
#     """
#     # Correct MySQL-specific syntax and transform it into PostgreSQL
#     statement = re.sub(r"`", r'"', statement)  # Convert backticks to double quotes
#     statement = re.sub(r"(?i)\bAUTO_INCREMENT\b", "SERIAL", statement, flags=re.IGNORECASE)
#     statement = re.sub(r",\s*\)", ")", statement)  # Remove trailing commas before closing parenthesis
#     statement = re.sub(r"\bVALUES\s*\(([^)]+)\)", correct_insert_values, statement, flags=re.IGNORECASE)
#     statement = re.sub(r"\);?\s*$", ");", statement.strip())  # Ensure statements end with a semicolon
#     statement = re.sub(r'BEGIN\s+/', 'BEGIN;', statement, flags=re.IGNORECASE)  # Correct BEGIN block
#     statement = re.sub(r'END\s+/', 'END;', statement, flags=re.IGNORECASE)  # Correct END block
#     statement = re.sub(r"(?i)\bDELIMITER\s+//", "", statement)  # Remove DELIMITER directives
#     statement = re.sub(r"(?i)\bDELIMITER\s*;", "", statement)  # Normalize statement end delimiter
#     statement = re.sub(r"(?i)\bSHOW\s+WARNINGS\b", "-- SHOW WARNINGS not supported in PostgreSQL", statement)
#     return statement

# def correct_insert_values(match):
#     values = match.group(1)
#     corrected_values = re.sub(r'"([^"]+):\s*([^"]+)"', r"('\1', \2)", values)
#     return f"VALUES {corrected_values}"









