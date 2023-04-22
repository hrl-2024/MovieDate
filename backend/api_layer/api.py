import logging
import os
import psycopg
from psycopg.errors import ProgrammingError
from flask import Flask, request, json
from flask_ngrok import run_with_ngrok
import json
import atexit    # Gracefully exit and cleanup after normal termination

# Need to import database_layer's service.py
import importlib.util
import sys
spec = importlib.util.spec_from_file_location("service", "database_layer/service.py")
DBService = importlib.util.module_from_spec(spec)
sys.modules["service"] = DBService
spec.loader.exec_module(DBService)

app = Flask(__name__)
# run_with_ngrok(app)     # flask_ngrok will not work until they allow using different port than 5000

# get crudential
credential_file = open("crudential.json")
credential_data = json.load(credential_file)

# connect to cockroachDB
connection = psycopg.connect(credential_data['General_connection_string'], application_name="$moviedate")

# Program exit (Signal 64) handler
def exit_handler():
    print("\nFlask application exiting. Closing database connection.")

    # Close communication with the database
    connection.close()

# install the handler
atexit.register(exit_handler)

@app.route('/user', methods=['POST'])
def insert_user():

    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)
    
    name = data.get('name')
    avatar = data.get('avatar')

    print(name)

    id = DBService.insert_user(connection, name, avatar)
    print(id)

    return {"id" : id}

@app.route('/user', methods=['GET'])
def get_user():

    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)
    
    id = data.get('id')
    print(id)

    user = DBService.getUser(connection, id)
    print(user)

    if user == None:
        return {"message": "User doesn't exist."}

    favorite_movie = None if len(user) < 4 else user[3]

    return {"id" : user[0],
            "name" : user[1],
            "avatar": user[2],
            "favorite_movie": favorite_movie}

@app.route("/user/avatar", methods=['PUT'])
def update_avatar():

    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)
    
    id = data.get('id')
    avatar = data.get('avatar')

    result = DBService.updateAvatar(connection, id, avatar)

    return {"updated": result} 

@app.route("/user/name", methods=['PUT'])
def update_name():

    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)
    
    id = data.get('id')
    name = data.get('name')

    result = DBService.updateName(connection, id, name)

    return {"updated": result} 

@app.route('/user/addFavoriteMovie', methods=['POST'])
def addToFavorite():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    uid = data.get("id")
    mid = data.get("movie_id")

    result = DBService.addToFavoriteMovie(connection, uid, mid)

    return {"added:": result}

@app.route('/user/removeFavoriteMovie', methods=['PATCH'])
def removeFromFavorite():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    uid = data.get("id")
    mid = data.get("movie_id")

    result = DBService.removeFromFavoriteMovie(connection, uid, mid)

    return {"removed:": result}

@app.route('/user/addFriend', methods=['POST'])
def addFriend():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    uid1 = data.get("uid1")
    uid2 = data.get("uid2")

    result = DBService.addFriend(connection, uid1, uid2)

    return {"added:": result}

@app.route('/user/removeFriend', methods=['DELETE'])
def removeFriend():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    uid1 = data.get("uid1")
    uid2 = data.get("uid2")

    result = DBService.removeFriend(connection, uid1, uid2)

    return {"removed:": result}

@app.route('/user/WatchParty', methods=['POST'])
def createWatchParty():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    uid = data.get("uid")
    mid = data.get("mid")
    date = data.get("date")
    platform = data.get("platform")

    if mid == None:
            return {"message:": "Creating a new WatchParty with no movie is not allowed."}

    # TODO: check valid date string type (refer to CockroachDB). Return false if invalid

    result = DBService.createWatchParty(connection, uid, mid, date, platform)

    print(result)

    return {"created:": True, "wid": result}

@app.route('/user/WatchParty', methods=['GET'])
def getWatchParty():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    organizer = data.get("uid")

    queryresult = DBService.getUserWatchParty(connection, organizer)

    if queryresult == None:
        return {"message:": "No watch party is created by this user"}
    
    result = []

    for watchParty in queryresult:
        result.append({"wid": watchParty[0],
                "ownerId": watchParty[1],
                "movieId": watchParty[2],
                "Date": watchParty[3],
                "Platform": watchParty[4]
                })
    
    return {"result": result}

