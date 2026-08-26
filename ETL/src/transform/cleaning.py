# Cleaning

def clean_orders(orders_df):

    #1.trim whitespace and standardize order_id
    orders_df["order_id"] = (
        orders_df["order_id"]
        .str.strip()
        .str.upper()
    )

    #2.remove duplicate order_id
    orders_df = orders_df.drop_duplicates(
        subset=["order_id"],
        keep="first"
    )
    return orders_df