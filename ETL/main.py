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
from src.transform.enrich import (enrich_customers,enrich_orders)
from src.transform.business_rules import (apply_business_rules)
from src.transform.aggregate import (aggregate_customers,aggregate_web_events)
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


#  6. Business Rules
orders_df = apply_business_rules(orders_df,products_df)


# 7. Aggrigate
reference_date = pd.Timestamp(datetime.now().date())
web_features = aggregate_web_events(web_events)

feature_customers = aggregate_customers(orders_df,reference_date)
feature_customers = feature_customers.merge(web_features,on="customer_id",how="left")

# Result

print("\n Orders")
print(orders_df.to_string())

print("\n Customers")
print(customers_df.to_string())

print("\nFeature Customers")
print(feature_customers.to_string())