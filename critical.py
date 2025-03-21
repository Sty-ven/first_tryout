import wget
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
taxi = wget.download(url)

empty_df = []
for month in range(1, 13):
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-{:02d}.parquet".format(
        month
    )
    table = wget.download(url)  # downloads the parquet file
    df = pq.read_table(table)  # this reads the parquet file
    df = df.to_pandas()  # converts pyarrow table to pandas dataframe
    empty_df.append(df)
final_df = pd.concat(empty_df)
subset_df = final_df.iloc[:10000, :]

con = create_engine("postgresql://admin:admin@sample_postgres/silent")

subset_df.to_sql("trip-data", con, if_exists="replace")
