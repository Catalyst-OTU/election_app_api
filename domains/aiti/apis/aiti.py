from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from config.session import get_db
from config.session import manager
import datetime
from domains.aiti.services import aiti as crud
from domains.aiti.schemas import aiti as schemas
from domains.aiti.models import aiti as models
from .aiti_tasks import (
    add_polling_station_result_task,
    add_parliamentary_result_task,
    add_presidential_result_task,
    add_constituency_winner_task,
    add_incident_task,
    confirm_parliamentary_result_task,
    confirm_presidential_result_task,
    toggle_presidential_results_task,
    update_reporter_task,
    update_parliamentary_result_task,
    confirm_incident_task
)

from domains.auth.apis.auth import verify_token
#from ..auth_router.main import verify_token
#from . import crud, schemas, models

router = APIRouter()

# GET

@router.get("/regions", response_model=schemas.ApiResponse)
async def regions(db: Session = Depends(get_db)):
    results = await crud.get_region(db)
    return {"data": results if results is not None else []}

@router.get("/constituencies", response_model=schemas.ApiResponse)
async def constituencies(db: Session = Depends(get_db)):
    results = await crud.get_constituency(db)
    return {"data": results if results is not None else []}

@router.get("/incidents", response_model=schemas.ApiResponse)
async def incidents(db: Session = Depends(get_db)):
    results = await crud.get_all_incidents(db)
    return {"data": results if results is not None else []}

@router.get("/constituencies/winners", response_model=schemas.ApiResponse)
async def constituency_winners(db: Session = Depends(get_db)):
    results = await crud.get_all_constituency_winners(db)
    return {"data": results if results is not None else []}

@router.get("/politicalparties", response_model=schemas.ApiResponse)
async def political_parties(db: Session = Depends(get_db)):
    results = await crud.get_all_parties(db)
    return {"data": results if results is not None else []}

@router.get("/candidates", response_model=schemas.ApiResponse)
async def candidates(db: Session = Depends(get_db)):
    results = await crud.get_all_candidates(db)
    return {"data": results if results is not None else []}

@router.get("/parliamentarians", response_model=schemas.ApiResponse)
async def parliamentarians(db: Session = Depends(get_db)):
    results = await crud.get_all_parliamentarians(db)
    return {"data": results if results is not None else []}

@router.get("/aggregations/national/presidential")
async def national_presidential_aggregations(db: Session = Depends(get_db)):
    results = await crud.get_national_presidential_aggregations(db)
    return {"data": results if results is not None else []}

@router.get("/past/regional/results", response_model=schemas.ApiResponse)
async def past_regional_results(db: Session = Depends(get_db)):
    results = await crud.get_past_regional_results(db)
    return {"data": results if results is not None else []}



@router.get("/past/regional/results/2020", response_model=schemas.ApiResponse)
async def past_regional_results_for_2020(db: Session = Depends(get_db)):
    results = await crud.get_past_regional_results_for_2020(db)
    return {"data": results if results is not None else []}





@router.get("/past/regional/results/2016", response_model=schemas.ApiResponse)
async def past_regional_results_for_2016(db: Session = Depends(get_db)):
    results = await crud.get_past_regional_results_for_2016(db)
    return {"data": results if results is not None else []}





@router.get("/past/national/results", response_model=schemas.ApiResponse)
async def past_national_results(db: Session = Depends(get_db)):
    results = await crud.get_past_national_results(db)
    return {"data": results if results is not None else []}

@router.get("/past/constituency/results", response_model=schemas.ApiResponse)
async def past_constituency_results(db: Session = Depends(get_db)):
    results = await crud.get_past_constituency_results(db)
    return {"data": results if results is not None else []}

@router.get("/constituencies/{id}/parliamentaryresults", response_model=schemas.ApiResponse)
async def parliamentary_result(id: int, db: Session = Depends(get_db)):
    results = await crud.get_parliamentary_result(id, db)
    return {"data": results if results is not None else []}

# used to confirm parliamentary results
@router.get("/parliamentaryresults/{id}/confirm")
async def confirmed_parliamentary_result(id: int, db: Session = Depends(get_db)):
    results = await crud.get_confirmed_parliamentary_result(id, db)
    if not results:
        raise HTTPException(status_code=501)
    return Response(status_code=status.HTTP_200_OK)

@router.get("/presidentialresults/{constituency_id}", response_model=schemas.ApiResponse)
async def presidential_result_by_constituency_id(constituency_id: int, db: Session = Depends(get_db)):
    results = await crud.get_presidential_result(constituency_id, db)
    return {"data": results if results is not None else []}

@router.get("/pollingstations/{polling_station_id}/siblings", response_model=schemas.ApiResponse)
async def get_polling_siblings(polling_station_id: str, db: Session = Depends(get_db)):
    results = await crud.get_polling_siblings(polling_station_id, db)
    return {"data": results if results is not None else []}

