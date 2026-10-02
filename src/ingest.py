import pandas as pd

files = {
    "customers": "data/raw/olist_customers_dataset.csv",
    "orders": "data/raw/olist_orders_dataset.csv",
    "order_items": "data/raw/olist_order_items_dataset.csv",
    "payments": "data/raw/olist_order_payments_dataset.csv",
    "products": "data/raw/olist_products_dataset.csv",
}

for name, path in files.items():
    df = pd.read_csv(path)

    print(f"\n--- {name.upper()} ---")
    print("Shape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing values:")
    print(df.isnull().sum())
    
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")

print("\n--- ORDER STATUS COUNTS ---")
print(orders["order_status"].value_counts())

print("\n--- DUPLICATES ---")

for name, path in files.items():
    df = pd.read_csv(path)

    print(
        name,
        "exact duplicate rows:",
        df.duplicated().sum()
    )