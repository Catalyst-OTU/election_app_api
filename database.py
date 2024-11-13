from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from databases import Database
import os

POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_DB: str = os.getenv("POSTGRES_DB", "gbc_db")

#SQLALCHEMY_DATABASE_URL = os.environ.get('DATABASE_URI') or 'postgres://postgres@postgres:5432/{}'.format(os.environ.get('DATABASE_NAME'))

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()

Base = declarative_base()

database = SQLALCHEMY_DATABASE_URL
#database = Database(SQLALCHEMY_DATABASE_URL)

