Question 1:


Run docker and load image with python 3.13
docker run -it  python:3.13 /bin/bash

Find out what the pip version is :
pip -V 
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)

version is 25.3

Question 2:

Given the docker-compose.yaml file,  the hostname and port that pgadmin should use to connect to the postgres database is

db:5433

DATA PREPARATION:

wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

run a jupyter notebook to load and query data:

uv run jupyter notebook

Now I will start the postgresql container with a new database called docker_homework:


docker network creae pg-network 

# Run PostgreSQL on the network
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="docker_homework" \
  -v ny_docker_homework_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgserver \
  postgres:18

# In another terminal, run pgAdmin on the same network
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4


===========
Question 3:
===========
Now in pgadmin:

SELECT count(trip_distance) FROM public.green_taxi_data
WHERE lpep_pickup_datetime::date BETWEEN '2025-11-01' and '2025-11-30'
AND trip_distance<=1;

8007

===========
QUESTION 4
===========

SELECT lpep_pickup_datetime::date as pickup_date, trip_distance 
FROM public.green_taxi_data
WHERE trip_distance<=100
ORDER BY trip_distance DESC limit 1;

2025-11-14 with a distance of 88.03 miles

==========
QUESTION 5
==========

SELECT "Zone", sum(total_amount) as total from green_taxi_data a JOIN locations b 
ON ("LocationID"  = "PULocationID")
WHERE lpep_pickup_datetime::date = '2025-11-18'
GROUP BY "Zone" 
ORDER BY total DESC
LIMIT 1;

East Harlem North

==========
QUESTION 6
==========

SELECT "Zone", MAX(tip_amount) as max_tip from green_taxi_data a JOIN locations b 
ON ("LocationID"  = "DOLocationID")
WHERE lpep_pickup_datetime::date BETWEEN '2025-11-01' and '2025-11-30'
AND "PULocationID" = (SELECT "LocationID" FROM locations WHERE "Zone" = 'East Harlem North')
GROUP BY "Zone"
ORDER BY max_tip DESC
LIMIT 1;

Yorkville West with a tip of 81.89



