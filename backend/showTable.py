import argparse
import psycopg
from psycopg.errors import ProgrammingError
import json

if __name__ == "__main__":
    # Connect to CockroachDB
    credential_file = open("crudential.json")

    credential_data = json.load(credential_file)

    connection = psycopg.connect(credential_data['General_connection_string'], application_name="$moviedate")

    parser = argparse.ArgumentParser(description = "MovieDate Show Table")
    parser.add_argument("--table", type = str, help = "table name for showing")

    args = parser.parse_args()
    table = args.table
    query = "SELECT * FROM {0}".format(table)

    with connection.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
        for row in results:
            print(row)
        # #Favor Movie Test
        # cur.execute("UPDATE Users SET favorMovies = array_append(favorMovies, 12345) WHERE uid = %s",(u[0],))
        # cur.execute("UPDATE Users SET favorMovies = array_append(favorMovies, 23456) WHERE uid = %s",(u[0],))
        # cur.execute("SELECT * FROM Users")
        # rows = cur.fetchall()
        # print("FavorMovies",rows)

        # #Friendswith Test
        # cur.execute("INSERT INTO FriendsWith (uid1,uid2) VALUES (%s,%s)",(u[0],u[1],))
        # cur.execute("SELECT * FROM FriendsWith")
        # rows = cur.fetchall()
        # print("FriendsWith",rows)
        
        # #Watch Party Test
        # cur.execute("INSERT INTO WatchParty(ownerId,movieId) VALUES (%s,12345)", (u[0],))
        # cur.execute("SELECT * FROM WatchParty")
        # rows= cur.fetchall()
        # w=rows[0]
        # print("WatchParty",rows)
        
        # #Participates In Test
        # cur.execute("INSERT INTO ParticipatesIn(wid,parId) VALUES (%s,%s)", (w[0],u[0]))
        # cur.execute("INSERT INTO ParticipatesIn(wid,parId) VALUES (%s,%s)", (w[0],u[1]))
        # cur.execute("SELECT * FROM ParticipatesIn")
        # rows= cur.fetchall()
        # print("ParticipatesIn",rows)

        # #Organizes Test
        # cur.execute("INSERT INTO Organizes(wid,ownerId) VALUES (%s,%s)",(w[0],u[0]))
        # cur.execute("SELECT * FROM Organizes")
        # rows= cur.fetchall()
        # print(f"Organizes:{rows}")


        # #Post Test
        # cur.execute("INSERT INTO Post(writer,wid) VALUES (%s,%s)",(u[0],w[0]))
        # cur.execute("SELECT * FROM Post")
        # rows= cur.fetchall()
        # p=rows[0]
        # print("Post",rows)
        # cur.execute("INSERT INTO PostsBy(pid,uid) VALUES (%s,%s)",(p[0],u[0]))
        # cur.execute("SELECT * FROM PostsBy")
        # rows= cur.fetchall()
        # p=rows[0]
        # print("PostBy",rows)


        # #Comments
        # cur.execute("INSERT INTO Comments(content,uid) VALUES (%s,%s)",("String",u[0]))
        # cur.execute("SELECT * FROM Comments")
        # rows= cur.fetchall()
        # c=rows[0]
        # print("Comments",rows)
        # cur.execute("INSERT INTO CommentsOn(cid,pid,uid) VALUES (%s,%s,%s)",(c[0],p[0],u[0]))
        # cur.execute("SELECT * FROM CommentsOn")
        # rows= cur.fetchall()
        # print("CommentsOn",rows)

        # #Likes 
        # cur.execute("INSERT INTO Likes(pid,uid) VALUES (%s,%s)",(p[0],u[0]))
        # cur.execute("SELECT * FROM Likes")
        # rows= cur.fetchall()
        # print("Likes",rows)
        
        connection.commit()
        
    # Close communication with the database
    connection.close()