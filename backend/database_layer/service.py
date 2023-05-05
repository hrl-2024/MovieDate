import psycopg
from psycopg.errors import ProgrammingError

# Create the user and return the uid of the user
def insert_user(connection, name : str, avatar, email, password):

    parsedName = name.replace("'", "''")
    parsedEmail = email.replace("'", "''")
    parsedpassword = str(password).replace("'", "''")

    query = """INSERT INTO Users (uname, email, pwd) VALUES ('{0}', '{1}', '{2}') RETURNING uid""".format(parsedName, parsedEmail, parsedpassword)

    if avatar:
        query = """INSERT INTO Users (uname, avatar, email, pwd) VALUES ('{0}', CAST('{1}' AS BLOB), '{2}', '{3}' )
        RETURNING uid""".format(parsedName, avatar, parsedEmail, parsedpassword)

    id = None

    with connection.cursor() as cur:
        try:
            cur.execute(query)
            id = cur.fetchone()
            connection.commit()
        except psycopg.errors.UniqueViolation as e:
            connection.rollback()
            return False, f"Error: {e}"

    return True, id[0]

# Create the user and return the uid of the user
def insert_oauthuser(connection, id, name, email, avatar):

    parsedName = name.replace("'", "''")
    parsedEmail = email.replace("'", "''")

    query = """INSERT INTO Users (uid, uname, email) VALUES ('{0}', '{1}', '{2}') RETURNING uid""".format(id, parsedName, parsedEmail)

    if avatar:
        query = """INSERT INTO Users (uid, uname, email, avatar) VALUES ('{0}', '{1}', '{2}', CAST('{3}' AS BLOB) )
        RETURNING uid""".format(id, parsedName, parsedEmail, avatar)

    id = None

    with connection.cursor() as cur:
        try:
            cur.execute(query)
            id = cur.fetchone()
            connection.commit()
            print("jjjj")
            print(id[0])
        except psycopg.errors.UniqueViolation as e:
            connection.rollback()
            
            return False, f"Error: {e}"

    return True, id[0]

def getUserById(connection, id):
    
    query = "SELECT uid, uname, email, avatar, favormovies FROM Users WHERE uid = {uid}".format(uid = id)

    user = None

    with connection.cursor() as cur:
        cur.execute(query)
        user = cur.fetchone()
        connection.commit()

    return user

def getUserByEmail(connection, email, password):

    parsedEmail = email.replace("'", "''")
    parsedpassword = str(password).replace("'", "''")

    print("password      :", password)
    print("parsedpassword:", parsedpassword)
    
    query = "SELECT uid, uname, email, avatar, favormovies FROM Users WHERE email = '{0}' AND pwd = '{1}'".format(parsedEmail, parsedpassword)

    user = None

    with connection.cursor() as cur:
        cur.execute(query)
        user = cur.fetchone()
        connection.commit()

    return user


def updateAvatar(connection, uid, avatar):

    checkUserExist = "SELECT uid FROM Users WHERE uid = {0}".format(uid)
    with connection.cursor() as cur:
        cur.execute(checkUserExist)
        userExist = cur.fetchone()
        connection.commit()
    
    if not userExist:
        return False, "user doesn't exist"

    query = "UPDATE Users SET avatar = CAST('{0}' AS BLOB) WHERE uid = {1}".format(avatar, uid)

    with connection.cursor() as cur:
        cur.execute(query)
        connection.commit()

    return True, "updated"

def updateName(connection, uid, name):

    checkUserExist = "SELECT uid FROM Users WHERE uid = {0}".format(uid)
    with connection.cursor() as cur:
        cur.execute(checkUserExist)
        userExist = cur.fetchone()
        connection.commit()
    
    if not userExist:
        return False, "user doesn't exist"

    parsedName = name.replace("'", "''")

    query = "UPDATE Users SET uname = '{0}' WHERE uid = {1}".format(parsedName, uid)

    with connection.cursor() as cur:
        cur.execute(query)
        connection.commit()

    return True, "updated"
    
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
        try:
            cur.execute(query1)
            cur.execute(query2)
            connection.commit()
        except psycopg.errors.UniqueViolation:
            connection.rollback()
            return False, "already friend"
    
    return True, "Added"

def removeFriend(connection, uid1, uid2):
    query1 = "DELETE FROM FriendsWith WHERE uid1 = {0} AND uid2 = {1}".format(uid1,uid2)
    query2 = "DELETE FROM FriendsWith WHERE uid1 = {0} AND uid2 = {1}".format(uid2,uid1)

    with connection.cursor() as cur:
        cur.execute(query1)
        cur.execute(query2)
        connection.commit()

    return True

