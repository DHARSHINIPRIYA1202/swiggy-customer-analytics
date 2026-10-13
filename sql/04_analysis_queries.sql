# 1. OVERALL BUSINESS ANALYSIS

# Total customers
SELECT COUNT(*) AS total_customers
FROM users;

# Total orders
SELECT COUNT(*) AS total_orders
FROM orders;

# Total sales
SELECT SUM(sales_amount) AS total_sales
FROM orders;


-- 1.4 Average Order Value
SELECT ROUND(AVG(sales_amount), 2) AS average_order_value
FROM orders;

#  Minimum order amount
SELECT MIN(sales_amount) AS minimum_order_amount
FROM orders;


# Maximum order amount
SELECT MAX(sales_amount) AS maximum_order_amount
FROM orders;


# Total quantity sold
SELECT SUM(sales_qty) AS total_quantity
FROM orders;

# Active customers
SELECT COUNT(DISTINCT user_id) AS active_customers
FROM orders;


# Customers without orders
SELECT COUNT(*) AS customers_without_orders
FROM users u LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.user_id IS NULL;

# 2. DATA QUALITY CHECKS


# Check invalid sales
SELECT COUNT(*) AS invalid_sales
FROM orders
WHERE sales_amount <= 0;


#  Check extreme quantities
SELECT COUNT(*) AS extreme_quantity_orders
FROM orders
WHERE sales_qty > 1000;


# Check duplicate users
SELECT  user_id,COUNT(*) AS duplicate_count
FROM users GROUP BY user_id HAVING COUNT(*) > 1;


# Check missing restaurant IDs in orders
SELECT COUNT(*) AS missing_restaurant_ids FROM orders
WHERE restaurant_id IS NULL;

# 3. CUSTOMER DEMOGRAPHIC ANALYSIS

# Customers by gender

SELECT  gender,COUNT(*) AS customer_count FROM users
GROUP BY gender ORDER BY customer_count DESC;

# Customers by occupation
SELECT occupation,COUNT(*) AS customer_count
FROM users GROUP BY occupation ORDER BY customer_count DESC;

# Customers by age
SELECT age,COUNT(*) AS customer_count
FROM users GROUP BY age ORDER BY age;

# Customers by marital status
SELECT marital_status,COUNT(*) AS customer_count
FROM users GROUP BY marital_status 
ORDER BY customer_count DESC;



# SALES BY CUSTOMER DEMOGRAPHICS

# Sales by gender
SELECT u.gender,COUNT(o.order_id) AS total_orders,
SUM(o.sales_amount) AS total_sales,ROUND(AVG(o.sales_amount), 2) AS average_order_value
FROM users u JOIN orders o ON u.user_id = o.user_id
GROUP BY u.gender ORDER BY total_sales DESC;

# Sales by occupation
SELECT u.occupation,COUNT(o.order_id) AS total_orders,
SUM(o.sales_amount) AS total_sales,ROUND(AVG(o.sales_amount), 2) AS average_order_value
FROM users u JOIN orders o ON u.user_id = o.user_id
GROUP BY u.occupation ORDER BY total_sales DESC;

# Sales by age

SELECT u.age,COUNT(o.order_id) AS total_orders,SUM(o.sales_amount) AS total_sales
FROM users u JOIN orders o ON u.user_id = o.user_id
GROUP BY u.age ORDER BY total_sales DESC;

# CUSTOMER ORDER FREQUENCY

# Orders per customer
SELECT user_id,COUNT(order_id) AS order_count
FROM orders GROUP BY user_id
ORDER BY order_count DESC;

# Customer order frequency distribution
SELECT order_count,COUNT(*) AS customer_count
FROM (SELECT user_id,COUNT(order_id) AS order_count
FROM orders GROUP BY user_id ) AS customer_orders
GROUP BY order_count ORDER BY order_count;

