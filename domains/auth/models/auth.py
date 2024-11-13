from sqlalchemy import event, Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric, Date
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.orm import relationship, backref
from config.session import Base, SessionLocal
import datetime

class RefreshTokens(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    jti = Column(String)

class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    jti = Column(String)