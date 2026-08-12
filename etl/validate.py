import pandas as pd


REQUIRED_COLUMNS = [
    "order_id",
    "date",
    "customer_name",
    "customer_phone",
    "product_name",
    "quantity",
    "unit_price",
    "status",
]

VALID_STATUSES = {
    "Pending",
    "Confirmed",
    "Delivered",
    "Cancelled",
}


def validate_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate raw order data before transformation.
    """

    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df["order_id"].duplicated().any():
        duplicates = df.loc[
            df["order_id"].duplicated(),
            "order_id"
        ].tolist()

        raise ValueError(
            f"Duplicate order IDs found: {duplicates}"
        )

    if (df["quantity"] <= 0).any():
        raise ValueError(
            "Quantity must be greater than zero."
        )

    if (df["unit_price"] < 0).any():
        raise ValueError(
            "Unit price cannot be negative."
        )

    invalid_statuses = set(df["status"]) - VALID_STATUSES

    if invalid_statuses:
        raise ValueError(
            f"Invalid statuses: {invalid_statuses}"
        )

    if df["customer_name"].isna().any():
        raise ValueError(
            "Customer name cannot be empty."
        )

    if df["product_name"].isna().any():
        raise ValueError(
            "Product name cannot be empty."
        )

    print("Validation successful")

    return df