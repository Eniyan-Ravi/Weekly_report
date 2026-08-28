from datetime import datetime

from src.extract.loaders import (
    load_orders,
    load_customers,
    load_products,
    load_returns,
    load_exchange_rates,
    load_web_events
)

from src.transform.cleaning import (clean_orders)
from src.transform.validation import (validate_orders)
from src.transform.standardize import (standardize_customers)
from src.transform.enrich import (enrich_customers,enrich_orders,enrich_products)
from src.transform.business_rules import (apply_business_rules)
from src.transform.aggregate import (aggregate_customers,aggregate_web_events)
from src.load.tables import (create_fact_sales,create_dim_customers,create_dim_products)
from src.load.load_to_sqlite import (load_to_sqlite)
import pandas as pd

# 1. Extract
orders_df = load_orders()
customers_df = load_customers()
products_df = load_products()
returns_df = load_returns()
exchange_rates = load_exchange_rates()
web_events = load_web_events()

# 2. Clean
orders_df = clean_orders(orders_df)

# 3. Validate
orders_df = validate_orders(orders_df,customers_df,products_df)

# 4. Standardize
customers_df = standardize_customers(customers_df)

# 5. Enrich
customers_df = enrich_customers(customers_df)
orders_df = enrich_orders(orders_df,exchange_rates,returns_df)
products_df = enrich_products(products_df,exchange_rates)


#  6. Business Rules
orders_df = apply_business_rules(orders_df,products_df)


# 7. Aggregate
reference_date = pd.Timestamp(datetime.now().date())
web_features = aggregate_web_events(web_events)

feature_customers = aggregate_customers(orders_df,reference_date)
feature_customers = feature_customers.merge(web_features,on="customer_id",how="left")

# 8. Prepare Final Tables
fact_sales = create_fact_sales(orders_df)
dim_customers = create_dim_customers(customers_df)
dim_products = create_dim_products(products_df)

#9. Load to SQLite
load_to_sqlite(fact_sales,dim_customers,dim_products,feature_customers)


# Result

print("\n Fact Sales")
print(fact_sales.to_string())

print("\n Dim Customers")
print(dim_customers.to_string())

print("\n Dim Products")
print(dim_products.to_string())

print("\nFeature Customers")
print(feature_customers.to_string())

