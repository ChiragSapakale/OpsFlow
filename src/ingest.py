import pandas as pd

from src.clean import (
    clean_orders,
    clean_products,
    remove_duplicates,
    data_quality_summary,
)

customers = pd.read_csv("data/raw/olist_customers_dataset.csv")
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
order_items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")
products = pd.read_csv("data/raw/olist_products_dataset.csv")


customers = remove_duplicates(customers)
orders = clean_orders(remove_duplicates(orders))
order_items = remove_duplicates(order_items)
payments = remove_duplicates(payments)
products = clean_products(remove_duplicates(products))


print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Order items:", order_items.shape)
print("Payments:", payments.shape)
print("Products:", products.shape)
print("\nData quality summary:")

datasets = {
    "customers": customers,
    "orders": orders,
    "order_items": order_items,
    "payments": payments,
    "products": products,
}

quality_reports = []

for name, df in datasets.items():
    quality_reports.append(data_quality_summary(df, name))

quality_df = pd.DataFrame(quality_reports)

print(quality_df)

quality_df.to_csv(
    "data/rejected/data_quality_report.csv",
    index=False
)