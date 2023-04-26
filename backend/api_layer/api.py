import logging
import os
import psycopg
from psycopg.errors import ProgrammingError
from flask import Flask, request, json, abort
from flask_ngrok import run_with_ngrok
import json
import atexit    # Gracefully exit and cleanup after normal termination

from datetime import datetime

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

# To check if the date is in valid format
def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        pass

    try:
        datetime.strptime(date_string, '%m-%d-%Y')
        return True
    except ValueError:
        pass

    try:
        datetime.strptime(date_string, '%m-%d-%y')
        return True
    except ValueError:
        pass

    try:
        datetime.strptime(date_string, '%y-%m-%d')
        return True
    except ValueError:
        pass

    try:
        datetime.strptime(date_string, '%d-%m-%y')
        return True
    except ValueError:
        pass

    return False

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
    email = data.get('email')
    password = data.get('password')

    if not (name and email and password):
        abort(400, "missing required field")

    # hash the password before passing in to the database service layer
    ok, message = DBService.insert_user(connection, name, avatar, email, hash(password))

    if ok:
        return {"success": True, "id" : message}
    else:
        return {"success": False, "message" : message}
    
@app.route('/oauthuser', methods=['POST'])
def insert_oauthuser():

    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)
    
    id = data.get('id')
    name = data.get('name')
    avatar = data.get('avatar')
    email = data.get('email')

    if not (id and name and email):
        abort(400, "missing required field")

    # hash the password before passing in to the database service layer
    ok, message = DBService.insert_oauthuser(connection, id, name, email, avatar)

    if ok:
        return {"success": True, "id" : message}
    else:
        return {"success": False, "message" : message}

