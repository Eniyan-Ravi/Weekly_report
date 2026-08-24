from src.extract.loaders import *

orders_df = load_orders()
customers_df = load_customers()


#3.valicate order_id, product_id, order_date not null
required_columns = ["order_id","product_id","order_date"]

valid_rows = orders_df[orders_df[required_columns].notna().all(axis=1)]

#4.validate customer_id must be present and exist in customers
valid_rows = orders_df[ orders_df["customer_id"].notna()
    &
    orders_df["customer_id"].isin(customers_df["customer_id"])
]

#5.validate quantity must be >=0 and not blank
quantity_non_zero = pd.to_numeric(valid_rows["quantity"],errors="coerce")

valid_rows = valid_rows[

    (quantity_non_zero > 0)
]


#6.validate amount must be >=0 and not blank
amount_numeric = pd.to_numeric(valid_rows["amount"],errors="coerce")

valid_rows = valid_rows[
    amount_numeric.notna()
    &
    (amount_numeric >= 0)
]

# 7.Type cast order_date 

date_formats = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m-%d-%Y"
]

parsed_dates = pd.Series(pd.NaT, index=valid_rows.index)
x = parsed_dates.isna()

for date_format in date_formats:

    parsed_dates.loc[x] = pd.to_datetime(
        valid_rows.loc[x, "order_date"],
        format=date_format,
        errors="coerce"
    )

valid_rows["order_date"] = parsed_dates

# removing NaN i.e the dates which didn't parse
valid_rows = valid_rows[
    valid_rows["order_date"].notna()
]
print(valid_rows.to_string())

