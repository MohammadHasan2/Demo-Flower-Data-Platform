from sqlalchemy import text
import streamlit as st

def get_total_revenue(
    connection,
    start_date=None,
    end_date=None
):

    query = """
        SELECT COALESCE(
            SUM(total_amount),
            0
        )
        FROM orders
        WHERE status != 'Cancelled'
    """

    params = {}

    if start_date:
        query += """
            AND order_date::date >= :start_date
        """

        params["start_date"] = start_date

    if end_date:
        query += """
            AND order_date::date <= :end_date
        """

        params["end_date"] = end_date

    result = connection.execute(
        text(query),
        params
    )

    return result.scalar()


def get_total_orders(
    connection,
    start_date=None,
    end_date=None
):

    query = """
        SELECT COUNT(*)
        FROM orders
        WHERE status != 'Cancelled'
    """

    params = {}

    if start_date:

        query += """
            AND order_date::date >= :start_date
        """

        params["start_date"] = start_date

    if end_date:

        query += """
            AND order_date::date <= :end_date
        """

        params["end_date"] = end_date

    result = connection.execute(
        text(query),
        params
    )

    return result.scalar()

def get_total_customers(connection):

    result = connection.execute(
        text("""
            SELECT COUNT(*)
            FROM customers
        """)
    )

    return result.scalar()


def get_products_sold(
    connection,
    start_date=None,
    end_date=None
):

    query = """
        SELECT COALESCE(
            SUM(oi.quantity),
            0
        )
        FROM order_items oi
        JOIN orders o
            ON o.id = oi.order_id
        WHERE o.status != 'Cancelled'
    """

    params = {}

    if start_date:

        query += """
            AND o.order_date::date >= :start_date
        """

        params["start_date"] = start_date

    if end_date:

        query += """
            AND o.order_date::date <= :end_date
        """

        params["end_date"] = end_date

    result = connection.execute(
        text(query),
        params
    )

    return result.scalar()

def get_last_etl_run(connection):

    result = connection.execute(
        text("""
            SELECT
                id,
                status,
                started_at,
                finished_at,
                rows_processed,
                error_message
            FROM etl_runs
            ORDER BY id DESC
            LIMIT 1
        """)
    )

    return result.fetchone()

def get_revenue_over_time(
    connection,
    start_date=None,
    end_date=None
):

    query = """
        SELECT
            order_date::date AS date,
            SUM(total_amount) AS revenue
        FROM orders
        WHERE status != 'Cancelled'
    """

    params = {}

    if start_date:

        query += """
            AND order_date::date >= :start_date
        """

        params["start_date"] = start_date

    if end_date:

        query += """
            AND order_date::date <= :end_date
        """

        params["end_date"] = end_date

    query += """
        GROUP BY order_date::date
        ORDER BY date
    """

    result = connection.execute(
        text(query),
        params
    )

    return result.fetchall()

def get_top_products(
    connection,
    start_date=None,
    end_date=None
):

    query = """
        SELECT
            p.name,
            SUM(oi.quantity) AS units_sold,
            SUM(
                oi.quantity * oi.unit_price
            ) AS revenue
        FROM order_items oi
        JOIN products p
            ON p.id = oi.product_id
        JOIN orders o
            ON o.id = oi.order_id
        WHERE o.status != 'Cancelled'
    """

    params = {}

    if start_date:

        query += """
            AND o.order_date::date >= :start_date
        """

        params["start_date"] = start_date

    if end_date:

        query += """
            AND o.order_date::date <= :end_date
        """

        params["end_date"] = end_date

    query += """
        GROUP BY p.name
        ORDER BY units_sold DESC
        LIMIT 10
    """

    result = connection.execute(
        text(query),
        params
    )

    return result.fetchall()

def get_orders_by_status(
    connection,
    start_date=None,
    end_date=None
):

    query = """
        SELECT
            status,
            COUNT(*) AS orders
        FROM orders
        WHERE 1=1
    """

    params = {}

    if start_date:

        query += """
            AND order_date::date >= :start_date
        """

        params["start_date"] = start_date

    if end_date:

        query += """
            AND order_date::date <= :end_date
        """

        params["end_date"] = end_date

    query += """
        GROUP BY status
        ORDER BY orders DESC
    """

    result = connection.execute(
        text(query),
        params
    )

    return result.fetchall()

def get_recent_orders(
    connection,
    start_date=None,
    end_date=None
):

    query = """
        SELECT
            o.id AS order_id,
            o.order_date,
            c.name AS customer,
            o.status,
            o.total_amount
        FROM orders o
        JOIN customers c
            ON c.id = o.customer_id
        WHERE 1=1
    """

    params = {}

    if start_date:

        query += """
            AND o.order_date::date >= :start_date
        """

        params["start_date"] = start_date

    if end_date:

        query += """
            AND o.order_date::date <= :end_date
        """

        params["end_date"] = end_date

    query += """
        ORDER BY o.order_date DESC
        LIMIT 10
    """

    result = connection.execute(
        text(query),
        params
    )

    return result.fetchall()

def get_all_customers(connection):

    query = """
        SELECT
            id,
            name,
            phone
        FROM customers
        ORDER BY name ASC
    """

    result = connection.execute(
        text(query)
    )

    return result.fetchall()

def search_customer_by_phone(
    connection,
    phone
):

    query = """
        SELECT
            name,
            phone
        FROM customers
        WHERE phone = :phone
        LIMIT 1
    """

    result = connection.execute(
        text(query),
        {
            "phone": phone
        }
    )

    return result.fetchone()