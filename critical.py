import wget
import pyarrow.parquet as pq
import pandas as pd
from sqlalchemy import create_engine
import os

taxi_data = r'C:\Users\oluwa\Documents\Hemie\Project\Docker\TLCTripRecordData\taxi_data'
os.makedirs(taxi_data, exist_ok=True)

con = create_engine('postgresql://admin:admin@NewYorkTaxiData:5433/taxi_data')

chunk_size = 150000
empty_df = []

for month in range(1, 13):
    url = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-{:02d}.parquet'.format(month)
    file_path = os.path.join(taxi_data, f'yellow_tripdata_2024-{month:02d}.parquet')

    if not os.path.exists(file_path):
        wget.download(url, file_path)
    table = pq.read_table(file_path)
    df = table.to_pandas()
    empty_df.append(df)
    final_df = pd.concat(empty_df, ignore_index=True)

    for i in range(0, len(final_df), chunk_size):
        chunk = final_df.iloc[i:i + chunk_size]
        chunk.to_sql('yellow_tripdata', con=con, if_exists='append', index=False)
        print(f'Uploaded chunk {i // chunk_size + 1} of {file_path}')