# One-time customers
SELECT COUNT(*) AS one_time_customers
FROM(SELECT user_id,COUNT(order_id) AS order_count
FROM orders GROUP BY user_id) AS customer_orders
WHERE order_count = 1;

# Repeat customers
SELECT COUNT(*) AS repeat_customers FROM
(SELECT user_id,COUNT(order_id) AS order_count
FROM orders GROUP BY user_id ) AS customer_orders
WHERE order_count > 1;

# Customers with 3 or more orders
SELECT COUNT(*) AS customers_with_3_plus_orders
FROM(SELECT user_id,COUNT(order_id) AS order_count
FROM orders GROUP BY user_id) AS customer_orders
WHERE order_count >= 3;



# CUSTOMER SPENDING ANALYSIS

# Total spending by customer
SELECT user_id,COUNT(order_id) AS total_orders,
SUM(sales_amount) AS total_spend FROM orders
GROUP BY user_id ORDER BY total_spend DESC;


# Average customer spending
SELECT ROUND(AVG(total_spend), 2) AS average_customer_spend
FROM(SELECT user_id,SUM(sales_amount) AS total_spend
FROM orders GROUP BY user_id
) AS customer_spending;

# Top 10 customers by spending
SELECT user_id,COUNT(order_id) AS total_orders,
SUM(sales_amount) AS total_spend FROM orders
GROUP BY user_id ORDER BY total_spend DESC
LIMIT 10;

# Top 10 customers by number of orders
SELECT user_id,COUNT(order_id) AS total_orders,
SUM(sales_amount) AS total_spend FROM orders
GROUP BY user_id ORDER BY total_orders DESC
LIMIT 10;

# YEARLY SALES ANALYSIS

# Year-wise sales
SELECT 
    YEAR(order_date) AS order_year,
    COUNT(order_id) AS total_orders,
    SUM(sales_amount) AS total_sales,
    ROUND(AVG(sales_amount), 2) AS average_order_value
FROM orders GROUP BY YEAR(order_date)
ORDER BY order_year;

# Highest sales year
SELECT YEAR(order_date) AS order_year,
SUM(sales_amount) AS total_sales
FROM orders GROUP BY YEAR(order_date)
ORDER BY total_sales DESC
LIMIT 1;

# MONTHLY SALES ANALYSIS

# Monthly sales
SELECT YEAR(order_date) AS order_year,
MONTH(order_date) AS order_month,COUNT(order_id) AS total_orders,
SUM(sales_amount) AS total_sales,ROUND(AVG(sales_amount), 2) 
AS average_order_value FROM orders GROUP BY 
    YEAR(order_date),
    MONTH(order_date)
ORDER BY order_year,order_month;

# Monthly sales with month name
SELECT YEAR(order_date) AS order_year,
    MONTHNAME(order_date) AS month_name,
    COUNT(order_id) AS total_orders,
    SUM(sales_amount) AS total_sales
FROM orders GROUP BY YEAR(order_date),
MONTH(order_date),MONTHNAME(order_date)
ORDER BY order_year,MONTH(order_date);

#RESTAURANT BASIC ANALYSIS


# Total restaurants
SELECT COUNT(*) AS total_restaurants
FROM restaurants;


# Total unique cities
SELECT COUNT(DISTINCT city) AS total_cities
FROM restaurants;


# Total unique cuisines
SELECT COUNT(DISTINCT cuisine) AS total_cuisines
FROM restaurants;


# Restaurants by country
SELECT country,COUNT(*) AS restaurant_count
FROM restaurants
GROUP BY country
ORDER BY restaurant_count DESC;

# CITY-WISE RESTAURANT ANALYSIS
 
# Restaurants by city
SELECT city,COUNT(*) AS restaurant_count
FROM restaurants GROUP BY city
ORDER BY restaurant_count DESC;

