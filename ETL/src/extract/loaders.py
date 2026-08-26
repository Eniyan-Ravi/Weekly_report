# Loading the raw datasets

import json
import pandas as pd
from pathlib import Path

# ETL project root
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "raw"

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
    with open("data/raw/web_events.log","r") as file:
        return file.readlines()

