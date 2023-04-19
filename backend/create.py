import logging
import os
import psycopg
from psycopg.errors import ProgrammingError
import json

if __name__ == "__main__":
    # Connect to CockroachDB
    credential_file = open("crudential.json")

    credential_data = json.load(credential_file)

    connection = psycopg.connect(credential_data['General_connection_string'], application_name="$moviedate")

    create_query_file = open("dbinit.sql", "r")

    create_query = create_query_file.read()

    with connection.cursor() as cur:
        cur.execute(create_query)
        connection.commit()

    # Close communication with the database
    connection.close()