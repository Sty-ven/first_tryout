import wget
import pyarrow.parquet as pq
url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
table = wget.download(url)
df = pq.read_table(table)
df= df.to_pandas()
print(df.columns)

