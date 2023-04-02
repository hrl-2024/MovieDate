import logging
import os
import psycopg
from psycopg.errors import ProgrammingError
from flask import Flask, request, json
import json
import atexit    # Gracefully exit and cleanup after normal termination

# Need to import database_layer's service.py
import importlib.util
import sys
spec = importlib.util.spec_from_file_location("service", "../database_layer/service.py")
DBService = importlib.util.module_from_spec(spec)
sys.modules["service"] = DBService
spec.loader.exec_module(DBService)

app = Flask(__name__)

# get crudential
credential_file = open("../crudential.json")
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
