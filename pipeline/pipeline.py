import pandas as pd
import sys

df = pd.DataFrame({"Terminal": [1, 2], "Passengers": [3, 4]})
print(df.head())

df.to_parquet(f"output_day_{sys.argv[1]}.parquet")