@app.route('/user', methods=['GET'])
def get_user():

    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)
    
    id = data.get('id')
    email = data.get('email')
    
    if not (id or email):
        abort(400, "need at least one field: id or email")

    if id:
        user = DBService.getUserById(connection, id)
        print(user)

        if user == None:
            return {"found": False, "message": "User doesn't exist."}

        favorite_movie = None if len(user) < 5 else user[4]

        avatar = user[3].decode('utf-8') if user[3] else "None"

        return {"found": True, 
                "id" : user[0],
                "name" : user[1],
                "email": user[2],
                "avatar": avatar,
                "favorite_movie": favorite_movie}
    else:
        # get the password
        password = data.get("password")

        if not password:
            abort(400, "If email is used to look up user, password field is required.")

        user = DBService.getUserByEmail(connection, email, hash(password))
        print(user)

        if user == None:
            return {"found": False, "message": "User doesn't exist/password is wrong."}

        favorite_movie = None if len(user) < 5 else user[4]

        avatar = user[3].decode('utf-8') if user[3] else "None"

        return {"found": True, 
                "id" : user[0],
                "name" : user[1],
                "email": user[2],
                "avatar": avatar,
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

    if not (id and avatar):
        abort(400, "missing required field")

    ok, msg = DBService.updateAvatar(connection, id, avatar)

    return {"updated": ok, "message": msg}

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

    if not (id and name):
        abort(400, "missing required field")

    ok, msg = DBService.updateName(connection, id, name)

    return {"updated": ok, "message": msg} 

@app.route('/user/FavoriteMovie', methods=['POST'])
def addToFavorite():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    uid = data.get("id")
    mid = data.get("movie_id")

    if not (uid and mid):
        abort(400, "missing required field")

    result, msg = DBService.addToFavoriteMovie(connection, uid, mid)

    return {"added": result, "Message": msg}

@app.route('/user/FavoriteMovie', methods=['DELETE'])
def removeFromFavorite():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    uid = data.get("id")
    mid = data.get("movie_id")

    if not (uid and mid):
        abort(400, "missing required field")

    result = DBService.removeFromFavoriteMovie(connection, uid, mid)

    return {"removed:": result}

@app.route('/user/Friend', methods=['POST'])
def addFriend():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    uid1 = data.get("uid1")
    uid2 = data.get("uid2")

    if not (uid1 and uid2):
        abort(400, "missing required field")

    result, msg = DBService.addFriend(connection, uid1, uid2)

    return {"added": result, "message": msg}

@app.route('/user/Friend', methods=['DELETE'])
def removeFriend():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    uid1 = data.get("uid1")
    uid2 = data.get("uid2")

    if not (uid1 and uid2):
        abort(400, "missing required field")

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
    time = data.get("time")
    platform = data.get("platform")

    if not (uid and mid and date and time and platform):
        abort(400, "missing required field")
    
    if not is_valid_date(date):
        abort(400, "Invalid date format")

    result, msg, wid = DBService.createWatchParty(connection, uid, mid, date, time, platform)

    if not result:
        abort(400, msg)

    return {"created": result, "wid": wid}

@app.route('/user/WatchParty', methods=['GET'])
def getWatchParty():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    organizer = data.get("id")

    if not organizer:
        abort(400, "required field empty")

    queryresult = DBService.getUserWatchParty(connection, organizer)

    if queryresult == None:
        return {"message": "No watch party is created by this user"}
    
    result = []

    for watchParty in queryresult:
        result.append({"wid": watchParty[0],
                "ownerId": watchParty[1],
                "movieId": watchParty[2],
                "Date": watchParty[3],
                "atTime": watchParty[4].strftime('%H:%M'),
                "Platform": watchParty[5]
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

    if not wid:
        abort(400, "missing required field")

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

    participant = data.get("uid")
    wid = data.get("wid")

    if not (participant and wid):
        abort(400, "missing required field")

    result, msg = DBService.addToWatchParty(connection, participant, wid)

    return {"added": result, "message": msg}

@app.route('/user/joinWatchPartyWithNoID', methods=['POST'])
def participateWatchPartyWithNoId():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    participant = data.get("participantid")
    organizer = data.get("organizerID")
    movie = data.get("mid")
    date = data.get("date")

    if not (participant and organizer and movie and date):
        abort(400, "missing required field")

    result = DBService.addToWatchPartyWithNoId(connection, participant, organizer, movie, date)

    # TODO: make (organizer, mid, date) unique in sql table: UNIQUE(col1, col2, col3)

    return {"added": result}

@app.route('/user/getParticipatedWatchParty', methods=['GET'])
def getParticipatedWatchParty():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    participant = data.get("uid")

    if not participant:
        abort(400, "missing required field")

    queryresult = DBService.getUserParticipatedWatchParty(connection, participant)

    if queryresult == None:
        return {"message": "This user have no participated Watch Party"}
    
    result = []

    print(queryresult)

    for watchParty in queryresult:
        avatar = watchParty[7].decode('utf-8') if watchParty[7] else "None"
        result.append({"wid": watchParty[0],
                "ownerId": watchParty[1],
                "movieId": watchParty[2],
                "Date": watchParty[3],
                "time": watchParty[4].strftime('%H:%M'),
                "Platform": watchParty[5],
                "owner's Name": watchParty[6],
                "owner's avatar": avatar
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

    if not (uid and movie_id and content):
        abort(400, "missing required field")

    # Optional
    newWatchParty = data.get("newWatchParty", False)   # optional. true -> create new watchparty
    wid = 0

    print("content:", content)

    if (newWatchParty):
        date = data.get("date")
        platform = data.get("platform")
        time = data.get("time")

        if not (date and platform and time):
            abort(400, "missing required field")

        # TODO: check valid date string type (refer to CockroachDB). Return false if invalid
        if not is_valid_date(date):
            abort(400, "Invalid date format")

        ok, msg, wid = DBService.createWatchParty(connection, uid, movie_id, date, time, platform)

        if not ok:
            abort(400, msg)
    
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

    if not uid:
        abort(400, "missing required field")

    posts = DBService.getUserPost(connection, uid)

    result = []

    print("post:", posts)

    for p in posts:
        avatar = p[8].decode('utf-8') if p[8] else "None"
        result.append({"pid": p[0],
                       "writer": p[1],
                       "movie_id": p[2],
                       "pdate": p[3],
                       "ptime": p[4].strftime('%H:%M'),
                       "content": p[5],
                       "wid": p[6],
                       "writer's name": p[7],
                       "writer's avatar": avatar
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

    if not uid:
        abort(400, "missing required field")

    posts = DBService.getAllPost(connection, uid)

    result = []

    print("posts:", posts)

    for p in posts:
        avatar = p[8].decode('utf-8') if p[8] else "None"
        result.append({"pid": p[0],
                       "writer": p[1],
                       "movie_id": p[2],
                       "pdate": p[3],
                       "ptime": p[4].strftime('%H:%M'),
                       "content": p[5],
                       "wid": p[6],
                       "writer's name": p[7],
                       "writer's avatar": avatar
            })
        
    return {"result": result}

@app.route('/post', methods=['DELETE'])
def deletePost():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    # Required Fields:
    pid = data.get("pid")

    if not pid:
        abort(400, "missing required field")

    ok = DBService.deletePost(connection, pid)

    return {"deleted": ok}


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

    if not (uid and pid and content):
        abort(400, "missing required field")

    ok, msg = DBService.postComment(connection, uid, pid, content)

    return {"posted": ok, "cid/message": msg}

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
    if not pid:
        abort(400, "missing required field")

    comments = DBService.getComment(connection, pid)

    result = []

    for c in comments:
        avatar = c[7].decode('utf-8') if c[7] else "None"
        result.append({
            "cid": c[0],
            "pid": c[1],
            "content": c[2],
            "date": c[3],
            "time": c[4].strftime('%H:%M'),
            "user": c[5],
            "user name": c[6],
            "user's avatar": avatar
        })

    return {"result":result}


@app.route("/comment", methods=["DELETE"])
def deleteComment():
    data = {}

    if request.is_json:
        data = request.json
    else:
        print("received non-json object, converting to json")
        data = json.loads(request.data)

    # Required Fields:
    cid = data.get("cid")
    if not cid:
        abort(400, "missing required field")

    ok = DBService.deleteComment(connection, cid)

    return {"deleted": ok}

def ensure_pythonhashseed(seed='0'):
    current_seed = os.environ.get("PYTHONHASHSEED")

    if current_seed is None or current_seed != seed:
        print(f'Setting PYTHONHASHSEED="{seed}"')
        os.environ["PYTHONHASHSEED"] = seed
        # restart the current process
        os.execl(sys.executable, sys.executable, *sys.argv)

if __name__ == '__main__':
    # app.run(debug=True)
    ensure_pythonhashseed(credential_data["password_hash_key"])  # to ensure hash value stays consistent across all sessions and servers
    app.run(port=5002)