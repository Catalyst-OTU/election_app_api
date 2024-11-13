# tasks.py
import re
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError, InternalError, DatabaseError
from celery import Celery, current_task
from config.session import SQLALCHEMY_DATABASE_URL, SessionLocal, engine
import sqlparse
from celery_worker import celery_app
import asyncpg
from sqlparse import format as sql_format, split as sql_split, parse as sql_parse
from psycopg2.extras import execute_values
from _sockets import ConnectionManager




manager = ConnectionManager()



def correct_insert_values(match):
    values = match.group(1)
    key_value_pairs = re.findall(r'"([^"]+)"\s*:\s*([^,]+)', values)
    if not key_value_pairs:
        logging.warning(f"No key-value pairs found: {values}")
        return match.group(0)
    
    transformed_values = [f"'{key}: {value.strip()}'" for key, value in key_value_pairs]
    return f"VALUES ({', '.join(transformed_values)})"


def split_sql_statements(content: str):
    # Use sql_split to split the content into individual statements
    statements = sqlparse.split(content)
    return [stmt.strip() for stmt in statements if stmt.strip()]


def convert_copy_from_stdin_corrected(sql_text):
    # Find all COPY FROM stdin blocks
    pattern = r"(COPY\s+[^\n]+FROM\s+stdin;)(.*?)(\\\.)"
    matches = re.finditer(pattern, sql_text, flags=re.DOTALL)

    for match in matches:
        copy_statement = match.group(1)  # COPY ... FROM stdin;
        data_rows = match.group(2).strip()  # Data rows in the COPY statement
        end_marker = match.group(3)  # End marker for the COPY section (\.)
        
        # Extract table name and columns from the COPY statement
        table_name_match = re.search(r'COPY\s+(\w+\.\w+)\s+\(([^)]+)\)', copy_statement)
        if table_name_match:
            table = table_name_match.group(1)  # Table name (schema.table format)
            columns = table_name_match.group(2)  # Column names
            
            # Prepare INSERT statements for each row
            rows = []
            for row in data_rows.splitlines():
                # Process each value: replace "\N" with NULL and escape single quotes
                values = []
                for val in row.split("\t"):
                    if val == '\\N':
                        values.append('NULL')
                    else:
                        escaped_val = val.replace("'", "''")
                        values.append(f"'{escaped_val}'")
                rows.append(f"({', '.join(values)})")
            
            # Combine all rows into a single INSERT statement
            insert_statements = f"INSERT INTO {table} ({columns}) VALUES {', '.join(rows)};\n"
            
            # Replace the COPY block with the INSERT statements
            sql_text = sql_text.replace(f"{copy_statement}{data_rows}\n\\.", insert_statements)
    
    return sql_text


