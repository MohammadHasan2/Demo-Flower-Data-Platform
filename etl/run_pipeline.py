import os

from dotenv import load_dotenv

from database.connection import engine

from etl.extract import extract_orders
from etl.validate import validate_orders
from etl.transform import transform_orders

from etl.load import (
    load_customers,
    load_products,
    load_orders
)

from etl.logger import (
    start_etl_run,
    complete_etl_run,
    fail_etl_run
)


load_dotenv()


def main():

    run_id = start_etl_run()

    try:

        google_sheet_url = os.getenv(
            "GOOGLE_SHEET_URL"
        )

        if not google_sheet_url:
            raise ValueError(
                "GOOGLE_SHEET_URL is not configured"
            )

        # =========================
        # Extract
        # =========================

        df = extract_orders(
            google_sheet_url
        )

        # =========================
        # Validate
        # =========================

        df = validate_orders(df)

        # =========================
        # Transform
        # =========================

        df = transform_orders(df)

        # =========================
        # Load
        # =========================

        with engine.begin() as connection:

            load_customers(
                connection,
                df
            )

            load_products(
                connection,
                df
            )

            load_orders(
                connection,
                df
            )

        # =========================
        # Success
        # =========================

        complete_etl_run(
            run_id,
            len(df)
        )

        result = {
            "status": "SUCCESS",
            "rows_processed": len(df),
            "run_id": run_id
        }

        print(
            "\nETL pipeline completed successfully!"
        )
        return result

    except Exception as error:

        fail_etl_run(
            run_id,
            str(error)
        )

        print(
            f"\nETL pipeline failed: {error}"
        )

        raise RuntimeError("TEST TRANSACTION ROLLBACK")


if __name__ == "__main__":
    main()