@router.get("/constituencies/{constituency_id}/incidents", response_model=schemas.ApiResponse)
async def incident_by_constituency_id(constituency_id: str, db: Session=Depends(get_db)):
    results = await crud.get_incidents(constituency_id, db)
    return {"data": results if results is not None else []}

@router.get("/reporters", response_model=schemas.ApiResponse)
async def get_constituency_reporters(constituency_name: str, db: Session=Depends(get_db)):
    results = await crud.get_constituency_reporters(constituency_name, db)
    return {"data": results if results is not None else []}

@router.get("/aggregations/presidential")
async def get_presidential_result_aggregations(constituency_name: str, db:Session=Depends(get_db)):
    results = await crud.get_presidential_result_aggregations(constituency_name, db)
    return {"data": results if results is not None else []}

@router.get("/aggregations/pollingstations")
async def get_constituency_pres_polling_station_agg(constituency_name: str, db:Session=Depends(get_db)):
    results = await crud.get_constituency_pres_polling_station_agg(constituency_name, db)
    return {"data": results if results is not None else []}

@router.get("/aggregations/regional/presidential")
async def get_reg_pres_agg(region: str, db: Session=Depends(get_db)):
    results = await crud.get_reg_pres_agg(region, db)
    return {"data": results if results is not None else []}

@router.get("/aggregations/pollingstation/presidential")
async def get_reg_pres_polling_station_agg(region: str, db: Session = Depends(get_db)):
    results = await crud.get_reg_pres_polling_station_agg(region, db)
    return {"data": results if results is not None else []}

@router.get("/constituencies/{code}", response_model=schemas.ApiResponse)
async def get_constituency_by_code(code: str, db: Session=Depends(get_db)):
    results = await crud.get_constituency_by_code(code, db)
    return {"data": results if results is not None else []}

@router.get("/pollingstations/{code}", response_model=schemas.ApiResponse)
async def get_polling_station(code: str, db: Session=Depends(get_db)):
    results = await crud.get_polling_station(code, db)
    return {"data": results if results is not None else []}

@router.get("/constituencies/{ps_code}/parliamentarians", response_model=schemas.ApiResponse)
async def get_const_parliamentarians(ps_code: str, db: Session=Depends(get_db)):
    results = await crud.get_const_parliamentarians(ps_code, db)
    return {"data": results if results is not None else []}

@router.get("/aggregations/pollingstation/national/presidential")
async def get_national_pres_polling_station_agg(db: Session=Depends(get_db)):
    results = await crud.get_national_pres_polling_station_agg(db)
    return {"data": results if results is not None else []}

@router.get("/parliamentarians/constituencies/{id}")
async def get_candidate_by_constituency_id(id: int, db: Session=Depends(get_db)):
    results = await crud.get_candidate_by_constituency_id(id, db)
    return results

@router.get("/incidents/{id}")
async def get_incidents_by_rec_id(id: int, db: Session=Depends(get_db)):
    results = await crud.get_incidents_by_rec_id(id, db)
    return {"data": results if results is not None else []}

@router.get("/incidents/constituencies/{constituency_id}")
async def get_incidents_to_update(constituency_id: str, db: Session = Depends(get_db)):
    results = await crud.get_incidents_to_update(constituency_id, db)
    return {"data": results if results is not None else []}

@router.get("/past/parliamentary/constituencies/results")
async def get_past_parliamentary_constituencies(db: Session = Depends(get_db)):
    results = await crud.get_past_parliamentary_constituencies(db)
    return {"data": results if results is not None else []}

@router.get("/past/parliamentary/regional/results")
async def get_past_parliamentary_regional(db: Session = Depends(get_db)):
    results = await crud.get_past_parliamentary_regional(db)
    return {"data": results if results is not None else []}

@router.get("/past/parliamentary/national/results")
async def get_past_parliamentary_national(db: Session = Depends(get_db)):
    results = await crud.get_past_parliamentary_national(db)
    return {"data": results if results is not None else []}
    
# POST

# @router.post("/pollingstations")
# async def  add_polling_station_result(payload: schemas.PollingStationCreate, db: Session = Depends(get_db)):
#     data = payload.dict()

#     res = await crud.add_polling_station_result(payload.stamp, payload.results, payload.participant_id, payload.polling_station_id, payload.constituency_id, db)
#     if not res:
#         return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)

#     data['polling_station_name'] = payload.polling_station_name
#     await manager.broadcast_json( {"type":"polling_update", "data":data} )

#     return Response(status_code=status.HTTP_201_CREATED)

