import pandas as pd


def validate_orders(orders_df,customers_df,products_df):

    #3.order_id, product_id, order_date must not be null
    required_columns = ["order_id","product_id","order_date"]
    valid_rows = orders_df[orders_df[required_columns].notna().all(axis=1)]


    #4.customer_id must be present and must exist in customers
    valid_rows = valid_rows[valid_rows["customer_id"].notna()
        &
        valid_rows["customer_id"].isin(customers_df["customer_id"])]


    #5.quantity must be > 0
    quantity_numeric = pd.to_numeric(valid_rows["quantity"],errors="coerce")
    valid_rows = valid_rows[quantity_numeric.notna()
        &
        (quantity_numeric > 0)]

    #6.amount must be numeric and >= 0
    amount_numeric = pd.to_numeric(valid_rows["amount"],errors="coerce")
    valid_rows = valid_rows[amount_numeric.notna()
        &
        (amount_numeric >= 0)]


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
            format=date_format,errors="coerce"
        )
    valid_rows["order_date"] = parsed_dates

    # Remove dates that could not be parsed

    valid_rows = valid_rows[
        valid_rows["order_date"].notna()
    ]

    #13.product_id must exist in products catalog
    valid_rows = valid_rows[valid_rows["product_id"].isin(products_df["product_id"])]
    return valid_rows