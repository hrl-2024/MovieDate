# Create the user and return the uid of the user
def insert_user(connection, name : str):

    query = "INSERT INTO Users (uname) VALUES (\'{uname}\') RETURNING uid".format(uname = name)

    id = None

    with connection.cursor() as cur:
        cur.execute(query)
        id = cur.fetchone()
        connection.commit()

    return id[0]