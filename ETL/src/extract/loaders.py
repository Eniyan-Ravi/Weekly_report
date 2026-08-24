# Loading the raw datasets

import json
import pandas as pd


def load_orders():
    return pd.read_csv("data/raw/orders.csv")


def load_customers():
    return pd.read_json("data/raw/customers.json")


def load_products():
    return pd.read_csv("data/raw/products.csv",sep="|")


def load_returns():
    return pd.read_csv("data/raw/returns.tsv",sep="\t")


def load_exchange_rates():
    with open(
        "data/raw/exchange_rates.json","r"
    ) as file:
        return json.load(file)


def load_web_events():
    with open(
        "ETL/data/raw/web_events.log","r"
    ) as file:
        return file.readlines()