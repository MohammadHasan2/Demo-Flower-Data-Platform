import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from etl.run_pipeline import main as run_etl
from database.connection import engine
from datetime import date, timedelta
import pandas as pd

from queries import (
    get_orders_by_status,
    get_recent_orders,
    get_revenue_over_time,
    get_top_products,
    get_total_revenue,
    get_total_orders,
    get_total_customers,
    get_products_sold,
    get_last_etl_run,
    get_all_customers,
    search_customer_by_phone,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Flower Shop Analytics",
    page_icon="🌸",
    layout="wide",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* Main page */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Header */
    .dashboard-subtitle {
        color: #777;
        font-size: 1.05rem;
        margin-top: -10px;
        margin-bottom: 1.5rem;
    }

    /* Section titles */
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }

    /* ETL status */
    .etl-status {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #eeeeee;
        background-color: #fafafa;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        padding-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <h1 style="margin-bottom: 0;">
        🌸 Flower Shop Analytics
    </h1>

    <p class="dashboard-subtitle">
        Track sales, customers, products and orders in one place.
    </p>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SYNC SECTION
# ============================================================

sync_col, status_col = st.columns([1, 3])

with sync_col:

    sync_clicked = st.button(
        "🔄 Sync Latest Data",
        type="primary",
        use_container_width=True,
    )

with status_col:

    st.caption(
        "Synchronize the latest orders from Google Sheets."
    )


if sync_clicked:

    with st.spinner("Running ETL pipeline..."):

        try:

            result = run_etl()

            st.success(
                "✅ Data synchronized successfully!"
            )

            st.info(
                f"Rows processed: "
                f"{result['rows_processed']}"
            )

            st.rerun()

        except Exception as error:

            st.error(
                f"❌ ETL failed: {error}"
            )


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🌸 Flower Shop")

st.sidebar.markdown("### 📊 Analytics")

st.sidebar.caption(
    "Choose the period you want to analyze."
)

today = date.today()

date_option = st.sidebar.selectbox(
    "Date range",
    [
        "Today",
        "Last 7 days",
        "Last 30 days",
        "This month",
        "All time",
    ],
)


if date_option == "Today":

    start_date = today
    end_date = today


elif date_option == "Last 7 days":

    start_date = today - timedelta(days=6)
    end_date = today


elif date_option == "Last 30 days":

    start_date = today - timedelta(days=29)
    end_date = today


elif date_option == "This month":

    start_date = today.replace(day=1)
    end_date = today


else:

    start_date = None
    end_date = None


st.sidebar.divider()

customer_page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "👥 Customers"
    ]
)

