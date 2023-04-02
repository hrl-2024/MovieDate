# To run this, use 'source ./init.sh' command

pip3 install "psycopg[binary]"
python3 -m pip install flask

DATABASE_URL=$(jq .General_connection_string crudential.json)
echo $DATABASE_URL
export DATABASE_URL=$DATABASE_URL
#export | grep DATABASE_URL

# create the database
python3 create.py

export Database_Path='./database_layer'

cd api_layer
python3 -m flask run