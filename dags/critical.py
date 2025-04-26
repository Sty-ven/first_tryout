from time import time

import wget
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine

from _datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


dag = DAG(
 dag_id="my_dag_name",
 start_date=datetime(2025, 4, 1),
 schedule="@daily",
)

@dag
def download_write_data():
    empty_df = []
    for month in range(1, 13):
        url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-{:02d}.parquet".format(
            month
        )
        table = wget.download(url)  # downloads the parquet file
        df = pq.read_table(table)#reads parquet file
        _dff = df.to_pandas() # converts pyarrow table to pandas dataframe
        empty_df.append(_dff)
    final_df = pd.concat(empty_df)
    # print(final_df.head())
    final_df.to_csv("taxi.csv", index=False) #put data into a csv file
    #read csv ile

@dag
def send_to_database():
    df_iter = pd.read_csv("../taxi.csv", chunksize=100000)
    while True:
        try:
            con = create_engine("postgresql://admin:admin@sample_postgres/silent")
            con.connect()
            df=next(df_iter)
            start_time = time()
            df.to_sql("trip_data", con=con, if_exists="append")
            end_time = time()
            elapsed_time=start_time-end_time
            print(f"100000 rows was print as in{elapsed_time} seconds")
        except Exception:
            print("The insertion was unsuccessful")

with dag:
    DOWNLOAD_WRITE_DATA=download_write_data()

    SEND_TO_DATABASE=send_to_database()

DOWNLOAD_WRITE_DATA>>SEND_TO_DATABASE