# Top 10 cities with most restaurants
SELECT city,COUNT(*) AS restaurant_count
FROM restaurants GROUP BY city
ORDER BY restaurant_count DESC LIMIT 10;

# Cities with more than 100 restaurants
SELECT city,COUNT(*) AS restaurant_count
FROM restaurants GROUP BY city
HAVING COUNT(*) > 100 ORDER BY restaurant_count DESC;

#  RESTAURANT RATING ANALYSIS
# Average restaurant rating

SELECT ROUND(AVG(rating), 2) AS average_rating
FROM restaurants WHERE rating IS NOT NULL;


# Highest rating
SELECT MAX(rating) AS highest_rating
FROM restaurants;

# Lowest rating
SELECT MIN(rating) AS lowest_rating
FROM restaurants
WHERE rating IS NOT NULL;

# Rating-wise restaurant count
SELECT rating,COUNT(*) AS restaurant_count
FROM restaurants WHERE rating IS NOT NULL
GROUP BY rating ORDER BY rating DESC;

# TOP RATED RESTAURANTS
# Top 10 highest-rated restaurants
SELECT restaurant_id,name,city,rating,rating_count
FROM restaurants WHERE rating IS NOT NULL
ORDER BY rating DESC LIMIT 10;

# Top-rated restaurants with at least 100 ratings
SELECT  restaurant_id,name,city,rating,rating_count
FROM restaurants WHERE rating IS NOT NULL
AND rating_count_numeric >= 100 ORDER BY rating DESC
LIMIT 10;

# Highly rated restaurants with strong review count
SELECT restaurant_id,name,city,rating,
rating_count_numeric FROM restaurants
WHERE rating >= 4.0 AND rating_count_numeric >= 500
ORDER BY rating DESC, rating_count_numeric DESC
LIMIT 20;

# CUISINE ANALYSIS

# Most common cuisines
SELECT cuisine,COUNT(*) AS restaurant_count
FROM restaurants GROUP BY cuisine
ORDER BY restaurant_count DESC;


# Top 10 cuisines
SELECT cuisine,COUNT(*) AS restaurant_count
FROM restaurants GROUP BY cuisine
ORDER BY restaurant_count DESC LIMIT 10;


# Cuisines with more than 100 restaurants
SELECT 
    cuisine,
    COUNT(*) AS restaurant_count
FROM restaurants
GROUP BY cuisine
HAVING COUNT(*) > 100
ORDER BY restaurant_count DESC;


-- ============================================================
-- 14. CITY + CUISINE ANALYSIS
-- ============================================================

-- 14.1 City and cuisine combination
SELECT 
    city,
    cuisine,
    COUNT(*) AS restaurant_count
FROM restaurants
GROUP BY city, cuisine
ORDER BY restaurant_count DESC;


-- 14.2 Top 20 city + cuisine combinations
SELECT 
    city,
    cuisine,
    COUNT(*) AS restaurant_count
FROM restaurants
GROUP BY city, cuisine
ORDER BY restaurant_count DESC
LIMIT 20;


-- ============================================================
-- 15. CITY-WISE RATING ANALYSIS
-- ============================================================

-- 15.1 Average rating by city
SELECT 
    city,
    COUNT(*) AS restaurant_count,
    ROUND(AVG(rating), 2) AS average_rating
FROM restaurants
WHERE rating IS NOT NULL
GROUP BY city
ORDER BY average_rating DESC;


-- 15.2 Cities with at least 10 rated restaurants
SELECT 
    city,
    COUNT(rating) AS rated_restaurants,
    ROUND(AVG(rating), 2) AS average_rating
FROM restaurants
WHERE rating IS NOT NULL
GROUP BY city
HAVING COUNT(rating) >= 10
ORDER BY average_rating DESC;


-- ============================================================
-- 16. RESTAURANT + ORDERS ANALYSIS
-- ============================================================

-- 16.1 Restaurant-wise orders and sales
SELECT 
    r.restaurant_id,
    r.name,
    r.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.sales_amount) AS total_sales