@app.route('/user/WatchParty', methods=['DELETE'])
def deleteWatchParty():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    wid = data.get("wid")

    result = DBService.deleteWatchParty(connection, wid)

    return {"removed": result}

@app.route('/user/joinWatchParty', methods=['POST'])
def participateWatchParty():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    participant = data.get("participantID")
    wid = data.get("wid")

    result = DBService.addToWatchParty(connection, participant, wid)

    return {"added:": result}

@app.route('/user/joinWatchPartyWithNoID', methods=['POST'])
def participateWatchPartyWithNoId():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    participant = data.get("participantID")
    organizer = data.get("organizerID")
    movie = data.get("mid")
    date = data.get("date")

    result = DBService.addToWatchPartyWithNoId(connection, participant, organizer, movie, date)

    # TODO: make (organizer, mid, date) unique in sql table: UNIQUE(col1, col2, col3)

    return {"added:": result}

@app.route('/user/getParticipatedWatchParty', methods=['GET'])
def getParticipatedWatchParty():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    participant = data.get("participantID")

    queryresult = DBService.getUserParticipatedWatchParty(connection, participant)

    if queryresult == None:
        return {"message:": "This user have no participated Watch Party"}
    
    result = []

    for watchParty in queryresult:
        result.append({"wid": watchParty[0],
                "ownerId": watchParty[1],
                "movieId": watchParty[2],
                "Date": watchParty[3],
                "Platform": watchParty[4]
                })
    
    return {"result": result}

@app.route('/user/post', methods=['POST'])
def createPost():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    # Required Fields:
    uid = data.get("uid")
    movie_id = data.get("movie_id", 0)
    content = data.get("content")

    # Optional
    newWatchParty = data.get("newWatchParty", False)   # optional. true -> create new watchparty
    wid = 0

    print("content:", content)

    if (newWatchParty):
        date = data.get("date")
        platform = data.get("platform")

        if movie_id == None:
            return {"message:": "Creating a new WatchParty with no movie is not allowed."}

        # TODO: check valid date string type (refer to CockroachDB). Return false if invalid

        wid = DBService.createWatchParty(connection, uid, movie_id, date, platform)
    
    pid = DBService.createPost(connection, uid, movie_id, content, wid)

    return {"created" : True, "pid" : pid}

@app.route('/user/post', methods=['GET'])
def getUserPost():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    # Required Fields:
    uid = data.get("uid")

    posts = DBService.getUserPost(connection, uid)

    result = []

    for p in posts:
        result.append({"pid": p[0],
                       "writer": p[1],
                       "movie_id": p[2],
                       "pdate": p[3],
                       "content": p[4],
                       "wid": p[5]
            })
        
    return {"result": result}

@app.route('/post', methods=['GET'])
def getAllPost():

    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    # Required Fields:
    uid = data.get("uid")

    posts = DBService.getAllPost(connection, uid)

    result = []

    for p in posts:
        result.append({"pid": p[0],
                       "writer": p[1],
                       "movie_id": p[2],
                       "pdate": p[3],
                       "content": p[4],
                       "wid": p[5]
            })
        
    return {"result": result}


@app.route("/comment", methods=["POST"])
def postComment():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    # Required Fields:
    uid = data.get("uid")
    pid = data.get("pid")
    content = data.get("content")

    cid = DBService.postComment(connection, uid, pid, content)

    return {"posted": True, "cid": cid}

@app.route("/comment", methods=["GET"])
def getComment():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    # Required Fields:
    pid = data.get("pid")

    comments = DBService.getComment(connection, pid)

    result = []

    for c in comments:
        result.append({
            "cid": c[0],
            "content": c[1],
            "cdate": c[2],
            "uid": c[3],
            "pid": c[4]
        })

    return {"result":result}


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(port=5002)