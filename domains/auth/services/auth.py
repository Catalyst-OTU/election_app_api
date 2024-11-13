from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.hash import pbkdf2_sha256 as sha256
from domains.users.models.users import User, Reporter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta
from domains.auth.models import auth as models
from domains.users.schemas import users as schemas
from config.session import get_db
import sqlalchemy
import utils
import sys

logger = utils.get_logger()

async def revoke_token(token: str, db: Session):
    revoke_token = models.RevokedToken(jti=token)
    try:
        db.execute(text("""SET search_path TO aiti"""))
        db.add(revoke_token)
        db.commit()
        db.close()
        return True
    except:
        db.rollback()
        db.close()
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        return False
    


# def get_user_by_phone_number(phone_number: str, db: Session):
#         return db.query(User).filter(phone_number==phone_number).first()
       


def verify_hash(password, hash):
        return sha256.verify(password, hash)


def authenticate_user(payload: schemas.UserBase, api_key, db: Session):
        db_user = db.query(User).filter(User.phone_number==payload.phone_number).first()

        if api_key == "gbcapi":
            # print("phone_number:", db_user.phone_number)
            if not db_user:
                raise HTTPException(status_code=401, detail="User with phone number not found")
            if not verify_hash(payload.password, db_user.password):
                raise HTTPException(status_code=401, detail="Incorrect password")

            access_token = utils.create_access_token(data = {"phone_number":payload.phone_number}, expires_delta=timedelta(minutes=1440))
            refresh_token = utils.create_refresh_token(data = {"phone_number":payload.phone_number})

            _dict = {
                'token': access_token,
                'refresh_token': refresh_token,
                # 'rec_id': db_user.rec_id,
                'phone_number': payload.phone_number
            }

            return _dict
        
        else:
             raise HTTPException(status_code=401, detail="SP sp_user_auth could not authenticate credentials")








async def is_token_blacklisted(token, db: Session):
    db.execute(text("""SET search_path TO aiti"""))
    res = db.query(models.RevokedToken).filter(models.RevokedToken.jti == token).first()
    db.close()
    if res is not None:
        return True
    return False

async def authenticate_user2(payload: schemas.UserBase , api_key, db: Session ):
    
    if api_key == "gbcapi":
        try:
            user = db.execute(text("""select aiti.sp_admin_user_auth(:phone,:password)""",{'phone':payload.phone_number,'password':payload.password}))

            user = db.execute(text("SELECT * FROM aiti.users u WHERE u.phone_number= TRIM(payload.phone_number) AND u.password = crypt(TRIM(p_password), u.password)"))
            db.close()
        except:
            logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
            db.close()
            raise HTTPException(status_code=401, detail="SP could not authenticate credentials")
        
        user = utils.synthesize_r_proxy(user)
        user = user.replace('(','')
        user = user.replace(')','')
        user = user.split(',')
        
        if len(user[0]) < 1:
            logger.warning("status_code=401/404, detail='reporter not found'")
            raise HTTPException(status_code=401, detail="back office user not found")
        
        access_token = utils.create_access_token(data = {"phone_number":payload.phone_number}, expires_delta=timedelta(minutes=1440))
        refresh_token = utils.create_refresh_token(data = {"phone_number":payload.phone_number})

        _dict = {
            'token': access_token,
            'refresh_token': refresh_token,
            'rec_id': user[2],
            'phone_number': payload.phone_number
        }
        
        return _dict    

    try:
        user = db.execute(text("""select aiti.sp_user_auth(:phone,:password)""",{'phone':payload.phone_number,'password':payload.password}))
        db.close()
    except:
        logger.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
        db.close()
        raise HTTPException(status_code=401, detail="SP sp_user_auth could not authenticate credentials")
    
    user = utils.synthesize_r_proxy(user)
    user = user.replace('(','')
    user = user.replace(')','')
    user = user.split(',')

    if len(user[0]) < 1:
        logger.warning("status_code=401/404, detail='reporter not found'")
        raise HTTPException(status_code=401, detail="reporter not found")

    access_token = utils.create_access_token(data = {"phone":payload.phone_number}, expires_delta=timedelta(minutes=1440))
    refresh_token = utils.create_refresh_token(data = {"phone":payload.phone_number})

    _dict = {
        'token': access_token,
        'refresh_token': refresh_token,
        'rec_id': int(user[0]),
        'phone_number': user[2],
        'constituency_id': int(user[4])
    }

    if int(user[4]) > 0:
        polling_stations = db.execute(text("""SELECT * FROM aiti.vw_polling_station where constituency_id=:constituency_id""",{'constituency_id':int(user[4])}))
        parliamentarians = db.execute(text("""SELECT * FROM aiti.parliamentary where constituency_id=:constituency_id""",{'constituency_id':int(user[4])}))
        _dict.update({'polling_stations': [dict(row) for row in polling_stations], 'parliamentarians': [dict(row) for row in parliamentarians]})
    # else:
    constituencies = db.execute(text("""SELECT * FROM aiti.vw_constituency"""))
    _dict.update({'constituencies': [dict(row) for row in constituencies]})

    db.close()

    return _dict
    
    