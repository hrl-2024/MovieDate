import psycopg
from psycopg.errors import ProgrammingError

# Create the user and return the uid of the user
def insert_user(connection, name : str):

    query = "INSERT INTO Users (uname) VALUES ('{uname}') RETURNING uid".format(uname = name)

    id = None

    with connection.cursor() as cur:
        cur.execute(query)
        id = cur.fetchone()
        connection.commit()

    return id[0]

def getUser(connection, id):
    
    query = "SELECT * FROM Users WHERE uid = {uid}".format(uid = id)

    user = None

    with connection.cursor() as cur:
        cur.execute(query)
        user = cur.fetchone()
        connection.commit()

    return user

def updateAvatar(connection, uid, avatar):

    query = "UPDATE Users SET avatar = CAST('{0}' AS BLOB) WHERE uid = {1}".format(avatar, uid)

    with connection.cursor() as cur:
        cur.execute(query)
        connection.commit()

    return True
    
def addToFavoriteMovie(connection, uid, mid):

    query = "UPDATE Users SET favorMovies = array_append(favorMovies, {0}) WHERE uid = {1}".format(mid, uid)

    with connection.cursor() as cur:
        cur.execute(query)
        connection.commit()

    return True

def removeFromFavoriteMovie(connection, uid, mid):
    query = "UPDATE Users SET favorMovies = array_remove(favorMovies, {0}) WHERE uid = {1}".format(mid, uid)

    with connection.cursor() as cur:
        cur.execute(query)
        connection.commit()

    return True

def addFriend(connection, uid1, uid2):

    query1 = "INSERT INTO FriendsWith (uid1,uid2) VALUES ({0},{1})".format(uid1,uid2)
    query2 = "INSERT INTO FriendsWith (uid1,uid2) VALUES ({0},{1})".format(uid2,uid1)

    with connection.cursor() as cur:
        cur.execute(query1)
        cur.execute(query2)
        connection.commit()

    return True

def removeFriend(connection, uid1, uid2):
    query1 = "DELETE FROM FriendsWith WHERE uid1 = {0} AND uid2 = {1}".format(uid1,uid2)
    query2 = "DELETE FROM FriendsWith WHERE uid1 = {0} AND uid2 = {1}".format(uid2,uid1)

    with connection.cursor() as cur:
        cur.execute(query1)
        cur.execute(query2)
        connection.commit()

    return True
