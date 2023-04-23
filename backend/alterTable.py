import argparse
import psycopg
from psycopg.errors import ProgrammingError
import json

if __name__ == "__main__":
    # Connect to CockroachDB
    credential_file = open("crudential.json")

    credential_data = json.load(credential_file)

    connection = psycopg.connect(credential_data['General_connection_string'], application_name="$moviedate")

    query = """CREATE TABLE Likes(
	pid INT NOT NULL,
    uid INT NOT NULL,
    PRIMARY KEY(pid,uid),
    CONSTRAINT Likes_FK_uid FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE,
    CONSTRAINT Likes_FK_pid FOREIGN KEY (pid) REFERENCES Post(pid) ON DELETE CASCADE
)"""

    with connection.cursor() as cur:
        cur.execute(query)
        # res = cur.fetchall()
        connection.commit()
    
    # Close communication with the database
    connection.close()