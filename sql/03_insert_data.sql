SELECT COUNT(*) AS total_users
FROM users;

SELECT COUNT(*) AS total_orders
FROM orders;

SELECT COUNT(*) AS total_restaurants
FROM restaurants;
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END) AS missing_user_id
FROM users;

SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) AS missing_order_id,
    SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END) AS missing_user_id,
    SUM(CASE WHEN restaurant_id IS NULL THEN 1 ELSE 0 END) AS missing_restaurant_id
FROM orders;

SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN restaurant_id IS NULL THEN 1 ELSE 0 END) AS missing_restaurant_id,
    SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END) AS missing_name
FROM restaurants;


SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT user_id) AS unique_user_ids
FROM users;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_order_ids
FROM orders;

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT restaurant_id) AS unique_restaurant_ids
FROM restaurants;

SELECT COUNT(*) AS unmatched_user_orders
FROM orders o
LEFT JOIN users u
    ON o.user_id = u.user_id
WHERE u.user_id IS NULL;


SELECT COUNT(*) AS unmatched_restaurant_orders
FROM orders o
LEFT JOIN restaurants r
    ON o.restaurant_id = r.restaurant_id
WHERE r.restaurant_id IS NULL;

SELECT
    o.restaurant_id,
    COUNT(*) AS affected_orders
FROM orders o
LEFT JOIN restaurants r
    ON o.restaurant_id = r.restaurant_id
WHERE r.restaurant_id IS NULL
GROUP BY o.restaurant_id
ORDER BY affected_orders DESC
LIMIT 10;

SELECT
    COUNT(*) AS unmatched_orders,
    COUNT(DISTINCT o.restaurant_id) AS distinct_unmatched_restaurants
FROM orders o
LEFT JOIN restaurants r
    ON o.restaurant_id = r.restaurant_id
WHERE r.restaurant_id IS NULL;


SELECT COUNT(*) AS total_orders,SUM(CASE
WHEN r.restaurant_id IS NULL THEN 1 ELSE 0 END
    ) AS unmatched_orders,ROUND(100.0 * SUM(
	CASE WHEN r.restaurant_id IS NULL THEN 1
	ELSE 0 END ) / COUNT(*),2) AS unmatched_percentage
FROM orders o LEFT JOIN restaurants r
    ON o.restaurant_id = r.restaurant_id;

DESCRIBE orders;

SELECT COUNT(*) AS unmatched_orders,SUM(
CASE WHEN o.sales_amount IS NULL THEN 1 ELSE 0 END) AS missing_sales_amount,
    SUM(CASE WHEN o.sales_amount <= 0 THEN 1 ELSE 0 END
    ) AS nonpositive_sales_amount,ROUND(SUM(o.sales_amount), 2) AS total_unmatched_sales
FROM orders o LEFT JOIN restaurants r
    ON o.restaurant_id = r.restaurant_id
WHERE r.restaurant_id IS NULL;

SELECT currency,COUNT(*) AS order_count,
ROUND(SUM(sales_amount), 2) AS total_sales
FROM orders o LEFT JOIN restaurants r
    ON o.restaurant_id = r.restaurant_id
WHERE r.restaurant_id IS NULL
GROUP BY currency;

SELECT currency,COUNT(*) AS order_count,
ROUND(SUM(sales_amount), 2) AS total_sales FROM orders o
LEFT JOIN restaurants r
    ON o.restaurant_id = r.restaurant_id
WHERE r.restaurant_id IS NULL
GROUP BY currency;

SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS sales_month,
    COUNT(*) AS total_orders,
    SUM(sales_qty) AS total_quantity,
    ROUND(SUM(sales_amount), 2) AS total_sales
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY sales_month;