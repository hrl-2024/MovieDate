import argparse
import psycopg
from psycopg.errors import ProgrammingError
import json

if __name__ == "__main__":
    # Connect to CockroachDB
    credential_file = open("crudential.json")

    credential_data = json.load(credential_file)

    connection = psycopg.connect(credential_data['General_connection_string'], application_name="$moviedate")

    query = """ALTER TABLE WatchParty
                ADD COLUMN atTime TIME"""

    # query = """SELECT * FROM Users WHERE uid = 858938797350584321 AND 1234 = ANY(favorMovies)"""

    query = "DELETE FROM WatchParty WHERE wid = 858961754158071809"

    with connection.cursor() as cur:
        cur.execute(query)
        # res = cur.fetchall()
        connection.commit()
    
    # Close communication with the database
    connection.close()