def transform_sql_to_postgresql(statement: str) -> str:
    try:
        # if statement.strip().startswith("COPY") and "FROM stdin" in statement:
        #     return convert_copy_from_stdin_corrected(statement)

        # Schema, table, and function existence checks
        if re.match(r"CREATE SCHEMA", statement, re.IGNORECASE):
            schema_name = re.search(r'CREATE SCHEMA\s+"?(\w+)"?', statement, re.IGNORECASE).group(1)
            statement = (
                f"DO $$ BEGIN "
                f"IF NOT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = '{schema_name}') THEN "
                f"{statement.strip()}; "
                f"END IF; "
                f"END $$;"
            )
        elif re.match(r"CREATE TABLE", statement, re.IGNORECASE):
            table_name_match = re.search(r'CREATE TABLE\s+"?(\w+)"?\."?(\w+)"?', statement, re.IGNORECASE)
            if table_name_match:
                schema_name, table_name = table_name_match.groups()
                statement = (
                    f"DO $$ BEGIN "
                    f"IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = '{schema_name}' AND table_name = '{table_name}') THEN "
                    f"{statement.strip()}; "
                    f"END IF; "
                    f"END $$;"
                )
        elif re.match(r"CREATE FUNCTION", statement, re.IGNORECASE):
            func_name_match = re.search(r'CREATE FUNCTION\s+"?(\w+)"?\."?(\w+)"?', statement, re.IGNORECASE)
            if func_name_match:
                schema_name, func_name = func_name_match.groups()
                statement = (
                    f"DO $$ BEGIN "
                    f"IF NOT EXISTS (SELECT 1 FROM pg_proc p JOIN pg_namespace n ON p.pronamespace = n.oid "
                    f"WHERE p.proname = '{func_name}' AND n.nspname = '{schema_name}') THEN "
                    f"{statement.strip()}; "
                    f"END IF; "
                    f"END $$;"
                )
        
        # General transformations
        statement = re.sub(r"`", r'"', statement)  # Convert backticks to double quotes
        statement = re.sub(r"(?i)\bAUTO_INCREMENT\b", "SERIAL", statement, flags=re.IGNORECASE)
        statement = re.sub(r",\s*\)", ")", statement)  # Remove trailing commas before closing parenthesis
        statement = re.sub(r"\bVALUES\s*\(([^)]+)\)", correct_insert_values, statement, flags=re.IGNORECASE)
        statement = re.sub(r"\);?\s*$", ");", statement.strip())  # Ensure statements end with a semicolon
        statement = re.sub(r'BEGIN\s+/', 'BEGIN;', statement, flags=re.IGNORECASE)  # Correct BEGIN block
        statement = re.sub(r'END\s+/', 'END;', statement, flags=re.IGNORECASE)  # Correct END block
        statement = re.sub(r"(?i)\bDELIMITER\s+//", "", statement)  # Remove DELIMITER directives
        statement = re.sub(r"(?i)\bDELIMITER\s*;", "", statement)  # Normalize statement end delimiter
        statement = re.sub(r"\\N", "NULL", statement)  # Replace \N with NULL
        statement = re.sub(r"(?i)\bSHOW\s+WARNINGS\b", "-- SHOW WARNINGS not supported in PostgreSQL", statement)

        logging.info(f"Transformed SQL: {statement}")
        return statement
    
    except Exception as e:
        logging.error(f"Error in SQL transformation: {e}")
        raise

@celery_app.task(bind=True)
async def execute_sql_task(self, file_content: str):
    statements = split_sql_statements(file_content)
    transformed_statements = []
    execution_errors = []

    await manager.notify_start(task_id)  # Notify start of execution
    for statement in statements:
        try:
            transformed_statement = transform_sql_to_postgresql(statement)
            stat = transformed_statement
            if statement.strip().startswith("COPY") and "FROM stdin":
                transformed_statement = convert_copy_from_stdin_corrected(stat)
            transformed_statements.append(transformed_statement)
        except Exception as transform_err:
            error_message = f"Error transforming statement: {transform_err}. Original SQL: {statement}"
            logging.error(error_message)
            execution_errors.append(error_message)

    if execution_errors:
        error_log = "\n".join(execution_errors)
        logging.error(f"Transformation finished with errors:\n{error_log}")
        return {"status": "failed", "errors": execution_errors}
    
    with engine.connect() as connection:
        for transformed_statement in transformed_statements:
            try:
                with connection.begin():
                    connection.execute(text(transformed_statement))
                    await manager.notify_completion(task_id, "migration successful")
            except (ProgrammingError, InternalError, DatabaseError) as exec_err:
                error_message = f"Error executing statement: {exec_err}. SQL: {transformed_statement}"
                logging.error(error_message)
                execution_errors.append(error_message)
                await manager.notify_completion(task_id, "migration failed:\n")

    if execution_errors:
        error_log = "\n".join(execution_errors)
        logging.error(f"Execution finished with errors:\n{error_log}")
        return {"status": "completed_with_errors", "errors": execution_errors}
        
    
    return {"status": "success", "message": "SQL file executed successfully."}


# @celery_app.task(bind=True)
# def execute_copy_only_task(self, file_content: str):
#     execution_errors = []

#     # Identify and transform only COPY statements
#     transformed_content = convert_copy_to_insert(file_content)
    
