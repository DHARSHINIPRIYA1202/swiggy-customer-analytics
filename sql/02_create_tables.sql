# USERS TABLE

USE swiggy_customer_analytics;

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(20),
    marital_status VARCHAR(30),
    occupation VARCHAR(50)
);

#ORDER TABLE

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE,
    sales_qty INT,
    sales_amount DECIMAL(15,2),
    currency VARCHAR(10),
    user_id INT,
    restaurant_id INT
);

#RESTAURANT TABLE

CREATE TABLE restaurants (
    restaurant_id INT PRIMARY KEY,
    name VARCHAR(255),
    country VARCHAR(50),
    city VARCHAR(100),
    rating DECIMAL(3,1),
    rating_count VARCHAR(30),
    cuisine VARCHAR(255),
    rating_count_numeric INT
);

Show tables;