def createWatchParty(connection, uid, mid, date, atTime, platform):

    query = """INSERT INTO WatchParty(ownerId,movieId,Dates,atTime,Platform)
        VALUES ({0},{1},'{2}',TIME '{3}','{4}')
        RETURNING wid""".format(uid, mid, date, atTime, platform)

    wid = None

    with connection.cursor() as cur:
        try:
            cur.execute(query)
            wid = cur.fetchone()[0]
            connection.commit()
        except psycopg.errors.InvalidDatetimeFormat:
            connection.rollback()
            return False, "Invalid time format", None

    return True, "created", wid

def deleteWatchParty(connection, wid):
    query = "DELETE FROM WatchParty WHERE wid = {0}".format(wid)

    with connection.cursor() as cur:
        cur.execute(query)
        connection.commit()
    
    return True

def getUserWatchParty(connection, uid):
    # find the wid first
    query = """SELECT wid, ownerId, movieId, Dates, atTime, Platform 
        FROM WatchParty
        WHERE ownerId = {0}""".format(uid)

    result = None

    with connection.cursor() as cur:
        cur.execute(query)
        result = cur.fetchall()
        connection.commit()

    return result

def addToWatchParty(connection, participant, wid):
    with connection.cursor() as cur:
        try:
            query = "INSERT INTO ParticipatesIn (wid, parId) VALUES ({0},{1})".format(wid, participant)
            cur.execute(query)
            connection.commit()
        except psycopg.errors.UniqueViolation:
            connection.rollback()
            return False, "already participated"

    return True, "added"

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
        SELECT wid, ownerId, movieId, Dates, atTime, Platform, uname, avatar
        FROM WatchParty
        INNER JOIN Users ON Users.uid = WatchParty.ownerId
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
        query = """INSERT INTO Post (writer, movie_id, pdate, ptime, content)
                VALUES({0}, {1}, CURRENT_TIMESTAMP, CURRENT_TIME, '{2}')
                RETURNING pid """.format(
                uid, movie_id, parsed_content
                )
        
        if wid != 0:
            query = """INSERT INTO Post (writer, movie_id, pdate, ptime, content, wid)
                VALUES({0}, {1}, CURRENT_TIMESTAMP, CURRENT_TIME, '{2}', {3})
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
        query = """SELECT pid, writer, movie_id, pdate, ptime, content, wid, uname, avatar
            FROM Post, Users
            WHERE Post.writer = {0} AND Post.writer = Users.uid
            ORDER BY pdate DESC, ptime DESC""".format(uid)
        
        cur.execute(query)
        post = cur.fetchall()
        connection.commit()

    return post

def getAllPost(connection, uid):

    post = None

    with connection.cursor() as cur:
        query = """SELECT pid, writer, movie_id, pdate, ptime, content, wid, uname, avatar
            FROM Post, Users
            WHERE writer in (
                SELECT uid2
                FROM FriendsWith
                WHERE uid1 = {uid}            
                ) OR writer = {uid} AND Post.writer = Users.uid
            ORDER BY pdate DESC""".format(uid=uid)
        
        cur.execute(query)
        post = cur.fetchall()
        connection.commit()

    return post

def deletePost(connection, pid):

    with connection.cursor() as cur:
        query = """DELETE FROM Post WHERE pid = {0} """.format(pid)
        
        cur.execute(query)
        connection.commit()

    return True
    

def postComment(connection, uid, pid, comment):

    cid = None

    parsedComment = comment.replace("'", "''")

    with connection.cursor() as cur:
        try:
            query = """ INSERT INTO Comments (pid, content, cdate, ctime, uid)
                        VALUES({0}, '{1}', CURRENT_TIMESTAMP, CURRENT_TIME, {2})
                        RETURNING cid""".format(pid, parsedComment, uid)
            
            cur.execute(query)
            cid = cur.fetchone()[0]
            connection.commit()
        except psycopg.errors.ForeignKeyViolation:
            connection.rollback()
            return False, "ForeignKeyViolation"

    return True, cid

def getComment(connection, pid):

    comments = None

    with connection.cursor() as cur:
        query = """ SELECT cid, pid, content, cdate, ctime, Comments.uid, uname, avatar
         FROM Comments, Users
         WHERE pid = {0} AND Comments.uid = Users.uid
         ORDER BY cdate DESC, ctime DESC  """.format(pid)
        
        cur.execute(query)
        comments = cur.fetchall()
        connection.commit()

    return comments

def deleteComment(connection, cid):
    with connection.cursor() as cur:
        query = """DELETE FROM Comments WHERE cid = {0}""".format(cid)
        cur.execute(query)
        connection.commit()

    return True