from datetime import datetime, timezone

from sqlalchemy import text

from database.connection import engine


def start_etl_run() -> int:
    """
    Create a new ETL run and return its ID.
    """

    with engine.begin() as connection:

        result = connection.execute(
            text("""
                INSERT INTO etl_runs (
                    status
                )
                VALUES (
                    'RUNNING'
                )
                RETURNING id
            """)
        )

        run_id = result.scalar()

    return run_id


def complete_etl_run(
    run_id: int,
    rows_processed: int
):
    """
    Mark an ETL run as successful.
    """

    with engine.begin() as connection:

        connection.execute(
            text("""
                UPDATE etl_runs
                SET
                    status = 'SUCCESS',
                    finished_at = :finished_at,
                    rows_processed = :rows_processed
                WHERE id = :run_id
            """),
            {
                "run_id": run_id,
                "finished_at": datetime.now(timezone.utc),
                "rows_processed": rows_processed
            }
        )


def fail_etl_run(
    run_id: int,
    error_message: str
):
    """
    Mark an ETL run as failed.
    """

    with engine.begin() as connection:

        connection.execute(
            text("""
                UPDATE etl_runs
                SET
                    status = 'FAILED',
                    finished_at = :finished_at,
                    error_message = :error_message
                WHERE id = :run_id
            """),
            {
                "run_id": run_id,
                "finished_at": datetime.now(timezone.utc),
                "error_message": error_message
            }
        )