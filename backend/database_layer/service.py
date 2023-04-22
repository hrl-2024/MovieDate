import psycopg
from psycopg.errors import ProgrammingError

# Create the user and return the uid of the user
def insert_user(connection, name : str, avatar=None):

    parsedName = name.replace("'", "''")

    query = """INSERT INTO Users (uname) VALUES ('{uname}') RETURNING uid""".format(uname = parsedName)

    if avatar:
        query = """INSERT INTO Users (uname, avatar) VALUES ('{0}', CAST('{1}' AS BLOB) )
        RETURNING uid""".format(parsedName, avatar)

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

def updateName(connection, uid, name):

    parsedName = name.replace("'", "''")

    query = "UPDATE Users SET uname = '{0}' WHERE uid = {1}".format(parsedName, uid)

    with connection.cursor() as cur:
        cur.execute(query)
        connection.commit()

    return True
    
def addToFavoriteMovie(connection, uid, mid):

    checkIfAlready = """SELECT uname FROM Users WHERE uid = {0} AND {1} = ANY(favorMovies)""".format(uid, mid)

    with connection.cursor() as cur:
        cur.execute(checkIfAlready)
        res = cur.fetchall()
        connection.commit()

    print("res:", res)

    if len(res) != 0:
        return False, "already in user's favorite"

    query = "UPDATE Users SET favorMovies = array_append(favorMovies, {0}) WHERE uid = {1}".format(mid, uid)

    with connection.cursor() as cur:
        cur.execute(query)
        connection.commit()

    return True, "added"

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

def createPost(connection, uid, movie_id : 0, content, wid : 0):
    pid = None

    parsed_content = content.replace("'", "''")
    print("parsed_content:", parsed_content)

    with connection.cursor() as cur:
        query = """INSERT INTO Post (writer, movie_id, pdate, content)
                VALUES({0}, {1}, CURRENT_TIMESTAMP, '{2}')
                RETURNING pid """.format(
                uid, movie_id, parsed_content
                )
        
        if wid != 0:
            query = """INSERT INTO Post (writer, movie_id, pdate, content, wid)
                VALUES({0}, {1}, CURRENT_TIMESTAMP, '{2}', {3})
                RETURNING pid """.format(
                uid, movie_id, parsed_content, wid
                )
        
        cur.execute(query)
        connection.commit()

        pid = cur.fetchone()[0]

    return pid

def getUserPost(connection, uid):
    post = None

    with connection.cursor() as cur:
        query = """SELECT *
            FROM Post
            WHERE writer = {0}
            ORDER BY pdate DESC""".format(uid)
        
        cur.execute(query)
        post = cur.fetchall()
        connection.commit()

    return post

def getAllPost(connection, uid):

    post = None

    with connection.cursor() as cur:
        query = """SELECT *
            FROM Post
            WHERE writer in (
                SELECT uid2
                FROM FriendsWith
                WHERE uid1 = {uid}            
                ) OR writer = {uid}
            ORDER BY pdate DESC""".format(uid=uid)
        
        cur.execute(query)
        post = cur.fetchall()
        connection.commit()

    return post

def postComment(connection, uid, pid, comment):

    cid = None

    parsedComment = comment.replace("'", "''")

    with connection.cursor() as cur:
        query = """ INSERT INTO Comments (pid, content, cdate, uid)
                    VALUES({0}, '{1}', CURRENT_TIMESTAMP, {2})
                    RETURNING cid""".format(pid, parsedComment, uid)
        
        cur.execute(query)
        cid = cur.fetchone()[0]
        connection.commit()

    return cid

def getComment(connection, pid):

    comments = None

    with connection.cursor() as cur:
        query = """ SELECT *
         FROM Comments
         WHERE pid = {0} """.format(pid)
        
        cur.execute(query)
        comments = cur.fetchall()
        connection.commit()

    return comments