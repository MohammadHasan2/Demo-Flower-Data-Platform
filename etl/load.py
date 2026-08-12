import pandas as pd
from sqlalchemy import text

from database.connection import engine


def load_customers(
    connection,
    df: pd.DataFrame
):
    """
    Insert new customers.
    """

    query = text("""
        INSERT INTO customers (
            name,
            phone
        )
        VALUES (
            :name,
            :phone
        )
        ON CONFLICT (phone)
        DO NOTHING
    """)

    for _, row in df.iterrows():

        connection.execute(
            query,
            {
                "name": row["customer_name"],
                "phone": str(row["customer_phone"])
            }
        )

    print("Customers loaded successfully")


def load_products(
    connection,
    df: pd.DataFrame
):
    """
    Insert new products and update prices.
    """

    query = text("""
        INSERT INTO products (
            name,
            price
        )
        VALUES (
            :name,
            :price
        )
        ON CONFLICT (name)
        DO UPDATE SET
            price = EXCLUDED.price
    """)

    for _, row in df.iterrows():

        connection.execute(
            query,
            {
                "name": row["product_name"],
                "price": float(row["unit_price"])
            }
        )

    print("Products loaded successfully")


def get_customer_id(
    connection,
    phone
):
    """
    Retrieve customer ID using phone number.
    """

    query = text("""
        SELECT id
        FROM customers
        WHERE phone = :phone
    """)

    result = connection.execute(
        query,
        {
            "phone": str(phone)
        }
    ).fetchone()

    if not result:
        raise ValueError(
            f"Customer not found: {phone}"
        )

    return result[0]


def get_product_id(
    connection,
    product_name
):
    """
    Retrieve product ID using product name.
    """

    query = text("""
        SELECT id
        FROM products
        WHERE name = :name
    """)

    result = connection.execute(
        query,
        {
            "name": product_name
        }
    ).fetchone()

    if not result:
        raise ValueError(
            f"Product not found: {product_name}"
        )

    return result[0]


def load_orders(
    connection,
    df: pd.DataFrame
):
    """
    Insert new orders or update existing orders.
    """

    order_query = text("""
        INSERT INTO orders (
            id,
            customer_id,
            order_date,
            status,
            total_amount
        )
        VALUES (
            :id,
            :customer_id,
            :order_date,
            :status,
            :total_amount
        )
        ON CONFLICT (id)
        DO UPDATE SET
            customer_id = EXCLUDED.customer_id,
            order_date = EXCLUDED.order_date,
            status = EXCLUDED.status,
            total_amount = EXCLUDED.total_amount
        RETURNING id
    """)

    delete_items_query = text("""
        DELETE FROM order_items
        WHERE order_id = :order_id
    """)

    item_query = text("""
        INSERT INTO order_items (
            order_id,
            product_id,
            quantity,
            unit_price
        )
        VALUES (
            :order_id,
            :product_id,
            :quantity,
            :unit_price
        )
    """)

    for _, row in df.iterrows():

        customer_id = get_customer_id(
            connection,
            row["customer_phone"]
        )

        product_id = get_product_id(
            connection,
            row["product_name"]
        )

        result = connection.execute(
            order_query,
            {
                "id": int(row["order_id"]),
                "customer_id": customer_id,
                "order_date": row["date"],
                "status": row["status"],
                "total_amount": float(row["subtotal"])
            }
        )

        order_id = result.scalar_one()

        connection.execute(
            delete_items_query,
            {
                "order_id": order_id
            }
        )

        connection.execute(
            item_query,
            {
                "order_id": order_id,
                "product_id": product_id,
                "quantity": int(row["quantity"]),
                "unit_price": float(row["unit_price"])
            }
        )

    print("Orders loaded successfully")