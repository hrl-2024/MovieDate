#pip3 install "psycopg[binary]"

DATABASE_URL=$(jq .General_connection_string crudential.json)
export DATABASE_URL=$DATABASE_URL
#export | grep DATABASE_URL