#     with engine.connect() as connection:
#         try:
#             with connection.begin():
#                 connection.execute(text(transformed_content))
#         except (ProgrammingError, InternalError, DatabaseError) as exec_err:
#             error_message = f"Error executing COPY transformed content: {exec_err}"
#             logging.error(error_message)
#             execution_errors.append(error_message)

#     if execution_errors:
#         error_log = "\n".join(execution_errors)
#         logging.error(f"Execution finished with errors:\n{error_log}")
#         return {"status": "completed_with_errors", "errors": execution_errors}
    
#     return {"status": "success", "message": "COPY commands executed successfully."}








######################################################################
######################################################################

# @celery_app.task(bind=True)
# def execute_sql_task(self, file_content: str):
#     statements = split_sql_statements(file_content)
#     transformed_statements = []
#     execution_errors = []

#     # Step 1: Transform each statement and store it for later execution
#     for statement in statements:
#         try:
#             transformed_statement = transform_sql_to_postgresql(statement)
#             transformed_statements.append(transformed_statement)
#         except Exception as transform_err:
#             error_message = f"Error transforming statement: {transform_err}. Original SQL: {statement}"
#             logging.error(error_message)
#             execution_errors.append(error_message)

#     # If there were transformation errors, do not proceed to execution
#     if execution_errors:
#         error_log = "\n".join(execution_errors)
#         logging.error(f"Transformation finished with errors:\n{error_log}")
#         return {"status": "failed", "errors": execution_errors}
    
#     # Step 2: Execute each transformed statement sequentially
#     with engine.connect() as connection:
#         for transformed_statement in transformed_statements:
#             if isinstance(transformed_statement, dict) and transformed_statement.get("type") == "COPY":
#                 # Process the COPY statement for bulk insert
#                 table_name = transformed_statement["table_name"]
#                 columns = transformed_statement["columns"]
#                 data_rows = transformed_statement["data"].splitlines()

#                 # Prepare data rows by converting to tuples, skipping invalid rows
#                 records = []
#                 for row in data_rows:
#                     try:
#                         if row.strip() and not row.startswith("\\."):
#                             row_values = tuple(
#                                 None if val == "\\N" else val.strip() for val in row.split("\t")
#                             )
#                             if len(row_values) == len(columns):
#                                 records.append(row_values)
#                             else:
#                                 error_message = f"Column mismatch for table {table_name}. Row: {row_values}"
#                                 logging.error(error_message)
#                                 execution_errors.append(error_message)
#                     except Exception as row_err:
#                         logging.error(f"Error processing row: {row}. Error: {row_err}")
#                         execution_errors.append(f"Error processing row: {row}. Error: {row_err}")

#                 print("records:: ", records)
#                 # Insert data using psycopg2's execute_values for bulk insert
#                 if records:
#                     try:
#                         with psycopg2.connect(SQLALCHEMY_DATABASE_URL) as pg_conn:
#                             with pg_conn.cursor() as cursor:
#                                 insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
#                                 execute_values(cursor, insert_sql, records)
#                                 pg_conn.commit()
#                     except Exception as exec_err:
#                         error_message = f"Error executing COPY data for table {table_name}: {exec_err}"
#                         logging.error(error_message)
#                         execution_errors.append(error_message)
#             else:
#                 # Execute the regular SQL statement
#                 try:
#                     with connection.begin():
#                         connection.execute(text(transformed_statement))
#                 except (ProgrammingError, InternalError, DatabaseError) as exec_err:
#                     error_message = f"Error executing statement: {exec_err}. SQL: {transformed_statement}"
#                     logging.error(error_message)
#                     execution_errors.append(error_message)

#     # Return or log all accumulated errors
#     if execution_errors:
#         error_log = "\n".join(execution_errors)
#         logging.error(f"Execution finished with errors:\n{error_log}")
#         return {"status": "completed_with_errors", "errors": execution_errors}
    
#     return {"status": "success", "message": "SQL file executed successfully."}



# def transform_json_strings_in_copy(statement: str) -> str:
#     # Pattern to match JSON-like key-value pairs in COPY statement
#     json_pattern = r'{(.*?)}'
    
