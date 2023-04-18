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
        cur.execute("SELECT * FROM Users")
        rows = cur.fetchall()
        u=[]
        # User Table Test
        for row in rows:
            print("Users",row)
            u.append(row[0])
        u.sort()
        #Favor Movie Test
        cur.execute("INSERT INTO FavorMovies (uid, movieID) VALUES (%s, 12345)",(u[0],))
        cur.execute("SELECT * FROM FavorMovies")
        rows = cur.fetchall()
        print("FavorMovies",rows)

        #Friendswith Test
        cur.execute("INSERT INTO FriendsWith (uid1,uid2) VALUES (%s,%s)",(u[0],u[1],))
        cur.execute("SELECT * FROM FriendsWith")
        rows = cur.fetchall()
        print("FriendsWith",rows)
        
        #Watch Party Test
        cur.execute("INSERT INTO WatchParty(ownerId,movieId) VALUES (%s,12345)", (u[0],))
        cur.execute("SELECT * FROM WatchParty")
        rows= cur.fetchall()
        w=rows[0]
        print("WatchParty",rows)
        
        #Participates In Test
        cur.execute("INSERT INTO ParticipatesIn(wid,parId) VALUES (%s,%s)", (w[0],u[0]))
        cur.execute("INSERT INTO ParticipatesIn(wid,parId) VALUES (%s,%s)", (w[0],u[1]))
        cur.execute("SELECT * FROM ParticipatesIn")
        rows= cur.fetchall()
        print("ParticipatesIn",rows)

        #Organizes Test
        cur.execute("INSERT INTO Organizes(wid,ownerId) VALUES (%s,%s)",(w[0],u[0]))
        cur.execute("SELECT * FROM Organizes")
        rows= cur.fetchall()
        print(f"Organizes:{rows}")


        #Post Test
        cur.execute("INSERT INTO Post(writer,wid) VALUES (%s,%s)",(u[0],w[0]))
        cur.execute("SELECT * FROM Post")
        rows= cur.fetchall()
        p=rows[0]
        print("Post",rows)
        cur.execute("INSERT INTO PostsBy(pid,uid) VALUES (%s,%s)",(p[0],u[0]))
        cur.execute("SELECT * FROM PostsBy")
        rows= cur.fetchall()
        p=rows[0]
        print("PostBy",rows)


        #Comments
        cur.execute("INSERT INTO Comments(content,uid) VALUES (%s,%s)",("String",u[0]))
        cur.execute("SELECT * FROM Comments")
        rows= cur.fetchall()
        c=rows[0]
        print("Comments",rows)
        cur.execute("INSERT INTO CommentsOn(cid,pid) VALUES (%s,%s)",(c[0],p[0]))
        cur.execute("SELECT * FROM CommentsOn")
        rows= cur.fetchall()
        print("CommentsOn",rows)

        #Likes 
        cur.execute("INSERT INTO Likes(pid,uid) VALUES (%s,%s)",(p[0],u[0]))
        cur.execute("SELECT * FROM Likes")
        rows= cur.fetchall()
        print("Likes",rows)
        
        connection.commit()






    # Close communication with the database
    connection.close()