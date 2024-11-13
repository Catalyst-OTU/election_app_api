# tasks/aiti_tasks.py

from celery import shared_task
from sqlalchemy.orm import Session
from config.session import async_session
from _sockets import ConnectionManager
import utils
import sys
import datetime
from domains.aiti.services import aiti as crud
import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import text

manager = ConnectionManager()
logger = utils.get_logger()

# Shared Celery task for polling station result
@shared_task
def add_polling_station_result_task(stamp, results, participant_id, polling_station_id, constituency_id, polling_station_name):
    with async_session() as db:
        try:
            # Convert results and timestamp
            rslts = utils.stringify_json(results)
            stamp = utils.timestamp_to_datetime(stamp)

            # Execute the stored procedure
            res = db.execute(
                text("""SELECT aiti.sp_add_polling_station_result(:stamp,:rslts,:participant_id,:polling_station_id,:constituency_id)""",
                {
                    'stamp': stamp, 
                    'rslts': rslts, 
                    'participant_id': participant_id, 
                    'polling_station_id': polling_station_id,
                    'constituency_id': constituency_id
                }
            ))
            db.commit()

            # Broadcast data asynchronously
            broadcast_data = {
                "type": "polling_update",
                "data": {
                    "stamp": stamp,
                    "results": results,
                    "participant_id": participant_id,
                    "polling_station_id": polling_station_id,
                    "constituency_id": constituency_id,
                    "polling_station_name": polling_station_name
                }
            }
            manager.broadcast_json(broadcast_data)
        except Exception as e:
            logger.error(f"Error in add_polling_station_result_task: {e}")
            db.rollback()

# Shared Celery task for parliamentary result
@shared_task
def add_parliamentary_result_task(stamp, results, participant_id, constituency_id):
    with async_session() as db:
        try:
            rslts = utils.stringify_json(results)
            stamp = utils.timestamp_to_datetime(stamp)

            # Execute stored procedure
            res = db.execute(
                text("""SELECT aiti.sp_add_parliamentary_result(:stamp,:rslts,:participant_id,:constituency_id)""",
                {
                    'stamp': stamp,
                    'rslts': rslts,
                    'participant_id': participant_id,
                    'constituency_id': constituency_id
                }
            ))
            db.commit()

            # Fetch and broadcast updated parliamentary result
            parliamentary_data = crud.get_parliamentary_result_by_rec_id(res.first().rec_id, db)
            if parliamentary_data:
                _dict = {k: str(v) if isinstance(v, datetime.datetime) else v for k, v in parliamentary_data.items()}
                manager.broadcast_json({"type": "parliamentary_update", "data": _dict})
        except Exception as e:
            logger.error(f"Error in add_parliamentary_result_task: {e}")
            db.rollback()

# Shared Celery task for presidential result
@shared_task
def add_presidential_result_task(stamp, results, participant_id, constituency_id):
    with async_session() as db:
        try:
            rslts = utils.stringify_json(results)
            stamp = utils.timestamp_to_datetime(stamp)

            # Execute stored procedure
            res = db.execute(
                text("""SELECT aiti.sp_add_presidential_result(:stamp,:rslts,:participant_id,:constituency_id)""",
                {
                    'stamp': stamp,
                    'rslts': rslts,
                    'participant_id': participant_id,
                    'constituency_id': constituency_id
                }
            ))
            db.commit()

            # Fetch and broadcast updated presidential result
            presidential_data = crud.get_presidential_result_by_rec_id(res.first().rec_id, db)
            if presidential_data:
                _dict = {k: str(v) if isinstance(v, datetime.datetime) else v for k, v in presidential_data.items()}
                manager.broadcast_json({"type": "presidential_update", "data": _dict})
        except Exception as e:
            logger.error(f"Error in add_presidential_result_task: {e}")
            db.rollback()

# Shared Celery task for constituency winner
@shared_task
def add_constituency_winner_task(candidate_id, constituency_id):
    with async_session() as db:
        try:
            # Execute stored procedure for constituency winner
            res = db.execute(
                text("""SELECT aiti.sp_add_constituency_winner(:candidate_id, :constituency_id)""",
                {'candidate_id': candidate_id, 'constituency_id': constituency_id}
            ))
            db.commit()
        except Exception as e:
            logger.error(f"Error in add_constituency_winner_task: {e}")
            db.rollback()

# Shared Celery task for confirming parliamentary result
@shared_task
def confirm_parliamentary_result_task(id):
    with async_session() as db:
        try:
            # Execute confirmation stored procedure
            res = db.execute(
                text("""SELECT aiti.sp_confirm_parliamentary_result(:id)""",
                {'id': id}
            ))
            db.commit()
        except Exception as e:
            logger.error(f"Error in confirm_parliamentary_result_task: {e}")
            db.rollback()

