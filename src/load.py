import pandas as pd
from sqlalchemy import create_engine, text
from src.clean import clean_products
from src.clean import clean_products, clean_orders

def get_engine():
    engine = create_engine(
        "postgresql+psycopg2://prakalp@localhost/opsflow"
    )

    return engine

def test_connection():
    engine = get_engine()

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful:", result.scalar())

def load_customers():
    engine = get_engine()

    customers = pd.read_csv(
        "data/raw/olist_customers_dataset.csv"
    )

    customers.to_sql(
        "customers",
        engine,
        if_exists="append",
        index=False
    )

    print("Customers loaded successfully")

def load_products():
    engine = get_engine()

    products = pd.read_csv(
        "data/raw/olist_products_dataset.csv"
    )

    products = clean_products(products)

    products.to_sql(
        "products",
        engine,
        if_exists="append",
        index=False
    )

    print("Products loaded successfully")    

def load_orders():
    engine = get_engine()

    orders = pd.read_csv(
        "data/raw/olist_orders_dataset.csv"
    )

    orders = clean_orders(orders)

    orders.to_sql(
        "orders",
        engine,
        if_exists="append",
        index=False
    )

    print("Orders loaded successfully")

def load_order_items():
    engine = get_engine()

    order_items = pd.read_csv(
        "data/raw/olist_order_items_dataset.csv"
    )

    order_items.to_sql(
        "order_items",
        engine,
        if_exists="append",
        index=False
    )

    print("Order items loaded successfully")

def load_payments():
    engine = get_engine()

    payments = pd.read_csv(
        "data/raw/olist_order_payments_dataset.csv"
    )

    payments.to_sql(
        "payments",
        engine,
        if_exists="append",
        index=False
    )

    print("Payments loaded successfully")

if __name__ == "__main__":
    test_connection()
    load_payments()