#     def wrap_json_key_value_pairs(match):
#         json_content = match.group(1)
#         # Ensure key-value pairs are properly wrapped in quotes
#         transformed_json = re.sub(r'(\b[a-zA-Z0-9_]+\b):\s*([0-9]+)', r'"\1": \2', json_content)
#         return f'{{{transformed_json}}}'
    
#     # Transform all JSON-like key-value pairs in the statement
#     return re.sub(json_pattern, wrap_json_key_value_pairs, statement)


################################################ @celery_app.task(bind=True)
# def execute_sql_task(self, file_content: str):
#     statements = split_sql_statements(file_content)
#     transformed_statements = []
#     execution_errors = []
#     line = 0
#     # Step 1: Transform each statement and store it for later execution
#     for statement in statements:
#         try:
#             transformed_statement = transform_sql_to_postgresql(statement)
#             transformed_statements.append(transformed_statement)
#             print(f"Transformed statement line {++line}. {transformed_statement}\n")
#         except Exception as transform_err:
#             error_message = f"Error transforming statement: {transform_err}. Original SQL: {statement}"
#             print("\n Error occurred during transformation: ", error_message)
#             logging.error(error_message)
#             execution_errors.append(error_message)
#             print("'n'nentire error log from transformation: ", execution_errors)

#     # If there were transformation errors, do not proceed to execution
#     if execution_errors:
#         error_log = "\n".join(execution_errors)
#         logging.error(f"Transformation finished with errors:\n{error_log}")
#         return {"status": "failed", "errors": execution_errors}
    
#     # Step 2: Execute each transformed statement sequentially
#     with engine.connect() as connection:
#         for transformed_statement in transformed_statements:
#             if isinstance(transformed_statement, dict) and transformed_statement.get("type") == "COPY":
#                 # Process the COPY statement for bulk insert
#                 table_name = transformed_statement["table_name"]
#                 columns = transformed_statement["columns"]
#                 data_rows = transformed_statement["data"].splitlines()

#                 # Convert data rows to list of tuples
#                 records = [
#                     tuple(row.split("\t")) for row in data_rows if row.strip() and not row.startswith("\\.")
#                 ]

#                 try:
#                     with connection.begin():
#                         connection.execute(
#                             text(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES :data"),
#                             {"data": records}
#                         )
#                 except (ProgrammingError, InternalError, DatabaseError) as exec_err:
#                     error_message = f"Error executing COPY data for table {table_name}: {exec_err}"
#                     logging.error(error_message)
#                     execution_errors.append(error_message)
#             else:
#                 # Execute the regular SQL statement
#                 try:
#                     with connection.begin():
#                         connection.execute(text(transformed_statement))
#                 except (ProgrammingError, InternalError, DatabaseError) as exec_err:
#                     error_message = f"Error executing statement: {exec_err}. SQL: {transformed_statement}"
#                     logging.error(error_message)
#                     execution_errors.append(error_message)

#     # Return or log all accumulated errors
#     if execution_errors:
#         error_log = "\n".join(execution_errors)
#         logging.error(f"Execution finished with errors:\n{error_log}")
#         return {"status": "completed_with_errors", "errors": execution_errors}
    
#     return {"status": "success", "message": "SQL file executed successfully."}

####################################8888888888888888888888888888

# @celery_app.task(bind=True)
# def execute_sql_task(self, file_content: str):
#     statements = split_sql_statements(file_content)
#     execution_errors = []  # Store errors for reporting
    
#     with engine.connect() as connection:
#         for statement in statements:
#             if not statement.strip():
#                 continue  # Skip empty statements
            
#             transformed_statement = transform_sql_to_postgresql(statement)
#             try:
#                 # Execute each statement in its own transaction
#                 with connection.begin():
#                     connection.execute(text(transformed_statement))
#             except (ProgrammingError, InternalError, DatabaseError) as stmt_err:
#                 # Log and store the error, and continue with the next statement
#                 error_message = f"Error executing statement: {stmt_err}. Statement: {transformed_statement}"
#                 logging.error(error_message)
#                 execution_errors.append(error_message)
    
