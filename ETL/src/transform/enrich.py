def enrich_customers(customers_df):

    #9.email_present boolean

    customers_df["email_present"] = (customers_df["email"].notna())

    return customers_df


def enrich_orders(orders_df,exchange_rates,returns_df):

    #10.Currency exchange

    rates = exchange_rates["rates"]

    orders_df["rate_to_usd"] = (orders_df["currency"].map(rates))

    orders_df["amount_usd"] = (orders_df["amount"]* orders_df["rate_to_usd"])


    # 14.order_id vs returns . Left join returns

    returned_orders = returns_df[["order_id"]].drop_duplicates()


    orders_df = orders_df.merge(returned_orders,
        on="order_id",
        how="left",
        indicator=True
    )

    orders_df["is_returned"] = (orders_df["_merge"] == "both")


    orders_df = orders_df.drop(columns=["_merge"])

    return orders_df