@router.post("/pollingstations")
async def add_polling_station_result(payload: schemas.PollingStationCreate):
    # Call Celery task instead of direct database operation
    task = add_polling_station_result_task.delay(
        payload.stamp, payload.results, payload.participant_id,
        payload.polling_station_id, payload.constituency_id, payload.polling_station_name
    )
    return {"task_id": task.id, "status": "Task Enqueued for processing ..."}
    # return Response(status_code=status.HTTP_202_ACCEPTED)  # Accepted, task in progress



# @router.post("/parliamentaryresults")
# async def  add_parliamentary_result(payload: schemas.ParliamentaryResultsCreate, db: Session = Depends(get_db)):
#     res = await crud.add_parliamentary_result(payload.stamp, payload.results, payload.participant_id, payload.constituency_id, db)
#     if not res:
#         return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
#     data = await crud.get_parliamentary_result_by_rec_id(res, db)
#     if data is not None:
#         _dict = {}
#         for item in data.items():
#             if isinstance(item[1], datetime.datetime):
#                 _dict[item[0]]=str(item[1])
#                 continue
#             _dict[item[0]] = item[1]
#         await manager.broadcast_json( {"type":"parliamentary_update", "data": _dict } )
#     return Response(status_code=status.HTTP_201_CREATED)

@router.post("/parliamentaryresults")
async def add_parliamentary_result(payload: schemas.ParliamentaryResultsCreate):
    # Call Celery task
    task = add_parliamentary_result_task.delay(
        payload.stamp, payload.results, payload.participant_id, payload.constituency_id
    )
    # return Response(status_code=status.HTTP_202_ACCEPTED)
    return {"task_id": task.id, "status": "Task Enqueued for processing ..."}

# @router.post("/presidentialresults")
# async def  add_presidential_result(payload: schemas.PresidentialResultsCreate, db: Session = Depends(get_db)):
#     res = await crud.add_presidential_result(payload.stamp, payload.results, payload.participant_id, payload.constituency_id, db)
#     if not res:
#         return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
#     data = await crud.get_presidential_result_by_rec_id(res, db)
#     if data is not None:
#         _dict = {}
#         for item in data.items():
#             if isinstance(item[1], datetime.datetime):
#                 _dict[item[0]]=str(item[1])
#                 continue
#             _dict[item[0]] = item[1]
#         await manager.broadcast_json( {"type":"presidential_update", "data": _dict } )
#     return Response(status_code=status.HTTP_201_CREATED)


@router.post("/presidentialresults")
async def add_presidential_result(payload: schemas.PresidentialResultsCreate):
    # Call Celery task
    task = add_presidential_result_task.delay(
        payload.stamp, payload.results, payload.participant_id, payload.constituency_id
    )
    # return Response(status_code=status.HTTP_202_ACCEPTED)
    return {"task_id": task.id, "status": "Task Enqueued for processing ..."}


# @router.post("/constituencywinners")
# async def add_constituency_winner(payload: schemas.ConstituencyWinnerCreate, db: Session = Depends(get_db)):
#     res = await crud.add_constituency_winner(payload.candidate_id, payload.constituency_id, db)
#     if not res:
#         return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
#     return Response(status_code=status.HTTP_201_CREATED)

@router.post("/constituencywinners")
async def add_constituency_winner(payload: schemas.ConstituencyWinnerCreate):
    # Call Celery task
    task = add_constituency_winner_task.delay(payload.candidate_id, payload.constituency_id)
    # return Response(status_code=status.HTTP_202_ACCEPTED)
    return {"task_id": task.id, "status": "Task Enqueued for processing ..."}

# @router.post("/incidents")
# async def add_incident(payload: schemas.IncidentCreate, db: Session = Depends(get_db)):
#     res = await crud.add_incident(payload.participant_id, payload.polling_station_id, payload.report, payload.stamp, payload.description, payload.constituency_id, db)
#     if not res:
#         return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
    
#     return Response(status_code=status.HTTP_201_CREATED)

@router.post("/incidents")
async def add_incident(payload: schemas.IncidentCreate):
    # Call Celery task
    task = add_incident_task.delay(
        payload.participant_id, payload.polling_station_id, payload.report,
        payload.stamp, payload.description, payload.constituency_id
    )
    # return Response(status_code=status.HTTP_202_ACCEPTED)
    return {"task_id": task.id, "status": "Task Enqueued for processing ..."}

#  PUT

# @router.put("/results/{rec_id}/parliamentary")
# async def update_parliamentary_result(rec_id: int, db: Session = Depends(get_db)):
#     res = await crud.update_parliamentary_result(rec_id, db)
#     if not res:
#         return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
#     data = await crud.get_parliamentary_result_by_rec_id(rec_id, db)
#     if data is not None:
#         _dict = {}
#         for item in data.items():
#             if isinstance(item[1], datetime.datetime):
#                 _dict[item[0]]=str(item[1])
#                 continue
#             _dict[item[0]] = item[1]
#         await manager.broadcast_json( {"type":"parliamentary_update_delete", "data": _dict } )
#     return Response(status_code=status.HTTP_200_OK)

