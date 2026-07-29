-- Run this in MySQL to verify your tables exist
-- onlineshoppingdb schema reference

USE onlineshoppingdb;

-- users: user_id, name, email, city, signup_date, gender
-- orders: order_id, user_id, order_date, order_status, total_amount
-- order_items: order_item_id, order_id, product_id, user_id, quantity, item_price, item_toatal
-- products: product_id, product_name, category, brand, price

SELECT 'Tables OK' AS status;
SHOW TABLES;
