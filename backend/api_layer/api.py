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
    print(name)
    id = DBService.insert_user(connection, name)
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

@app.route("/user/updateAvatar", methods=['POST'])
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

    return {"added:": result} 

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

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(port=5002)