if customer_page == "👥 Customers":

    st.title("👥 Customers")

    st.caption(
        "View and search registered customers."
    )

    with engine.connect() as connection:

        customers_data = get_all_customers(
            connection
        )

    st.subheader("📋 All Customers")

    if customers_data:

        customers_df = pd.DataFrame(
            customers_data,
            columns=[
                "ID",
                "Name",
                "Phone"
            ]
        )

        st.dataframe(
            customers_df[
                [
                    "Name",
                    "Phone"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No customers found."
        )

    st.divider()

    st.subheader("🔎 Search Customer")

    phone = st.text_input(
        "Enter customer phone number",
        placeholder="e.g. 03xxxxxx"
    )

    if st.button(
        "Search Customer",
        type="primary"
    ):

        if not phone.strip():

            st.warning(
                "Please enter a phone number."
            )

        else:

            with engine.connect() as connection:

                customer = search_customer_by_phone(
                    connection,
                    phone.strip()
                )

            if customer:

                st.success(
                    "✅ Customer found"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "👤 Name",
                        customer.name
                    )

                with col2:

                    st.metric(
                        "📱 Phone",
                        customer.phone
                    )

            else:

                st.error(
                    "❌ Customer not found."
                )

elif customer_page == "📊 Dashboard":
    st.sidebar.divider()

    st.sidebar.caption(
        "Data source: Google Sheets"
    )

    st.sidebar.caption(
        "Database: Supabase PostgreSQL"
    )


    # ============================================================
    # DATABASE QUERIES
    # ============================================================

    with engine.connect() as connection:

        revenue = get_total_revenue(
            connection,
            start_date,
            end_date,
        )

        orders = get_total_orders(
            connection,
            start_date,
            end_date,
        )

        customers = get_total_customers(
            connection,
        )

        products_sold = get_products_sold(
            connection,
            start_date,
            end_date,
        )

        last_run = get_last_etl_run(
            connection,
        )

        revenue_data = get_revenue_over_time(
            connection,
            start_date,
            end_date,
        )

        top_products = get_top_products(
            connection,
            start_date,
            end_date,
        )

        status_data = get_orders_by_status(
            connection,
            start_date,
            end_date
        )

        recent_orders = get_recent_orders(
            connection,
            start_date,
            end_date
        )


    # ============================================================
    # OVERVIEW
    # ============================================================
    
    st.markdown(
        '<div class="section-title">📊 Overview</div>',
        unsafe_allow_html=True,
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "💰 Revenue",
            f"${revenue:,.2f}",
        )


    with col2:

        st.metric(
            "🛒 Orders",
            f"{orders:,}",
        )


    with col3:

        st.metric(
            "👥 Customers",
            f"{customers:,}",
        )


    with col4:

        st.metric(
            "🌸 Products Sold",
            f"{products_sold:,}",
        )


    # ============================================================
    # REVENUE + ORDER STATUS
    # ============================================================

    st.divider()

    chart_col1, chart_col2 = st.columns(2)


    # ------------------------------------------------------------
    # Revenue Chart
    # ------------------------------------------------------------

    with chart_col1:

        st.subheader("📈 Revenue Trend")

        if revenue_data:

            revenue_df = pd.DataFrame(
                revenue_data,
                columns=[
                    "date",
                    "revenue",
                ],
            )

            revenue_df["revenue"] = (
                revenue_df["revenue"].astype(float)
            )

            revenue_df["date"] = pd.to_datetime(
                revenue_df["date"]
            )

            revenue_df = revenue_df.set_index(
                "date"
            )

            st.line_chart(
                revenue_df["revenue"]
            )

        else:

            st.info(
                "No revenue data available for this period."
            )


    # ------------------------------------------------------------
    # Order Status
    # ------------------------------------------------------------

    with chart_col2:

        st.subheader("📦 Orders by Status")

        if status_data:

            status_df = pd.DataFrame(
                status_data,
                columns=[
                    "Status",
                    "Orders",
                ],
            )

            st.bar_chart(
                status_df.set_index("Status")
            )

        else:

            st.info(
                "No order status data available."
            )


    # ============================================================
    # TOP PRODUCTS
    # ============================================================

    st.divider()

    st.subheader("🌸 Top-Selling Products")


    if top_products:

        products_df = pd.DataFrame(
            top_products,
            columns=[
                "Product",
                "Units Sold",
                "Revenue",
            ],
        )

        products_df["Revenue"] = products_df[
            "Revenue"
        ].apply(
            lambda value: f"${value:,.2f}"
        )

        st.dataframe(
            products_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No product sales available for this period."
        )


    # ============================================================
    # RECENT ORDERS
    # ============================================================

    st.divider()

    st.subheader("🛍️ Recent Orders")


    if recent_orders:

        orders_df = pd.DataFrame(
            recent_orders,
            columns=[
                "Order ID",
                "Date",
                "Customer",
                "Status",
                "Amount",
            ],
        )

        orders_df["Amount"] = orders_df[
            "Amount"
        ].apply(
            lambda value: f"${value:,.2f}"
        )

        st.dataframe(
            orders_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No recent orders available."
        )


    # ============================================================
    # ETL PIPELINE STATUS
    # ============================================================

    st.divider()

    st.subheader("⚙️ Data Pipeline")


    if last_run:

        run_id = last_run.id
        status = last_run.status
        rows = last_run.rows_processed
        started = last_run.started_at


        if status == "SUCCESS":

            st.success(
                f"✅ Last sync successful — "
                f"{rows} rows processed."
            )


        elif status == "FAILED":

            st.error(
                f"❌ Last sync failed."
            )


            if last_run.error_message:

                st.caption(
                    f"Error: {last_run.error_message}"
                )


        else:

            st.warning(
                f"⏳ Pipeline status: {status}"
            )


        status_col1, status_col2, status_col3 = st.columns(3)


        with status_col1:

            st.write(
                f"**Run:** #{run_id}"
            )


        with status_col2:

            st.write(
                f"**Rows processed:** {rows}"
            )


        with status_col3:

            st.write(
                f"**Started:** {started}"
            )


    else:

        st.info(
            "No ETL runs have been recorded yet."
        )