import pandas as pd
from src.utils.reject_logger import log_rejection


def validate_orders(orders_df,customers_df,products_df):
    valid_rows = orders_df.copy()

    #3.order_id, product_id, order_date must not be null
    required_columns = ["order_id","product_id","order_date"]
    invalid_rows = valid_rows[valid_rows[required_columns].isna().any(axis=1)]

    for index, row in invalid_rows.iterrows():
        log_rejection(row,"Missing required field")

    valid_rows = valid_rows[~valid_rows.index.isin(invalid_rows.index)]


    #4.customer_id must be present and must exist in customers
    invalid_rows = valid_rows[valid_rows["customer_id"].isna()
        |~valid_rows["customer_id"].isin(customers_df["customer_id"])]

    for index, row in invalid_rows.iterrows():
        if pd.isna(row["customer_id"]):
            reason = "Missing customer_id"
        else:
            reason = "Customer does not exist"

        log_rejection(row, reason)

    valid_rows = valid_rows[~valid_rows.index.isin(invalid_rows.index)]

    #5.quantity must be > 0
    quantity_numeric = pd.to_numeric(valid_rows["quantity"],errors="coerce")

    invalid_rows = valid_rows[quantity_numeric.isna()
        |
        (quantity_numeric <= 0)]
    for index, row in invalid_rows.iterrows():
        log_rejection(row,"Invalid quantity")

    valid_rows = valid_rows[~valid_rows.index.isin(invalid_rows.index)]

    #6.amount must be numeric and >= 0
    amount_numeric = pd.to_numeric(valid_rows["amount"],errors="coerce")
    invalid_rows = valid_rows[amount_numeric.isna()|(amount_numeric < 0)]
    for index, row in invalid_rows.iterrows():
        log_rejection(row,"Invalid amount")
    valid_rows = valid_rows[~valid_rows.index.isin(invalid_rows.index)]

    #7. Parse all three date formats
    date_formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m-%d-%Y"
    ]

    parsed_dates = pd.Series(pd.NaT,index=valid_rows.index)
    for date_format in date_formats:
        mask = parsed_dates.isna()
        parsed_dates.loc[mask] = pd.to_datetime(valid_rows.loc[mask, "order_date"],
            format=date_format,errors="coerce")
        
    # Find dates that could not be parsed
    invalid_rows = valid_rows[parsed_dates.isna()]
    for index, row in invalid_rows.iterrows():
        log_rejection(row,"Invalid order_date")

    # Keep only successfully parsed dates
    valid_rows["order_date"] = parsed_dates
    valid_rows = valid_rows[valid_rows["order_date"].notna()]


    #13.product_id must exist in products catalog
    invalid_rows = valid_rows[~valid_rows["product_id"].isin(products_df["product_id"])]
    for index, row in invalid_rows.iterrows():
        log_rejection(row,"Product does not exist")

    valid_rows = valid_rows[valid_rows["product_id"].isin(products_df["product_id"])]
    return valid_rows
