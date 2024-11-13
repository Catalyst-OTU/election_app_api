FROM postgis/postgis:12-master

COPY ./apollo_Db.sql /docker-entrypoint-initdb.d/1-apollo_Db.sql

COPY ./aiti_schema.sql /docker-entrypoint-initdb.d/2-aiti_schema.sql

