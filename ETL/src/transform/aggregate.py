import pandas as pd


def aggregate_customers(orders_df,reference_date):

    #15:Aggregate per customer

    feature_customers = (orders_df.groupby("customer_id").agg(
            total_orders=("order_id","nunique"),

            total_spend_usd=("amount_usd","sum"),

            avg_order_value=("amount_usd","mean"),

            return_rate=("is_returned","mean"),

            last_order_date=("order_date","max")
        ).reset_index()
    )


    # Days since last order

    feature_customers["days_since_last_order"] = (reference_date-feature_customers["last_order_date"]).dt.days

    # Remove last_order_date

    feature_customers = feature_customers.drop(columns=["last_order_date"])
    
    return feature_customers