FROM restaurants r
JOIN orders o
    ON r.restaurant_id = o.restaurant_id
GROUP BY 
    r.restaurant_id,
    r.name,
    r.city
ORDER BY total_sales DESC;


-- 16.2 Top 10 restaurants by sales
SELECT 
    r.restaurant_id,
    r.name,
    r.city,
    COUNT(o.order_id) AS total_orders,
    SUM(o.sales_amount) AS total_sales
FROM restaurants r
JOIN orders o
    ON r.restaurant_id = o.restaurant_id
GROUP BY 
    r.restaurant_id,
    r.name,
    r.city
ORDER BY total_sales DESC
LIMIT 10;


-- 16.3 Top 10 restaurants by order frequency
SELECT 
    r.restaurant_id,
    r.name,
    r.city,
    COUNT(o.order_id) AS total_orders
FROM restaurants r
JOIN orders o
    ON r.restaurant_id = o.restaurant_id
GROUP BY 
    r.restaurant_id,
    r.name,
    r.city
ORDER BY total_orders DESC
LIMIT 10;



 # CITY-WISE SALES + RESTAURANT ANALYSIS
 
# City-wise restaurant count, orders and sales
SELECT  r.city,COUNT(DISTINCT r.restaurant_id) AS restaurant_count,
COUNT(o.order_id) AS total_orders,SUM(o.sales_amount) AS total_sales
FROM restaurants r JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.city ORDER BY total_sales DESC;


# Top 10 cities by sales
SELECT r.city,COUNT(o.order_id) AS total_orders,SUM(o.sales_amount) AS total_sales
FROM restaurants r JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.city ORDER BY total_sales DESC LIMIT 10;

# FINAL BUSINESS QUESTIONS

# Top 10 customers by spending
SELECT user_id,COUNT(order_id) AS total_orders,
SUM(sales_amount) AS total_spend FROM orders
GROUP BY user_id ORDER BY total_spend DESC LIMIT 10;

# Top 10 customers by order frequency
SELECT user_id,COUNT(order_id) AS total_orders,SUM(sales_amount) AS total_spend
FROM orders GROUP BY user_id ORDER BY total_orders DESC
LIMIT 10;

# One-time customers
SELECT user_id,COUNT(order_id) AS total_orders,
SUM(sales_amount) AS total_spend FROM orders
GROUP BY user_id HAVING COUNT(order_id) = 1
ORDER BY total_spend DESC;

# High-value customers
SELECT user_id,COUNT(order_id) AS total_orders,SUM(sales_amount) AS total_spend
FROM orders GROUP BY user_id HAVING SUM(sales_amount) >= 50000
ORDER BY total_spend DESC;


-- 18.5 Customers with 3+ orders
SELECT 
    user_id,
    COUNT(order_id) AS total_orders,
    SUM(sales_amount) AS total_spend
FROM orders
GROUP BY user_id
HAVING COUNT(order_id) >= 3
ORDER BY total_orders DESC, total_spend DESC;


# Top restaurants with rating and sales
SELECT r.restaurant_id,r.name,r.city,r.rating,
COUNT(o.order_id) AS total_orders,SUM(o.sales_amount) AS total_sales
FROM restaurants r JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.restaurant_id,r.name,r.city,r.rating
ORDER BY total_sales DESC LIMIT 10;

# Top cities by sales
SELECT r.city,COUNT(o.order_id) AS total_orders,SUM(o.sales_amount) AS total_sales
FROM restaurants r JOIN orders o ON r.restaurant_id = o.restaurant_id
GROUP BY r.city ORDER BY total_sales DESC LIMIT 10;


# Top cuisines by restaurant count
SELECT cuisine,COUNT(*) AS restaurant_count
FROM restaurants GROUP BY cuisine
ORDER BY restaurant_count DESC
LIMIT 10;
