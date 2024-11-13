from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
import sqlalchemy
import utils
import sys
import psycopg2
from sqlalchemy import text

logger = utils.get_logger()

# READ

async def get_region(db: Session):
    try:
        res = db.execute(text("""SELECT aiti.sp_region_find()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_constituency(db: Session):
    try:
        res = db.execute(text("""select * from aiti.sp_get_all_constituencies()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)   

async def get_all_incidents(db: Session):
    try:
        res = db.execute(text("""select * from aiti.sp_get_all_incidents()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)   

async def get_all_constituency_winners(db: Session):
    try:
        res = db.execute(text("""select * from aiti.sp_get_all_constituency_winners()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)  

async def get_all_parties(db: Session):
    try:
        res = db.execute(text("""select * from aiti.get_all_parties()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)  

async def get_all_candidates(db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_all_candidates()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_all_parliamentarians(db: Session):
    try:
        res = db.execute(text("""select * from aiti.sp_get_all_parliamentarians()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_national_presidential_aggregations(db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_national_pres_agg()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)





async def get_past_regional_results(db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_past_regional_results()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)





async def get_past_regional_results_for_2020(db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_past_regional_results_2020()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)






async def get_past_regional_results_for_2016(db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_past_regional_results_2016()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)




async def get_past_national_results(db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_past_national_results()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_past_constituency_results(db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_past_constituency_results()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_national_pres_polling_station_agg(db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_national_pres_polling_station_agg()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_parliamentary_result(id, db: Session):
    try:
        res = db.execute(text("""select * from aiti.sp_get_parliamentary_result(:id)""",{'id':id}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_confirmed_parliamentary_result(id, db: Session):
    try:
        res = db.execute(text("""select * from aiti.sp_confirm_parliamentary_result(:id)""",{'id':id}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_constituency_by_code(code, db: Session):
    try:
        res = db.execute(text("""select * from aiti.sp_constituency(:code)""",{'code':code}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_polling_station(code, db: Session):
    try:
        res = db.execute(text("""select * from aiti.sp_polling_station(:code)""",{'code':code}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_const_parliamentarians(ps_code, db: Session):
    try:
        res = db.execute(text("""select * from aiti.sp_get_const_parliamentarians(:ps_code)""",{'ps_code':ps_code}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_incidents(constituency_id, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_incidents(:constituency_id)""",{'constituency_id':constituency_id}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_reg_pres_polling_station_agg(region, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_reg_pres_polling_station_agg(:region)""",{'region':region}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_reg_pres_agg(region, db: Session):
    try:
        res = db.execute(text("""select * from aiti.sp_get_reg_pres_agg(:region)""",{'region':region}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_presidential_result(constituency_id, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_presidential_result(:constituency_id)""",{'constituency_id':constituency_id}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_polling_siblings(polling_station_id, db: Session):
    try:
        res = db.execute(text("""select * from aiti.sp_polling_sibs(:polling_station_id)""",{'polling_station_id':polling_station_id}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_constituency_reporters(constituency_name, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_reporters(:constituency_name)""",{'constituency_name':constituency_name}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_presidential_result_aggregations(constituency_name, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_presidential_result_agg(:constituency_name)""",{'constituency_name':constituency_name}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_constituency_pres_polling_station_agg(constituency_name, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_get_constituency_pres_polling_station_agg(:constituency_name)""",{'constituency_name':constituency_name}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_candidate_by_constituency_id(constituency_id, db):
    try:
        res = db.execute(text("""SELECT (SELECT json_agg(w) FROM (select * from aiti.vw_polling_station where constituency_id = :constituency_id ) as w) AS polling_stations ,(SELECT json_agg(p) FROM (select rec_id, region, constituency_name, name_of_candidate, party_affiliation, sex, constituency_id from aiti.vw_paliamentary where constituency_id = :constituency_id ) as p) AS parliamentarians;""",{'constituency_id':constituency_id}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return res.fetchone()

async def get_incidents_by_rec_id(id, db):
    try:
        res = db.execute(text("""select * from aiti.vw_get_incidents where rec_id=:id""",{'id':id}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return res.first()
    # return utils.synthesize_r_proxy(res)

async def get_incidents_to_update(constituency_id, db):
    try:
        res = db.execute(text("""select aiti.sp_get_incidents_to_update(:constituency_id)""",{'constituency_id':constituency_id}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return res.fetchall()

async def get_past_parliamentary_constituencies(db):
    try:
        res = db.execute(text("""select * from aiti.sp_get_past_parliamentary_constituency()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_past_parliamentary_regional(db):
    try:
        res = db.execute(text("""select * from aiti.sp_get_past_parliamentary_regional()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_past_parliamentary_national(db):
    try:
        res = db.execute(text("""select * from aiti.sp_get_past_parliamentary_national()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_2016_parliamentary_results(db):
    try:
        res = db.execute(text("""select * from aiti.sp_get_2016_parliamentary_results()"""))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def get_presidential_result_by_rec_id(rec_id, db):
    try:
        res = db.execute(text("""SELECT * FROM aiti.presidential_result where rec_id=:rec_id""",{'rec_id':rec_id}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return res.first()

async def get_parliamentary_result_by_rec_id(rec_id, db):
    try:
        res = db.execute(text("""SELECT * FROM aiti.parliamentary_result where rec_id=:rec_id""",{'rec_id':rec_id}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return res.first()

# CREATE

async def add_parliamentary_result(stamp, results, participant_id, constituency_id, db: Session):
    rslts = utils.stringify_json(results)
    stamp = utils.timestamp_to_datetime(stamp)
    try:
        res = db.execute(text("""select aiti.sp_add_parliamentary_result(:stamp,:rslts,:participant_id,:constituency_id)""",{'stamp':stamp,'rslts':rslts, 'participant_id':participant_id, 'constituency_id':constituency_id}))
        db.commit()
        db.close()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="something went wrong {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def add_polling_station_result(stamp, results, participant_id, polling_station_id, constituency_id, db: Session):
    rslts = utils.stringify_json(results)
    stamp = utils.timestamp_to_datetime(stamp)
    try:
        res = db.execute(text("""select aiti.sp_add_polling_station_result(:stamp,:rslts,:participant_id,:polling_station_id,:constituency_id)""",{'stamp':stamp, 'rslts':rslts, 'participant_id':participant_id, 'polling_station_id':polling_station_id,'constituency_id':constituency_id}))
        db.commit()
        db.close()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="something went wrong {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def add_presidential_result(stamp, results, participant_id, constituency_id, db: Session):
    rslts = utils.stringify_json(results)
    stamp = utils.timestamp_to_datetime(stamp)

    try:
        res = db.execute(text("""select aiti.sp_add_presidential_result(:stamp,:rslts,:participant_id,:constituency_id)""",{'stamp':stamp,'rslts':rslts,'participant_id':participant_id,'constituency_id':constituency_id}))
        db.commit()
        db.close()
    
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="something went wrong {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def add_constituency_winner(candidate_id, constituency_id, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_add_constituency_winner(:candidate_id,:constituency_id)""",{'candidate_id':candidate_id,'constituency_id':constituency_id}))
        db.commit()
        db.close()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="something went wrong {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def add_incident(participant_id, polling_station_id, report, stamp, description, constituency_id, db: Session):
    rslts = utils.stringify_array_json(report)
    stamp = utils.timestamp_to_datetime(stamp)

    try:
        res = db.execute(text("""select aiti.sp_incident_add(:participant_id, :polling_station_id, :rslts, :stamp, :description, :constituency_id )""", {'participant_id':participant_id, 'polling_station_id':polling_station_id, 'rslts':rslts, 'stamp':stamp, 'description':description, 'constituency_id':constituency_id}))
        db.commit()
        db.close()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="something went wrong {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

# UPDATE

async def update_parliamentary_result(rec_id, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_update_parliamentary_result_2(:rec_id)""",{'rec_id':rec_id}))
        db.commit()
        db.close()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def update_reporter(rec_id, phone_number, gender, constituency_id, name, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_update_reporter(:rec_id,:phone_number,:gender,:constituency_id,:name)""",{'rec_id':rec_id, 'phone_number':phone_number, 'gender':gender, 'constituency_id':constituency_id, 'name':name}))
        db.commit()
        db.close()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def confirm_presidential_results(id, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_confirm_presidential_result(:id)""",{'id':id}))
        db.commit()
        db.close()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def toggle_presidential_results(id, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_update_presidential_result_2(:id)""",{'id':id}))
        db.commit()
        db.close()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def confirm_incident(id, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_confirm_incident(:id)""",{'id':id}))
        db.commit()
        db.close()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)

async def update_reporter(rec_id, phone_number, gender, constituency_id, name, db: Session):
    try:
        res = db.execute(text("""select aiti.sp_update_reporter(:rec_id, :phone_number, :gender, :constituency_id, :name)""",{'rec_id':rec_id, 'phone_number':phone_number, 'gender':gender, 'constituency_id':constituency_id, 'name':name}))
        db.commit()
        db.close()
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=500, detail="sqlalchemy[Database] error: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    return utils.synthesize_r_proxy(res)