#     # Return or log all accumulated errors
#     if execution_errors:
#         error_log = "\n".join(execution_errors)
#         logging.error(f"Execution finished with errors:\n{error_log}")
#         return {"status": "completed_with_errors", "errors": execution_errors}
    
#     return {"status": "success", "message": "SQL file executed successfully."}


# @celery_app.task(bind=True)
# def execute_sql_task(self, file_content: str):
#     # Step 1: Split and transform all statements before execution
#     statements = split_sql_statements(file_content)
#     transformed_statements = []
#     execution_errors = []
#     line = 0
#     # Transform each statement and store it for later execution
#     for index, statement in enumerate(statements, 1):
#         try:
#             transformed_statement = transform_sql_to_postgresql(statement)
#             transformed_statements.append(transformed_statement)
#             print(f"Transformed statement line {++line}. {transformed_statement}\n")
#         except Exception as transform_err:
#             error_message = f"Error transforming statement {index}: {transform_err}. Original SQL: {statement}"
#             print("\n Error occurred during transformation: ", error_message)
#             logging.error(error_message)
#             execution_errors.append(error_message)
#             print("'n'nentire error log from transformation: ", execution_errors)
    
#     # If there were transformation errors, do not proceed to execution
#     if execution_errors:
#         error_log = "\n".join(execution_errors)
#         logging.error(f"Transformation finished with errors:\n{error_log}")
#         return {"status": "failed", "errors": execution_errors}
    
#     # Step 2: Execute each transformed statement sequentially
#     with engine.connect() as connection:
#         for index, transformed_statement in enumerate(transformed_statements, 1):
#             try:
#                 # Execute each transformed statement in its own transaction
#                 with connection.begin():
#                     connection.execute(text(transformed_statement))
#             except (ProgrammingError, InternalError, DatabaseError) as exec_err:
#                 # Log and store the error, and continue with the next statement
#                 error_message = f"Error executing transformed statement {index}: {exec_err}. SQL: {transformed_statement}"
#                 logging.error(error_message)
#                 execution_errors.append(error_message)
    
#     # Return or log all accumulated errors
#     if execution_errors:
#         error_log = "\n".join(execution_errors)
#         logging.error(f"Execution finished with errors:\n{error_log}")
#         return {"status": "completed_with_errors", "errors": execution_errors}
    
#     return {"status": "success", "message": "SQL file executed successfully."}




#########################################################################
#########################################################################

# @celery_app.task(bind=True)
# def execute_sql_task(self, file_content: str):
#     statements = split_sql_statements(file_content)
#     with engine.connect() as connection:
#         transaction = connection.begin()
#         try:
#             for statement in statements:
#                 if statement.strip():
#                     try:
#                         transformed_statement = transform_sql_to_postgresql(statement)
#                         connection.execute(text(transformed_statement))
#                     except ProgrammingError as stmt_err:
#                         if 'DuplicateSchema' in str(stmt_err):
#                             logging.warning(f"Skipping existing schema creation: {stmt_err}")
#                             continue
#                         logging.error(f"Statement execution error: {stmt_err}")
#                         raise stmt_err
#             transaction.commit()
#             return {"status": "success", "message": "SQL file executed successfully."}
#         except Exception as e:
#             transaction.rollback()
#             raise self.retry(exc=e, countdown=5, max_retries=1)










# def transform_sql_to_postgresql(statement: str) -> str:
#     try:
#         # Parse the statement
#         parsed_statements = sql_parse(statement)
#         transformed_statements = []

#         for parsed in parsed_statements:
#             raw_statement = str(parsed).strip()  # Convert the parsed statement back to a string
            
