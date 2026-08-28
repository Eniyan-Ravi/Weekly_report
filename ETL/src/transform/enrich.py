def enrich_customers(customers_df):

    #9.email_present boolean
    customers_df["email_present"] = (customers_df["email"].notna())
    return customers_df


def enrich_orders(orders_df,exchange_rates,returns_df):

    #10.Currency exchange
    rates = exchange_rates["rates"]
    orders_df["rate_to_usd"] = (orders_df["currency"].map(rates))
    orders_df["amount_usd"] = (orders_df["amount"]* orders_df["rate_to_usd"]).round(2)

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

def enrich_products(products_df, exchange_rates):
    # Currency exchange
    rates = exchange_rates["rates"]
    products_df["rate_to_usd"] = (products_df["currency"].map(rates))
    products_df["unit_price_usd"] = (products_df["unit_price"]* products_df["rate_to_usd"]).round(2)

    # Price tier

    def classify_price(price):
        if price < 10:
            return "low"
        elif price < 100:
            return "medium"
        else:
            return "high"

    products_df["price_tier"] = (products_df["unit_price"].apply(classify_price))
    return products_df