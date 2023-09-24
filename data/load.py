import pandas as pd
import pystore


history = pd.read_csv("data/sales_df_train.csv", parse_dates=[2], index_col="date")
pystore.set_path("/home/kubanez/Dev/Lenta_TS_backend/data/pystore")
store = pystore.store("mydatastore")
collection_his = store.collection("lenta.eod")
collection.write("history", history[:-1], metadata={"source": "initial"})
collection.append("history", history[-1:])

forecast = pd.read_csv("data/sales_df_train.csv", parse_dates=[2], index_col="date")
collection_fut = store.collection("lenta.fc")
collection.write("future", forecast)

item = collection_his.item("history")
df = item.to_pandas()
print(df.head())
