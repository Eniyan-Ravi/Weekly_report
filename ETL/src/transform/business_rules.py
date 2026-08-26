def apply_business_rules(
    orders_df,
    products_df
):

    # Get product price

    orders_df = orders_df.merge(
        products_df[
            ["product_id", "unit_price"]],
        on="product_id",
        how="left"
    )


    # Assumption:
    # discount is 8%

    orders_df["discount"] = 8


    # Rule 11:
    # total = quantity * price

    orders_df["total"] = (
        orders_df["quantity"]
        * orders_df["unit_price"]
    )


    # discount_value

    orders_df["discount_value"] = (
        orders_df["total"]
        * orders_df["discount"]
        / 100
    )


    # net_revenue

    orders_df["net_revenue"] = (
        orders_df["total"]
        - orders_df["discount_value"]
    )


    # Rule 12:
    # price tier

    def classify_price(price):

        if price < 10:
            return "low"

        elif price < 100:
            return "medium"

        else:
            return "high"


    orders_df["price_tier"] = (
        orders_df["unit_price"]
        .apply(classify_price)
    )


    return orders_df