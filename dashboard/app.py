import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine


st.set_page_config(
    page_title="OpsFlow Dashboard",
    layout="wide"
)

st.title("OpsFlow")
st.subheader("Business Operations Analytics Dashboard")


@st.cache_resource
def get_engine():
    return create_engine(
        "postgresql+psycopg2://prakalp@localhost/opsflow"
    )


engine = get_engine()


total_revenue = pd.read_sql(
    """
    SELECT ROUND(SUM(p.payment_value), 2) AS total_revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered';
    """,
    engine
).iloc[0, 0]


total_orders = pd.read_sql(
    """
    SELECT COUNT(*) AS total_orders
    FROM orders
    WHERE order_status = 'delivered';
    """,
    engine
).iloc[0, 0]


total_customers = pd.read_sql(
    """
    SELECT COUNT(DISTINCT c.customer_unique_id) AS total_customers
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered';
    """,
    engine
).iloc[0, 0]


average_order_value = pd.read_sql(
    """
    SELECT ROUND(
        SUM(p.payment_value) / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered';
    """,
    engine
).iloc[0, 0]


col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"{total_revenue:,.2f}")
col2.metric("Delivered Orders", f"{total_orders:,}")
col3.metric("Unique Customers", f"{total_customers:,}")
col4.metric("Average Order Value", f"{average_order_value:,.2f}")

monthly_revenue = pd.read_sql(
    """
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
        ROUND(SUM(p.payment_value), 2) AS revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY month
    ORDER BY month;
    """,
    engine
)

st.subheader("Monthly Revenue Trend")

revenue_chart = px.line(
    monthly_revenue,
    x="month",
    y="revenue",
    labels={
        "month": "Month",
        "revenue": "Revenue"
    }
)

st.plotly_chart(revenue_chart, width="stretch")

payment_breakdown = pd.read_sql(
    """
    SELECT
        p.payment_type,
        COUNT(*) AS payment_count,
        ROUND(SUM(p.payment_value), 2) AS total_payment_value
    FROM payments p
    JOIN orders o
        ON p.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY p.payment_type
    ORDER BY total_payment_value DESC;
    """,
    engine
)

st.subheader("Payment Method Breakdown")

payment_chart = px.bar(
    payment_breakdown,
    x="payment_type",
    y="total_payment_value",
    labels={
        "payment_type": "Payment Method",
        "total_payment_value": "Payment Value"
    }
)

st.plotly_chart(payment_chart, width="stretch")

delivery_performance = pd.read_sql(
    """
    SELECT
        CASE
            WHEN order_delivered_customer_date::date <= order_estimated_delivery_date::date
                THEN 'On Time'
            ELSE 'Late'
        END AS delivery_status,
        COUNT(*) AS total_orders
    FROM orders
    WHERE order_status = 'delivered'
    AND order_delivered_customer_date IS NOT NULL
    GROUP BY delivery_status
    ORDER BY total_orders DESC;
    """,
    engine
)

st.subheader("Delivery Performance")

delivery_chart = px.pie(
    delivery_performance,
    names="delivery_status",
    values="total_orders"
)

st.plotly_chart(delivery_chart, width="stretch")

delivery_metrics = pd.read_sql(
    """
    SELECT
        ROUND(
            AVG(
                EXTRACT(
                    DAY FROM (
                        order_delivered_customer_date
                        - order_purchase_timestamp
                    )
                )
            ),
            2
        ) AS average_delivery_days,

        ROUND(
            100.0 *
            COUNT(*) FILTER (
                WHERE order_delivered_customer_date::date <= order_estimated_delivery_date::date
            )
            / COUNT(*),
            2
        ) AS on_time_percentage

    FROM orders
    WHERE order_status = 'delivered'
    AND order_delivered_customer_date IS NOT NULL;
    """,
    engine
)

avg_delivery_days = delivery_metrics.iloc[0]["average_delivery_days"]
on_time_percentage = delivery_metrics.iloc[0]["on_time_percentage"]

col5, col6 = st.columns(2)

col5.metric(
    "Average Delivery Time",
    f"{avg_delivery_days:.2f} days"
)

col6.metric(
    "On-Time Delivery",
    f"{on_time_percentage:.2f}%"
)

monthly_activity = pd.read_sql(
    """
    SELECT
        DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
        COUNT(*) AS total_orders,
        COUNT(DISTINCT c.customer_unique_id) AS unique_customers
    FROM orders o
    JOIN customers c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY month
    ORDER BY month;
    """,
    engine
)

st.subheader("Monthly Orders and Customers")

activity_chart = px.line(
    monthly_activity,
    x="month",
    y=["total_orders", "unique_customers"],
    labels={
        "month": "Month",
        "value": "Count",
        "variable": "Metric"
    }
)

activity_chart.for_each_trace(
    lambda trace: trace.update(
        name={
            "total_orders": "Delivered Orders",
            "unique_customers": "Unique Customers"
        }.get(trace.name, trace.name)
    )
)

st.plotly_chart(activity_chart, width="stretch")