from time import time

import wget
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine

from _datetime import datetime

from airflow.models import DAG
from airflow.operators.python import PythonOperator


dag = DAG(
 dag_id="my_dag_name",
 start_date=datetime(2025, 4, 1),
 schedule="@daily",
 catchup= False
)

def download_write_data():
    empty_df = []
    for month in range(1, 13):
        url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-{:02d}.parquet".format(
            month
        )
        table = wget.download(url)  # downloads the parquet file
        df = pq.read_table(table)#reads parquet filedf_iter = pd.read_csv("../taxi.csv", chunksize=100000)
        _dff = df.to_pandas() # converts pyarrow table to pandas dataframe
        empty_df.append(_dff)
    final_df = pd.concat(empty_df)
    print(final_df.head())
    final_df.to_csv("taxi.csv", index=False) #put data into a csv file
    #read csv ile

# def send_to_database():
#     con = create_engine("postgresql://admin:admin@sample_postgres/silent")
#     con.connect()
#     df_iter = pd.read_csv("../taxi.csv", chunksize=100000)
#
#     i=0
#     for part in enumerate(df_iter):
#         i=+1
#         start_time = time()
#         part.to_sql("trip_data", con=con, if_exists="append",index=False)
#         end_time = time()
#         elapsed_time=start_time-end_time
#         print(f"Chunk {i+1} was inserted in {elapsed_time, 2} seconds")

# with dag:
#     DOWNLOAD_WRITE_DATA=download_write_data()
#
#     SEND_TO_DATABASE=send_to_database()
#
# DOWNLOAD_WRITE_DATA>>SEND_TO_DATABASE
download_task = PythonOperator(
    task_id="download_write_data",
    python_callable=download_write_data,
    dag=dag
)
#
# send_task = PythonOperator(
#     task_id="send_to_database",
#     python_callable=send_to_database,
#     dag=dag,
# )
#
download_task