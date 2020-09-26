#!bin/sh

while ! nc -zw1 postgres 5432
do
  echo "Waiting for connection to postgres"
  sleep 1
done

python -m scripts.create_database
alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 8080
