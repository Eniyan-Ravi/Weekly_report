#Removing leading/trailing whitespace from order_id(1)
from src.extract.loaders import load_orders

orders_df = load_orders()

#For removing leading/triling whitespace
orders_df["order_id"] = (orders_df["order_id"].str.strip().str.upper())

#Droping duplicate from order_id (keep first)
deduplicated_orders_df = orders_df.drop_duplicates(subset=["order_id"],keep="first")


