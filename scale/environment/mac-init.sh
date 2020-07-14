#!/usr/bin/env bash

export SCALE_DB_PORT=55432
export SCALE_MESSAGE_PORT=55672
export SCALE_DB_PASS=scale-postgres

# Launch a database for Scale testing
docker run -d --restart=always -p ${SCALE_DB_PORT}:5432 --name scale-postgis \
    -e POSTGRES_PASSWORD=${SCALE_DB_PASS} mdillon/postgis:9.4-alpine
echo Giving Postgres a moment to start up before initializing...
sleep 10

docker run -d --restart=always -p ${SCALE_MESSAGE_PORT}:5672 --name scale-rabbitmq \
    rabbitmq:3.6-management

# Configure database
cat << EOF > database-commands.sql
CREATE USER scale PASSWORD 'scale' SUPERUSER;
CREATE DATABASE scale OWNER=scale;
EOF
docker cp database-commands.sql scale-postgis:/database-commands.sql
rm database-commands.sql
docker exec -it scale-postgis su postgres -c 'psql -f /database-commands.sql'
docker exec -it scale-postgis su postgres -c 'psql scale -c "CREATE EXTENSION postgis;"'

# Install all python dependencies
brew install gdal
brew install libgeoip
brew install postgresql

cp scale/local_settings_dev.py scale/local_settings.py
cat << EOF >> scale/local_settings.py
BROKER_URL = 'amqp://guest:guest@localhost:${SCALE_MESSAGE_PORT}//'

POSTGIS_TEMPLATE = 'template_postgis'

DATABASES = {'default': dj_database_url.config(default='postgis://scale:scale@localhost:${SCALE_DB_PORT}/scale')}
EOF

# Initialize virtual environment
pip install virtualenv
python2 -m virtualenv -p $(which python2) environment/scale
cat pip/requirements.txt | sed 's^psycopg2^psycopg2-binary^' > pip/mac.txt
environment/scale/bin/pip install -r pip/mac.txt

# Load up database with schema migrations to date and fixtures
environment/scale/bin/python manage.py migrate
environment/scale/bin/python manage.py load_all_data
