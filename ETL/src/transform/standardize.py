def standardize_customers(customers_df):
    #8.Extract city from nested address
    customers_df["city"] = customers_df["address"].apply(
        lambda x: x["city"]
    )

    city_country_mapping = {
        "New York": "USA",
        "Mumbai": "India",
        "Chennai": "India",
        "Berlin": "Germany",
        "London": "UK"
    }

    # Standardize country
    customers_df["country"] = customers_df["city"].map(city_country_mapping)
    return customers_df