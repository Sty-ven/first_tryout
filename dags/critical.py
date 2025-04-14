import wget
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine
from time import time
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def download_and_write_csv():
    empty_df = []
    for month in range(1, 13):
        url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-{month:02d}.parquet'
        table = wget.download(url)
        df = pq.read_table(table).to_pandas()
        empty_df.append(df)

    final_df = pd.concat(empty_df)
    final_df.to_csv("taxi.csv", index=False)
    print("CSV file written.")

def upload_to_postgres():
    con = create_engine("postgresql://admin:admin@taxi_data:5432/trips")
    df_iter = pd.read_csv("taxi.csv", chunksize=100000)

    for i, chunk in enumerate(df_iter):
        start_time = time()
        chunk.to_sql("trip_data", con, if_exists="append", index=False)
        end_time = time()
        print(f"Chunk {i+1} uploaded in {round(end_time - start_time, 2)} seconds.")

# Define the DAG
with DAG(
    dag_id="taxi_trip_dag",
    start_date=datetime(2025, 4, 8),
    schedule_interval="@daily",
    catchup=False
) as dag:

    download_task = PythonOperator(
        task_id="download_and_write_csv",
        python_callable=download_and_write_csv,
    )

    upload_task = PythonOperator(
        task_id="upload_to_postgres",
        python_callable=upload_to_postgres,
    )

    download_task >> upload_task
