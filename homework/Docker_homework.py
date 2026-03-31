#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import click
import pyarrow.parquet as pq
from sqlalchemy import create_engine


def do_zones(engine):
    df1 = pd.read_csv('taxi_zone_lookup.csv')
    print(df1.head())

    # Check data types
    print(df1.dtypes)
    # Check data shape
    print(df1.shape)
    # Here we read the locations file. Since it's small, we just post it all at once to the database using to_sql()
    df1.to_sql(name='locations', con=engine, if_exists='replace')

def do_taxi_data(engine):
    # Now the parquet file...
    df2 = pd.read_parquet('green_tripdata_2025-11.parquet')

    print(df2.head())
    # Check data types
    print(df2.dtypes)
    # Check data shape
    print(df2.shape)

    # Here me read the parquet file and post it's content to the database table, all records at once
    # 
    # df2.to_sql(name='green_taxi_data', con=engine, if_exists='replace')
    # print(pd.io.sql.get_schema(df2, name='green_taxi_data', con=engine))

    # This ir our improved code, also scalable. If the parquet file is too large, it's better to read it using chunks... 

    engine = create_engine('postgresql+psycopg://root:root@localhost:5432/docker_homework')
    parquet_file = pq.ParquetFile('green_tripdata_2025-11.parquet')
    print(parquet_file.schema)
    batch_size = 10000  # adjust based on your memory
    first_batch = True

    for batch in parquet_file.iter_batches(batch_size=batch_size):
        df_chunk = batch.to_pandas()

        df_chunk.to_sql(
            name='green_taxi_data',
            con=engine,
            if_exists='replace' if first_batch else 'append',
            index=False
        )
        print("Inserted:", len(df_chunk))
        first_batch = False


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='docker_homework', help='PostgreSQL database name')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db):
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    do_zones(engine)
    do_taxi_data(engine)
    

if __name__ == '__main__':
    run()