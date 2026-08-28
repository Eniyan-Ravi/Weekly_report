import sqlite3


def load_to_sqlite(
    fact_sales,
    dim_customers,
    dim_products,
    feature_customers
):


    connection = sqlite3.connect("data/warehouse/novacart.db")


    # Load fact_sales
    fact_sales.to_sql("fact_sales",connection,if_exists="replace",index=False)


    # Load dim_customers
    dim_customers.to_sql("dim_customers",connection,if_exists="replace",index=False)


    # Load dim_products
    dim_products.to_sql("dim_products",connection,if_exists="replace",index=False)

    # Load feature_customers
    feature_customers.to_sql("feature_customers",connection,if_exists="replace",index=False)

    connection.close()
    print("All tables loaded successfully.")