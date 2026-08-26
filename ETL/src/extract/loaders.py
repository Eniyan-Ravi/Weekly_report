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
    with open("data/raw/exchange_rates.json","r") as file:
        return json.load(file)


def load_web_events():

    web_events = pd.read_csv("data/raw/web_events.log",sep="|",header=None,
        names=["timestamp","session","customer_id","event","product"])

    web_events["session"] = (web_events["session"].str.split("=").str[1].str.strip())
    web_events["customer_id"] = (web_events["customer_id"].str.split("=").str[1].str.strip())
    web_events["event"] = (web_events["event"].str.split("=").str[1].str.strip())
    web_events["product"] = (web_events["product"].str.split("=").str[1].str.strip())

    return web_events

