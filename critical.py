import wget
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine
from time import time

empty_df = []
for month in range(1, 2):
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-{:02d}.parquet".format(
        month
    )
    table = wget.download(url)  # downloads the parquet file
    df = pq.read_table(table)  # this reads the parquet file
    df = df.to_pandas()  # converts pyarrow table to pandas dataframe
    empty_df.append(df)
final_df = pd.concat(empty_df)
print(final_df.head(5))
final_df = final_df.to_csv("taxi.csv", index=False)

# read csv file
df_iter = pd.read_csv("taxi.csv", chunksize=100000)


while True:
    try:
        df = next(df_iter)
        con = create_engine("postgresql://admin:admin@sample_postgres/silent")

        start_time = time()
        df.to_sql("trip-data", con, if_exists="append", index=False)
        end_time = time()

        elapsed_time = end_time - start_time
        print(f"100000 rows was inserted in {elapsed_time} seconds")
    except Exception:
        print("The insertion was unsuccessful")