@router.put("/results/{rec_id}/parliamentary")
async def update_parliamentary_result(rec_id: int):
    # Call Celery task for updating parliamentary results
    task = update_parliamentary_result_task.delay(rec_id)
    # return Response(status_code=status.HTTP_202_ACCEPTED)
    return {"task_id": task.id, "status": "Task Enqueued for processing ..."}



# @router.put("/results/{rec_id}/presidential")
# async def toggle_presidential_results(rec_id: int, db: Session = Depends(get_db)):
#     res = await crud.toggle_presidential_results(rec_id, db)
#     if not res:
#         return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
#     data = await crud.get_presidential_result_by_rec_id(rec_id, db)
#     if data is not None:
#         _dict = {}
#         for item in data.items():
#             if isinstance(item[1], datetime.datetime):
#                 _dict[item[0]]=str(item[1])
#                 continue
#             _dict[item[0]] = item[1]
#         await manager.broadcast_json( {"type":"presidential_update_delete", "data": _dict } )
#     return Response(status_code=status.HTTP_200_OK)

@router.put("/results/{rec_id}/presidential")
async def toggle_presidential_results(rec_id: int):
    # Call Celery task
    task = toggle_presidential_results_task.delay(rec_id)
    # return Response(status_code=status.HTTP_202_ACCEPTED)
    return {"task_id": task.id, "status": "Task Enqueued for processing ..."}

# @router.put("/reporters")
# async def update_reporter(payload: schemas.UpdateReporter, db: Session = Depends(get_db)):
#     res = await crud.update_reporter(payload.rec_id, payload.phone_number, payload.gender, payload.constituency_id, payload.name, db)
#     if not res:
#         return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
#     return Response(status_code=status.HTTP_200_OK)

@router.put("/reporters")
async def update_reporter(payload: schemas.UpdateReporter):
    # Call Celery task
    task = update_reporter_task.delay(
        payload.rec_id, payload.phone_number, payload.gender,
        payload.constituency_id, payload.name
    )
    # return Response(status_code=status.HTTP_202_ACCEPTED)
    return {"task_id": task.id, "status": "Task Enqueued for processing ..."}

# @router.post("/presidentialresults/{id}/confirm")
# async def confirm_presidential_results(id: int, db: Session = Depends(get_db)):
#     res = await crud.confirm_presidential_results(id, db)
#     if not res:
#         return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
#     return Response(status_code=status.HTTP_200_OK)

@router.post("/presidentialresults/{id}/confirm")
async def confirm_presidential_results(id: int):
    # Call Celery task
    task = confirm_presidential_result_task.delay(id)
    # return Response(status_code=status.HTTP_202_ACCEPTED)
    return {"task_id": task.id, "status": "Task Enqueued for processing ..."}

@router.post("/parliamentaryresults/{id}/confirm")
async def confirm_parliamentary_results(id: int):
    # Call Celery task for confirming parliamentary results
    task = confirm_parliamentary_result_task.delay(id)
    return {"task_id": task.id, "status": "Task Enqueued for processing ..."}
    # return Response(status_code=status.HTTP_202_ACCEPTED)


# @router.put("/incidents/{id}/toggle", status_code=status.HTTP_200_OK)
# async def confirm_incident(id: int, db: Session = Depends(get_db)):
#     res = await crud.confirm_incident(id, db)
#     if not res:
#         return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
#     data = await crud.get_incidents_by_rec_id(res, db)
#     if data is not None:
#         _dict = {}
#         for item in data.items():
#             if isinstance(item[1], datetime.datetime):
#                 _dict[item[0]]=str(item[1])
#                 continue
#             _dict[item[0]] = item[1]
#         await manager.broadcast_json( {"type":"incident_update", "data": _dict } )
#     return Response(status_code=status.HTTP_200_OK)

# PUT endpoint to confirm an incident
@router.put("/incidents/{id}/toggle", status_code=status.HTTP_202_ACCEPTED)
async def confirm_incident(id: int):
    # Trigger Celery task to confirm the incident asynchronously
    task = confirm_incident_task.delay(id)
    # return Response(status_code=status.HTTP_202_ACCEPTED)
    return {"task_id": task.id, "status": "Task Enqueued for processing ..."}


# @router.put("/reporters")
# async def update_reporter(payload: schemas.UpdateReporter, db: Session = Depends(get_db)):
#     res = await crud.update_reporter(payload.rec_id, payload.phone_number, payload.gender, payload.constituency_id, payload.name, db)
#     if not res:
#         return Response(status_code=status.HTTP_417_EXPECTATION_FAILED)
#     return Response(status_code=status.HTTP_200_OK)



# 