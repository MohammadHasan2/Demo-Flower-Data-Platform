from datetime import date

from database.connection import engine
from reports.telegram import send_telegram_message
from app.queries import (
    get_total_revenue,
    get_total_orders,
    get_products_sold,
    get_top_products,
    get_orders_by_status,
    get_last_etl_run,
)


def generate_daily_report():

    today = date.today()

    with engine.connect() as connection:

        revenue = get_total_revenue(
            connection,
            today,
            today
        )

        orders = get_total_orders(
            connection,
            today,
            today
        )

        products_sold = get_products_sold(
            connection,
            today,
            today
        )

        top_products = get_top_products(
            connection,
            today,
            today
        )

        status_data = get_orders_by_status(
            connection,
            today,
            today
        )

        last_run = get_last_etl_run(
            connection
        )

    message = f"""
🌸 ZeeFlower Daily Report
━━━━━━━━━━━━━━━━━━━━

📅 {today.strftime("%B %d, %Y")}

💰 Revenue
${revenue:,.2f}

🛒 Orders
{orders:,}

🌸 Products Sold
{products_sold:,}
"""

    if top_products:

        top_product = top_products[0]

        message += f"""
🏆 Top Product
{top_product[0]} — {top_product[1]} units
"""

    message += "\n📦 Order Status\n"

    for status, count in status_data:
        message += f"{status}: {count}\n"

    if last_run:

        message += f"""
⚙️ ETL
Status: {last_run.status}
Rows Processed: {last_run.rows_processed}
"""

    return message.strip()


if __name__ == "__main__":

    report = generate_daily_report()

    print(report)

    send_telegram_message(report)

    print("Daily report sent successfully.")