#             # Check for CREATE SCHEMA
#             if raw_statement.upper().startswith("CREATE SCHEMA"):
#                 schema_name_match = re.search(r'CREATE SCHEMA\s+"?(\w+)"?', raw_statement, re.IGNORECASE)
#                 if schema_name_match:
#                     schema_name = schema_name_match.group(1)
#                     raw_statement = (
#                         f"DO $$ BEGIN "
#                         f"IF NOT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = '{schema_name}') THEN "
#                         f"{raw_statement}; "
#                         f"END IF; "
#                         f"END $$;"
#                     )
            
#             # Check for CREATE TABLE
#             elif raw_statement.upper().startswith("CREATE TABLE"):
#                 table_name_match = re.search(r'CREATE TABLE\s+"?(\w+)"?\."?(\w+)"?', raw_statement, re.IGNORECASE)
#                 if table_name_match:
#                     schema_name, table_name = table_name_match.groups()
#                     raw_statement = (
#                         f"DO $$ BEGIN "
#                         f"IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = '{schema_name}' AND table_name = '{table_name}') THEN "
#                         f"{raw_statement}; "
#                         f"END IF; "
#                         f"END $$;"
#                     )
            
#             # General transformations
#             raw_statement = sql_format(raw_statement, reindent=True, keyword_case='upper')
#             raw_statement = re.sub(r"`", r'"', raw_statement)  # Convert backticks to double quotes
#             raw_statement = re.sub(r"(?i)\bAUTO_INCREMENT\b", "SERIAL", raw_statement, flags=re.IGNORECASE)
#             raw_statement = re.sub(r",\s*\)", ")", raw_statement)  # Remove trailing commas before closing parenthesis
#             raw_statement = re.sub(r"\bVALUES\s*\(([^)]+)\)", correct_insert_values, raw_statement, flags=re.IGNORECASE)
#             raw_statement = re.sub(r"\);?\s*$", ");", raw_statement.strip())  # Ensure statements end with a semicolon
#             raw_statement = re.sub(r'BEGIN\s+/', 'BEGIN;', raw_statement, flags=re.IGNORECASE)  # Correct BEGIN block
#             raw_statement = re.sub(r'END\s+/', 'END;', raw_statement, flags=re.IGNORECASE)  # Correct END block
#             raw_statement = re.sub(r"(?i)\bDELIMITER\s+//", "", raw_statement)  # Remove DELIMITER directives
#             raw_statement = re.sub(r"(?i)\bDELIMITER\s*;", "", raw_statement)  # Normalize statement end delimiter
#             raw_statement = re.sub(r"(?i)\bSHOW\s+WARNINGS\b", "-- SHOW WARNINGS not supported in PostgreSQL", raw_statement)

#             transformed_statements.append(raw_statement)

#         # Join all transformed statements into a single string
#         final_transformed_statement = " ".join(transformed_statements)
#         logging.info(f"Transformed SQL: {final_transformed_statement}")
#         return final_transformed_statement
    
#     except Exception as e:
#         logging.error(f"Error in SQL transformation: {e}")
#         raise







# def correct_insert_values(match):
#     values = match.group(1)
#     # Detect key-value pairs and transform them to 'key: value'
#     key_value_pairs = re.findall(r'"([^"]+)"\s*:\s*([^,]+)', values)
    
#     # Transform each pair into a string 'key: value'
#     transformed_values = [f"'{key}: {value.strip()}'" for key, value in key_value_pairs]
    
#     return f"VALUES ({', '.join(transformed_values)})"




# def split_sql_statements(content: str):
#     statements = re.split(r';\s*(?=(?:[^\'"]*["\'][^\'"]*["\'])*[^\'"]*$)', content)
#     return [stmt.strip() for stmt in statements if stmt.strip()]

