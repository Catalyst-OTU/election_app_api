from celery import shared_task
import sqlalchemy.exc
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from config.session import async_session, SessionLocal
# from passlib.hash import sha256_crypt
from passlib.hash import pbkdf2_sha256 as sha256
from domains.users.models import users as models
from domains.users.schemas import users as schemas
import utils
import sys
import sqlalchemy
from fastapi import HTTPException

logger = utils.get_logger()
# sha256 = sha256_crypt()



# # Task to create a reporter
# @shared_task
# def create_reporter_task(payload: dict):
#     with async_session() as db:
#         try:
#             # Create Reporter data
#             reporter_data = models.Reporter(
#                 phone_number=payload['phone_number'],
#                 reporter_name=payload['reporter_name'],
#                 gender=payload['gender'],
#                 constituency_id=payload['constituency_id']
#             )
#             db.add(reporter_data)
#             db.commit()
#             db.refresh(reporter_data)

#             # Create User data for Reporter
#             user_data = models.User(
#                 phone_number=payload['phone_number'],
#                 password=sha256.hash(payload['password'])
#             )
#             db.add(user_data)
#             db.commit()
#             db.refresh(user_data)

#             logger.info("Reporter created successfully")
#             return {"status": "success", "reporter_id": reporter_data.id}

#         except IntegrityError:
#             db.rollback()
#             logger.error("Database error: unique violation for reporter creation")
#             return {"status": "error", "message": "unique_violation"}

#         except Exception as e:
#             db.rollback()
#             logger.error(f"Error in create_reporter_task: {e}")
#             return {"status": "error", "message": str(e)}


# Task to create a reporter
@shared_task
def create_reporter_task(payload: dict):
    db = SessionLocal()  # Create a synchronous database session
    try:
        reporter_data = models.Reporter(
            phone_number=payload['phone_number'],
            reporter_name=payload['reporter_name'],
            gender=payload['gender'],
            constituency_id=payload['constituency_id']
        )
        db.add(reporter_data)
        db.commit()
        db.refresh(reporter_data)

        user_data = models.User(
            phone_number=payload['phone_number'],
            password=sha256.hash(payload['password'])
        )
        db.add(user_data)
        db.commit()
        db.refresh(user_data)

        logger.info("Reporter created successfully")
        return {"status": "success", "reporter_id": reporter_data.rec_id}

    except IntegrityError:
        db.rollback()
        logger.error("Database error: unique violation for reporter creation")
        return {"status": "error", "message": "unique_violation"}

    except Exception as e:
        db.rollback()
        logger.error(f"Error in create_reporter_task: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


# Task to create a user
@shared_task
def create_user_task(payload: dict):
    db = SessionLocal()  # Create a synchronous database session
    try:
        user_data = models.User(
            phone_number=payload['phone_number'],
            password=sha256.hash(payload['password'])
        )
        db.add(user_data)
        db.commit()
        db.refresh(user_data)

        logger.info("User created successfully")
        return {"status": "success", "user_id": user_data.rec_id}

    except IntegrityError:
        db.rollback()
        logger.error("Database error: unique violation for user creation")
        return {"status": "error", "message": "unique_violation"}

    except Exception as e:
        db.rollback()
        logger.error(f"Error in create_user_task: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


# # Task to create a user
# @shared_task
# def create_user_task(payload: dict):
#     with async_session() as db:
#         try:
#             # Create User data
#             user_data = models.User(
#                 phone_number=payload['phone_number'],
#                 password=sha256.hash(payload['password'])
#             )
#             db.add(user_data)
#             db.commit()
#             db.refresh(user_data)

#             logger.info("User created successfully")
#             return {"status": "success", "user_id": user_data.id}

#         except IntegrityError:
#             db.rollback()
#             logger.error("Database error: unique violation for user creation")
#             return {"status": "error", "message": "unique_violation"}

#         except Exception as e:
#             db.rollback()
#             logger.error(f"Error in create_user_task: {e}")
#             return {"status": "error", "message": str(e)}