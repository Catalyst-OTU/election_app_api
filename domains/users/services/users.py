from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from passlib.hash import pbkdf2_sha256 as sha256
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from domains.users.schemas import users as schemas
from domains.users.models import users as models
from config.session import get_db
import sqlalchemy
import utils
import sys

async def create_user(payload: schemas.UserBase , db: Session = Depends(get_db)):
    try:
        #res = db.execute("""select aiti.sp_create_user(:phone_number,:password)""",{'phone_number':payload.phone_number,'password':payload.password})
        data = models.User(
            phone_number=payload.phone_number,
            password=sha256.hash(payload.password)
        )
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
        
        # db.commit()
        # db.close()
        # return res.first().values()[0]
        # return utils.synthesize_r_proxy(res)
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        db.close()
        raise HTTPException(status_code=500, detail="something went wrong: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))
    
async def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100, search:str=None, value:str=None ):
    try:
        base = db.query(models.Reporter)
        if search and value:
            try:
                base = base.filter(models.Reporter.__table__.c[search].like("%" + value + "%"))
            except KeyError:
                return base.offset(skip).limit(limit).all()
        return base.offset(skip).limit(limit).all()
    except:
        raise HTTPException(status_code=500, detail="{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]) )

async def create_reporter(payload: schemas.Reporter , db: Session = Depends(get_db)):
    try:
        #res = db.execute("""select aiti.sps_register_user(:name,:phone,:password,:gender,:constituency_id)""",{'name':payload.reporter_name,'phone':payload.phone_number,'password':payload.password,'gender':payload.gender,'constituency_id':payload.constituency_id})
       

        reporter_data = models.Reporter(
            phone_number=payload.phone_number,
            reporter_name=payload.reporter_name,
            gender=payload.gender,
            constituency_id=payload.constituency_id
        )
        
        db.add(reporter_data)
        db.commit()
        db.refresh(reporter_data)


        user_data = models.User(
            phone_number=payload.phone_number,
            password=sha256.hash(payload.password)
        )
        db.add(user_data)
        db.commit()
        db.refresh(user_data)
        
        return reporter_data
        # db.commit()
        # db.close()
        # return res.first().values()[0]
    except sqlalchemy.exc.IntegrityError:
        db.rollback()
        db.close()
        raise HTTPException(status_code=409, detail="sqlalchemy[Database] error: unique_violation")
    except:
        db.rollback()
        db.close()
        raise HTTPException(status_code=500, detail="something went wrong: {}:{}".format(sys.exc_info()[0], sys.exc_info()[1]))

# db.execute("SET search_path TO aiti")

# user = db.query(models.User).filter(models.User.phone_number == payload.phone_number).first()

# if user:
#     raise HTTPException(status_code=409, detail="user with phone already exists")

# new_user = models.User(password=models.User.generate_hash(payload.password), phone_number=payload.phone_number)

# try:
    
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user) 
#     db.close()

#     return new_user

# except IntegrityError:
#     db.rollback()
#     raise HTTPException(status_code=409, detail="record conflicts")

# except:
#     db.rollback()
#     raise HTTPException(status_code=500, detail="something went wrong")

   # h =  res.first()
    # print(type(h))
    # print(dir(h))
    # print(h)
    # print(dir(res.first()))
    # print(type(res.first().values()[0]))
    # print(type(h.first()))
        # a = tuple(res.fetchall()[0])
        # print(tuple(a))
        # print(a[0])
        # return utils.synthesize_r_proxy(res)