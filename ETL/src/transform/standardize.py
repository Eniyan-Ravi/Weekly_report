from src.extract.loaders import *

orders_df = load_orders()
customers_df = load_customers()


#To map variants to country 


# Extract city and country from address
customers_df["city"] = customers_df["address"].apply(
    lambda x: x.get("city")
)

customers_df["country"] = customers_df["address"].apply(
    lambda x: x.get("country")
)

print("Cities:")
print(set(customers_df["city"]))

print("\nCountries:")
print(set(customers_df["country"]))
#---------------------------------------------------------------------------------
# Extract city from address
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

# Update country based on city

customers_df["country"] = customers_df["city"].map(
    city_country_mapping
)

print(customers_df[["customer_id", "city", "country"]].to_string())