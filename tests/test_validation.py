import pandas as pd

from src.validate import (
    validate_required_columns,
    find_missing_required_values,
    find_negative_values,
)

def test_validate_required_columns():
    df = pd.DataFrame({
        "order_id": [1, 2],
        "customer_id": [10, 20]
    })

    missing = validate_required_columns(
        df,
        ["order_id", "customer_id", "order_status"]
    )

    assert missing == ["order_status"]

def test_find_missing_required_values():
    df = pd.DataFrame({
        "order_id": [1, 2],
        "customer_id": [10, None]
    })

    invalid = find_missing_required_values(
        df,
        ["order_id", "customer_id"]
    )

    assert len(invalid) == 1

def test_find_negative_values():
    df = pd.DataFrame({
        "price": [10.0, -5.0],
        "freight_value": [2.0, 3.0]
    })

    invalid = find_negative_values(
        df,
        ["price", "freight_value"]
    )

    assert len(invalid) == 1