# Shared Celery task for confirming presidential result
@shared_task
def confirm_presidential_result_task(id):
    with async_session() as db:
        try:
            # Execute confirmation stored procedure
            res = db.execute(
                text("""SELECT aiti.sp_confirm_presidential_result(:id)""",
                {'id': id}
            ))
            db.commit()
        except Exception as e:
            logger.error(f"Error in confirm_presidential_result_task: {e}")
            db.rollback()

# Shared Celery task for adding an incident report
@shared_task
def add_incident_task(participant_id, polling_station_id, report, stamp, description, constituency_id):
    with async_session() as db:
        try:
            rslts = utils.stringify_array_json(report)
            stamp = utils.timestamp_to_datetime(stamp)

            # Execute stored procedure for incident
            res = db.execute(
                text("""SELECT aiti.sp_incident_add(:participant_id, :polling_station_id, :rslts, :stamp, :description, :constituency_id)""",
                {
                    'participant_id': participant_id,
                    'polling_station_id': polling_station_id,
                    'rslts': rslts,
                    'stamp': stamp,
                    'description': description,
                    'constituency_id': constituency_id
                }
            ))
            db.commit()
        except Exception as e:
            logger.error(f"Error in add_incident_task: {e}")
            db.rollback()

# Task for confirming an incident
@shared_task
def confirm_incident_task(id):
    with async_session() as db:
        try:
            # Execute the confirm incident stored procedure
            res = db.execute(
                text("""SELECT aiti.sp_confirm_incident(:id)""",
                {'id': id}
            ))
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            db.rollback()
            logger.error(f"Database error: unique_violation while confirming incident with id {id}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error in confirm_incident_task: {e}")


# Shared Celery task for toggling presidential result
@shared_task
def toggle_presidential_results_task(id):
    with async_session() as db:
        try:
            # Execute toggle stored procedure
            res = db.execute(
                text("""SELECT aiti.sp_update_presidential_result_2(:id)""",
                {'id': id}
            ))
            db.commit()
        except Exception as e:
            logger.error(f"Error in toggle_presidential_results_task: {e}")
            db.rollback()

# Shared Celery task for updating reporter information
@shared_task
def update_reporter_task(rec_id, phone_number, gender, constituency_id, name):
    with async_session() as db:
        try:
            # Execute update stored procedure for reporter
            res = db.execute(
                text("""SELECT aiti.sp_update_reporter(:rec_id, :phone_number, :gender, :constituency_id, :name)""",
                {
                    'rec_id': rec_id,
                    'phone_number': phone_number,
                    'gender': gender,
                    'constituency_id': constituency_id,
                    'name': name
                }
            ))
            db.commit()
        except Exception as e:
            logger.error(f"Error in update_reporter_task: {e}")
            db.rollback()


# Task for updating parliamentary results
@shared_task
def update_parliamentary_result_task(rec_id):
    with async_session() as db:
        try:
            res = db.execute(
                text("""SELECT aiti.sp_update_parliamentary_result_2(:rec_id)""",
                {'rec_id': rec_id}
            ))
            db.commit()
        except sqlalchemy.exc.IntegrityError:
            db.rollback()
            logger.error(f"Database error: unique_violation while updating result with rec_id {rec_id}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error in update_parliamentary_result_task: {e}")




























# # tasks/aiti_tasks.py
# from celery import shared_task
# from sqlalchemy.orm import Session
# from config.session import async_session
# from domains.aiti.services import aiti as crud
# from _sockets import ConnectionManager

# manager = ConnectionManager()

# # Shared Celery task for polling station result
# @shared_task
# def add_polling_station_result_task(stamp, results, participant_id, polling_station_id, constituency_id, polling_station_name):
#     db: Session = async_session()
#     result = crud.add_polling_station_result(stamp, results, participant_id, polling_station_id, constituency_id, db)
    
#     if result:
#         broadcast_data = {
#             "type": "polling_update",
#             "data": {
#                 "stamp": stamp,
#                 "results": results,
#                 "participant_id": participant_id,
#                 "polling_station_id": polling_station_id,
#                 "constituency_id": constituency_id,
#                 "polling_station_name": polling_station_name
#             }
#         }
#         manager.broadcast_json(broadcast_data)
    
#     db.close()
#     return result

# @shared_task
# def add_parliamentary_result_task(stamp, results, participant_id, constituency_id):
#     db: Session = async_session()
#     result = crud.add_parliamentary_result(stamp, results, participant_id, constituency_id, db)
    
#     if result:
#         broadcast_data = {"type": "parliamentary_update", "data": result}
#         manager.broadcast_json(broadcast_data)

#     db.close()
#     return result

# # Define similar tasks for `add_presidential_result` and any other routes that require task queuing.
