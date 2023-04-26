# To run this, use 'source ./init.sh' command

# install all dependencies:
pip3 install "psycopg[binary]"
python3 -m pip install flask
brew install ngrok/ngrok/ngrok
pip3 install flask-ngrok

DATABASE_URL=$(jq .General_connection_string crudential.json)
echo $DATABASE_URL
export DATABASE_URL=$DATABASE_URL
#export | grep DATABASE_URL

# create the database
python3 create.py

sudo python3 api_layer/api.py