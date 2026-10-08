SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
    ROUND(SUM(p.payment_value), 2) AS revenue
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month;

SELECT
    ROUND(
        SUM(p.payment_value) / COUNT(DISTINCT o.order_id),2) AS average_order_value
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered';

SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS month,
    COUNT(*) AS total_orders
FROM orders
WHERE order_status = 'delivered'
GROUP BY month
ORDER BY month;

SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
    COUNT(DISTINCT c.customer_unique_id) AS unique_customers
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY month
ORDER BY month;

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

SELECT
    ROUND(
        AVG(
            EXTRACT(
                DAY FROM (order_delivered_customer_date - order_purchase_timestamp)
            )
        ),
        2
    ) AS average_delivery_days
FROM orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL;


-- On-Time vs Late Deliveries
SELECT
    CASE
        WHEN order_delivered_customer_date::date <= order_estimated_delivery_date::date THEN 'On Time'
        ELSE 'Late'
    END AS delivery_status,
    COUNT(*) AS total_orders
FROM orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL
GROUP BY delivery_status
ORDER BY total_orders DESC;


-- On-Time Delivery Percentage
SELECT
    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE order_delivered_customer_date::date <= order_estimated_delivery_date::date
        )
        / COUNT(*),
        2
    ) AS on_time_delivery_percentage
FROM orders
WHERE order_status = 'delivered'
AND order_delivered_customer_date IS NOT NULL;

SELECT
    ROUND(SUM(p.payment_value), 2) AS total_revenue
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered';

SELECT
    COUNT(*) AS total_orders
FROM orders
WHERE order_status = 'delivered';

SELECT
    COUNT(DISTINCT c.customer_unique_id) AS total_customers
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered';