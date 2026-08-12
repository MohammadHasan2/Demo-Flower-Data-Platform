import pandas as pd


def extract_orders(source: str) -> pd.DataFrame:
    """
    Extract orders from a CSV file or URL.
    """

    df = pd.read_csv(
        source,
        dtype={
            "customer_phone": "string"
        }
    )

    print(
        f"Extracted {len(df)} orders"
    )

    return df