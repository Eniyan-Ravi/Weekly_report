# Prepare final warehouse tables


def create_fact_sales(orders_df):
    fact_sales = orders_df[
        [
            "order_id",
            "customer_id",
            "product_id",
            "quantity",
            "amount",
            "currency",
            "amount_usd",
            "order_date",
            "price_tier",
            "net_revenue",
            "is_returned"
        ]
    ].copy()
    return fact_sales


def create_dim_customers(customers_df):
    dim_customers = customers_df[
        [
            "customer_id",
            "name",
            "email_present",
            "city",
            "country",
            "is_premium",
            "signup_date"
        ]
    ].copy()
    return dim_customers


def create_dim_products(products_df):
    dim_products = products_df[
        [
            "product_id",
            "product_name",
            "category",
            "unit_price",
            "currency",
            "unit_price_usd",
            "price_tier"
        ]
    ].copy()
    return dim_products