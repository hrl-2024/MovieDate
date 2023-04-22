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

def createWatchParty(connection, uid, mid, date, platform):

    query1 = "INSERT INTO WatchParty(ownerId,movieId,Dates,Platform) VALUES ({0},{1},'{2}','{3}') RETURNING wid".format(uid, mid, date, platform)

    wid = None

    with connection.cursor() as cur:
        cur.execute(query1)
        wid = cur.fetchone()[0]
        connection.commit()

    return wid

def deleteWatchParty(connection, wid):
    query = "DELETE FROM WatchParty WHERE wid = {0}".format(wid)

    with connection.cursor() as cur:
        cur.execute(query)
        connection.commit()
    
    return True

def getUserWatchParty(connection, uid):
    # find the wid first
    query = "SELECT * FROM WatchParty WHERE ownerId = {0}".format(uid)

    result = None

    with connection.cursor() as cur:
        cur.execute(query)
        result = cur.fetchall()
        connection.commit()

    return result

def addToWatchParty(connection, participant, wid):
    with connection.cursor() as cur:
        query = "INSERT INTO ParticipatesIn (wid, parId) VALUES ({0},{1})".format(wid, participant)
        cur.execute(query)
        connection.commit()

    return True

def addToWatchPartyWithNoId(connection, participant, organizer, movie, date):

    # find the wid first
    findWidQuery = "SELECT wid FROM WatchParty WHERE ownerId = {0} AND movieId = {1} AND Dates='{2}'".format(organizer, movie, date)

    wid = None

    with connection.cursor() as cur:
        cur.execute(findWidQuery)
        wid = cur.fetchone()[0]

        print("found wid: ", wid)

        # insert
        query = "INSERT INTO ParticipatesIn (wid, parId) VALUES ({0},{1})".format(wid, participant)
        cur.execute(query)
        connection.commit()

    return True

def getUserParticipatedWatchParty(connection, participant):
    wid = None

    with connection.cursor() as cur:
        query = """
        SELECT *
        FROM WatchParty
        WHERE wid in 
            (SELECT wid FROM ParticipatesIn WHERE parId = {0})""".format(participant)
        cur.execute(query)
        connection.commit()

        wid = cur.fetchall()

    return wid