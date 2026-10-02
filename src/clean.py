import pandas as pd

def clean_orders(df):
    df = df.copy()

    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    return df

def clean_products(df):
    df = df.copy()

    df = df.rename(columns={
        "product_name_lenght": "product_name_length",
        "product_description_lenght": "product_description_length",
    })

    df["product_category_name"] = df["product_category_name"].fillna("unknown")

    return df

def remove_duplicates(df):
    df = df.copy()
    df = df.drop_duplicates()

    return df

def data_quality_summary(df, name):
    return {
        "dataset": name,
        "rows": len(df),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": int(df.isnull().sum().sum()),
    }