# def transform_sql_to_postgresql(statement: str) -> str:
#     statement = re.sub(r"`", r'"', statement)  # Convert backticks to double quotes
#     statement = re.sub(r"(?i)\bAUTO_INCREMENT\b", "SERIAL", statement, flags=re.IGNORECASE)
#     statement = re.sub(r",\s*\)", ")", statement)  # Remove trailing commas before closing parenthesis
#     statement = re.sub(r"\bVALUES\s*\(([^)]+)\)", correct_insert_values, statement, flags=re.IGNORECASE)
#     statement = re.sub(r"\);?\s*$", ");", statement.strip())  # Ensure statements end with a semicolon
#     statement = re.sub(r'BEGIN\s+/', 'BEGIN;', statement, flags=re.IGNORECASE)  # Correct BEGIN block
#     statement = re.sub(r'END\s+/', 'END;', statement, flags=re.IGNORECASE)  # Correct END block
#     statement = re.sub(r"(?i)\bDELIMITER\s+//", "", statement)  # Remove DELIMITER directives
#     statement = re.sub(r"(?i)\bDELIMITER\s*;", "", statement)  # Normalize statement end delimiter
#     statement = re.sub(r"(?i)\bSHOW\s+WARNINGS\b", "-- SHOW WARNINGS not supported in PostgreSQL", statement)
   
#     return statement
 # statement = transform_json_strings_in_copy(statement)  # Add transformation for JSON-like strings


# def transform_sql_to_postgresql(statement: str) -> str:
#     statement = re.sub(r"`", r'"', statement)  # Convert backticks to double quotes
#     statement = re.sub(r"(?i)\bAUTO_INCREMENT\b", "SERIAL", statement, flags=re.IGNORECASE)
#     statement = re.sub(r",\s*\)", ")", statement)  # Remove trailing commas before closing parenthesis
#     statement = re.sub(r"\bVALUES\s*\(([^)]+)\)", correct_insert_values, statement, flags=re.IGNORECASE)
#     statement = re.sub(r"\);?\s*$", ");", statement.strip())  # Ensure statements end with a semicolon
#     statement = re.sub(r'BEGIN\s+/', 'BEGIN;', statement, flags=re.IGNORECASE)  # Correct BEGIN block
#     statement = re.sub(r'END\s+/', 'END;', statement, flags=re.IGNORECASE)  # Correct END block
#     statement = re.sub(r"(?i)\bDELIMITER\s+//", "", statement)  # Remove DELIMITER directives
#     statement = re.sub(r"(?i)\bDELIMITER\s*;", "", statement)  # Normalize statement end delimiter
#     statement = re.sub(r"(?i)\bSHOW\s+WARNINGS\b", "-- SHOW WARNINGS not supported in PostgreSQL", statement)
#     return statement



# def correct_insert_values(match):
#     values = match.group(1)
#     # Transform key-value pairs into a single string with format 'key: value'
#     transformed_values = []
#     for item in re.findall(r'"\s*([^"]+)\s*"\s*:\s*([^,]+)', values):
#         key, value = item
#         key = key.strip('"')  # Remove any extra quotes from keys
#         value = value.strip()  # Ensure no extra spaces
#         transformed_values.append(f"'{key}: {value}'")
#     return f"VALUES ({', '.join(transformed_values)})"

# def correct_insert_values(match):
#     values = match.group(1)
#     # Parse the key-value pairs and transform them into SQL-compatible tuples
#     transformed_values = []
#     for item in re.findall(r'"\s*([^"]+)\s*"\s*:\s*([^,]+)', values):
#         key, value = item
#         key = key.strip('"')  # Remove extra quotes from keys
#         transformed_values.append(f"('{key}', {value.strip()})")
#     return f"VALUES {', '.join(transformed_values)}"

# def correct_insert_values(match):
#     values = match.group(1)
#     # Remove trailing commas inside the column definition
#     values = re.sub(r",\s*\)", ")", values)
#     # Split key-value pairs and transform them
#     key_value_pairs = re.findall(r'"([^"]+)":\s*(\d+)', values)
#     corrected_values = ", ".join(f"('{k}', {v})" for k, v in key_value_pairs)
#     return f"VALUES {corrected_values}"




