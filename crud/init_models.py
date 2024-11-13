from domains.users.models.users import Base
from domains.auth.models.auth import Base
from config.session import engine
from sqlalchemy import text


# def create_tables():
#     Base.metadata.create_all(bind=engine)

# List all schemas required by the models here
required_schemas = ["aiti"]

def create_schema_if_not_exists(engine, schema_name):
    """
    Creates the specified schema if it does not already exist.
    """
    with engine.connect() as connection:
        connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))
        connection.commit()

def create_tables():
    # First, ensure all required schemas are created
    for schema in required_schemas:
        create_schema_if_not_exists(engine, schema)

    # Now, create tables in the defined schemas
    Base.metadata.create_all(bind=engine)
    