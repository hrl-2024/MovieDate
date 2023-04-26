import argparse
import psycopg
from psycopg.errors import ProgrammingError
import json

if __name__ == "__main__":
    # Connect to CockroachDB
    credential_file = open("crudential.json")

    credential_data = json.load(credential_file)

    connection = psycopg.connect(credential_data['General_connection_string'], application_name="$moviedate")

    query = """INSERT INTO Users (uid, uname, email, pwd) VALUES (1, 'hrl', 'hrl@bu.edu', '12345')"""

    with connection.cursor() as cur:
        cur.execute(query)
        # res = cur.fetchall()
        connection.commit()
    
    # Close communication with the database
    connection.close()