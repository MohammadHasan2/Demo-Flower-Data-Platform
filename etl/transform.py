import pandas as pd


def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and transform validated order data.
    """

    df = df.copy()

    # Normalize text
    df["customer_name"] = (
        df["customer_name"]
        .str.strip()
    )

    df["product_name"] = (
        df["product_name"]
        .str.strip()
    )

    df["status"] = (
        df["status"]
        .str.strip()
        .str.title()
    )

    # Convert date
    df["date"] = pd.to_datetime(
        df["date"],
        errors="raise"
    )

    # Ensure numeric types
    df["quantity"] = df["quantity"].astype(int)

    df["unit_price"] = df["unit_price"].astype(float)

    # Calculate order item subtotal
    df["subtotal"] = (
        df["quantity"] * df["unit_price"]
    )

    print("Transformation successful")

    return df