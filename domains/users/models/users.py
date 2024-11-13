from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date
from sqlalchemy.orm import relationship, backref
from passlib.hash import pbkdf2_sha256 as sha256
from config.session import Base, SessionLocal
import datetime

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'aiti'}

    rec_id = Column(Integer , autoincrement=True, primary_key=True)
    password = Column(String, nullable = False)
    phone_number = Column(String, unique = True, nullable = False)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def find_by_phone(cls, phone_number):
        return cls.query.filter_by(phone_number = phone_number).first()


class Reporter(Base):
    __tablename__ = "reporters"
    __table_args__ = {'schema': 'aiti'}

    rec_id = Column(Integer, autoincrement=True, primary_key=True)
    reporter_name = Column(String, nullable = False)
    phone_number= Column(String, unique = True, nullable = False)
    gender = Column(String, nullable = False)
    constituency_id = Column(Integer)
    apollo_polling_station_id = Column(String)
    status = Column(String, nullable = False)

    # , ForeignKey('constituency.rec_id')
    # @classmethod
    # def find_by_phone(cls, phone_number):
    #     return cls.query.filter_by(phone_number = phone_number).first()
