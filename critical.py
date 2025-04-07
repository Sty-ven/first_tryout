import wget
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine

con = create_engine("postgresql://admin:admin@TaxiData/trips")

chunk_size = 150000
empty_df = []

for month in range(1, 13):
    url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-{:02d}.parquet'.format(month)
    table = wget.download(url)
    df = pq.read_table(table)
    df = df.to_pandas()
    empty_df.append(df)
    final_df = pd.concat(empty_df, ignore_index=True)

    for i in range(0, len(final_df), chunk_size):
        chunk = final_df.iloc[i:i + chunk_size]
        chunk.to_sql('yellow_tripdata', con=con, if_exists='append', index=False)
        print(f'Uploaded chunk {i // chunk_size + 1} of {final_df}')