# celery_app = Celery("tasks")
# celery_app.config_from_object("celeryconfig")

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Helper functions
# async def execute_sql_file(file: UploadFile):
#     content = (await file.read()).decode('utf-8')
#     statements = split_sql_statements(content)
#     print("\ndatabase: ", database)
#     async with database.transaction():
#         for statement in statements:
#             if statement.strip():
#                 statement = transform_sql_to_postgresql(statement)
#                 try:
#                     await database.execute(statement)
#                 except asyncpg.exceptions.DuplicateTableError:
#                     # Skip existing CREATE TABLE or SCHEMA errors
#                     continue
#                 except asyncpg.exceptions.UniqueViolationError:
#                     # Handle unique violations gracefully
#                     continue
#                 except Exception as e:
#                     raise HTTPException(status_code=400, detail=f"SQL execution error: {str(e)}")

# def split_sql_statements(content: str):
#     # Split the content into individual SQL statements, taking care of comments and multi-line commands
#     statements = re.split(r';\s*(?=(?:[^\'"]*["\'][^\'"]*["\'])*[^\'"]*$)', content)
#     return [stmt.strip() for stmt in statements if stmt.strip()]

# def transform_sql_to_postgresql(statement: str) -> str:
#     """
#     Transforms general SQL syntax to be compatible with PostgreSQL, covering various SQL constructs.
#     """
#     # Correct MySQL-specific syntax and transform it into PostgreSQL
#     statement = re.sub(r"`", r'"', statement)  # Convert backticks to double quotes
#     statement = re.sub(r"(?i)\bAUTO_INCREMENT\b", "SERIAL", statement, flags=re.IGNORECASE)
#     statement = re.sub(r",\s*\)", ")", statement)  # Remove trailing commas before closing parenthesis
#     statement = re.sub(r"\bVALUES\s*\(([^)]+)\)", correct_insert_values, statement, flags=re.IGNORECASE)
#     statement = re.sub(r"\);?\s*$", ");", statement.strip())  # Ensure statements end with a semicolon
#     statement = re.sub(r'BEGIN\s+/', 'BEGIN;', statement, flags=re.IGNORECASE)  # Correct BEGIN block
#     statement = re.sub(r'END\s+/', 'END;', statement, flags=re.IGNORECASE)  # Correct END block
#     statement = re.sub(r"(?i)\bDELIMITER\s+//", "", statement)  # Remove DELIMITER directives
#     statement = re.sub(r"(?i)\bDELIMITER\s*;", "", statement)  # Normalize statement end delimiter
#     statement = re.sub(r"(?i)\bSHOW\s+WARNINGS\b", "-- SHOW WARNINGS not supported in PostgreSQL", statement)
#     return statement

# def correct_insert_values(match):
#     values = match.group(1)
#     corrected_values = re.sub(r'"([^"]+):\s*([^"]+)"', r"('\1', \2)", values)
#     return f"VALUES {corrected_values}"




###########_--------------------------------------------

# @celery_app.task(bind=True)
# def process_sql(self, sql_text: str):
#     sql_text = clean_sql_syntax(sql_text)
    
#     try:
#         with engine.connect() as connection:
#             for statement in split_sql_statements(sql_text):
#                 if statement.strip():
#                     try:
#                         connection.execute(text(statement))
#                         current_task.update_state(state='PROGRESS', meta={'status': f'Executed: {statement[:50]}...'})
#                     except ProgrammingError as e:
#                         if 'already exists' in str(e) or 'syntax error' in str(e):
#                             logging.warning(f"Ignored error: {e}")
#                             continue
#                         else:
#                             raise e
#         logging.info("SQL file executed successfully")
#     except Exception as e:
#         logging.error(f"Error executing SQL file: {e}")
#         raise

# def clean_sql_syntax(sql_text):
#     sql_text = re.sub(r",\s*\)", ")", sql_text, flags=re.MULTILINE)
#     sql_text = re.sub(r'VALUES\s+\(([^)]+)\);', lambda match: clean_insert_values(match.group(1)), sql_text, flags=re.MULTILINE)
#     return sql_text

# def clean_insert_values(values_str):
#     clean_values = re.sub(r'["\']', '', values_str)
#     return f"VALUES ({clean_values})"

# def split_sql_statements(sql_text):
#     statements = sqlparse.split(sql_text)
#     return [stmt.strip() for stmt in statements if stmt.strip()]
