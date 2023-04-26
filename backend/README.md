# MovieDate Backend Server Code

This directory contains backend server code for MovieDate application.

## Prerequite:

Before you can get this backend server code running, you must request a 'crudential.json' and 'CACert.sh' file from Ruihang to access the database in the cloud.

You must also have your ngrok account and configured it to your system. Read more [here](https://ngrok.com/).

Pre-requite dependency on your system: python3, ngrok, pip, homebrew <br>
* Note: After ngrok's installation, your ngrok's token must also be added to your system.

## Get it running:
0. (This is only required once.) run 'source ./CACert.sh" (be sure you are in the backend folder)
1. Once you have your 'crudential.json' file and ngrok configured, make sure you are in the 'backend' directory. Then simply run 'source ./init.sh' and enter your password as prompted in your command line to get the local flask server running. The 'init.sh' file will also ensure you have all of the backend dependency listed below.
2. After the flask server is running, open another terminal and use 'ngrok http 5002' to deploy your local server online.

Dependency: flask, flask-ngrok, psycopg[binary]

# Backend Architecture

![](https://i.imgur.com/prZvAuV.png)

# [CockroachDB ER diagram (Click to view)](https://docs.google.com/drawings/d/1RlKlOd8FNrVaUYEe0mKbFvWQwE01w1iYAO5jRxI3yEI/edit?usp=sharing)

Screenshot at Apr 26 (maybe out of date. Please use the link above to view the most updated ER):
![](https://i.imgur.com/OSZbOsV.png)