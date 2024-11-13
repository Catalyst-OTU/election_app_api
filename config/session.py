from google.cloud.sql.connector import Connector,IPTypes
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy import create_engine,MetaData
from config.settings import Settings
import sqlalchemy 
import pg8000
from _sockets import ConnectionManager
import psycopg2
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


SQLALCHEMY_DATABASE_URL = Settings.SQLALCHEMY_DATABASE_URL
INSTANCE_CONNECTION_NAME = Settings.INSTANCE_CONNECTION_NAME

ASYNC_DATABASE_URL = Settings.SQLALCHEMY_ASYNC_DATABASE_URL  # New async URL
async_engine = create_async_engine(Settings.SQLALCHEMY_ASYNC_DATABASE_URL)
async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

async def get_async_db():
    """This manages the database session with async support and caching."""
    async with async_session() as session:
        yield session


manager = ConnectionManager()

if INSTANCE_CONNECTION_NAME is not None:
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=Settings.POSTGRES_USER,
            password=Settings.POSTGRES_PASSWORD,
            db=Settings.POSTGRES_DB,
            ip_type=IPTypes.PUBLIC,
        )
        return conn
    
    engine = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()

Base = declarative_base()

database = SQLALCHEMY_DATABASE_URL
    
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base.query = session.query_property()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()





# # Function to get the database connection
# def get_db_connection():
#     conn = psycopg2.connect(
#         host=Settings.POSTGRES_SERVER,
#         port=Settings.POSTGRES_PORT,
#         dbname=Settings.POSTGRES_DB,
#         user=Settings.POSTGRES_USER,
#         password=Settings.POSTGRES_PASSWORD
#     )
#     return conn