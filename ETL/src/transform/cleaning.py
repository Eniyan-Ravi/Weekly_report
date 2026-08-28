# Cleaning

def clean_orders(orders_df):

    #1.trim whitespace and standardize order_id
    orders_df["order_id"] = (orders_df["order_id"].str.strip().str.upper())

    #customer_id
    orders_df["customer_id"] = (orders_df["customer_id"].str.strip())

    #product_id
    orders_df["product_id"] = (orders_df["product_id"].str.strip())

    #currency
    orders_df["currency"] = (orders_df["currency"].str.strip().str.upper()
    )

    #2.Remove duplicate order_id
    orders_df = orders_df.drop_duplicates(subset=["order_id"],keep="first")
    return orders_df