# Sales Analytics Dashboard

A full-stack analytics dashboard for an online shopping system, built with Flask and MySQL. It provides a web-based interface to explore customer, product, and order data through real-time aggregations, joins, and filters — without writing SQL manually.

## Overview

This project simulates a real-world e-commerce backend and analytics layer. It integrates a normalized MySQL database with a Flask web application to let users view KPIs, search and filter records, and insert new data through a clean, dark-themed UI.

## Dataset

Built on a synthetic e-commerce dataset (via Kaggle) covering:
- **Users** — ~5,000 records (id, name, email, city, gender, signup date)
- **Products** — ~2,000 records (id, name, category, brand, price)
- **Orders** — ~10,000 records (id, user, date, status, total amount)
- **Order Items** — ~21,900 records (order/product line items, quantity, pricing)

## Features

- **Dashboard** — live KPIs: total customers, products, orders, and revenue; recent orders, top products, and revenue by city
- **Customers** — searchable, filterable customer list with order count and total spend per customer
- **Products** — searchable, filterable product catalog with units sold per product
- **Orders** — full order details via multi-table joins (users → orders → order_items → products), filterable by status and search
- **Add Data** — forms to insert new customers, products, and orders directly into the database

## Tech Stack

- **Backend:** Python, Flask
- **Database:** MySQL (via `mysql.connector`)
- **Frontend:** HTML, CSS (custom dark theme)
- **Tools:** MySQL Workbench, VS Code

## Database Design

Four related tables (`users`, `products`, `orders`, `order_items`) connected via primary/foreign keys, normalized up to 3NF to eliminate redundancy and maintain referential integrity. Aggregate queries (`COUNT`, `SUM`, `GROUP BY`) and multi-table `JOIN`s power the dashboard's analytics views.

## Setup

1. Clone the repo and install dependencies:
```bash
   pip install -r requirements.txt
```
2. Create a `.env` file with your database credentials:
   DB_HOST=localhost
   DB_NAME=onlineshoppingdb
   DB_USER=root
   DB_PASSWORD=your_password

3. Set up the MySQL schema and import the dataset (see `schema_check.sql`).
4. Run the app:
```bash
   python app.py
```
## Preview

<img width="929" height="411" alt="image" src="https://github.com/user-attachments/assets/f6f834e1-410a-4743-9afe-cbb71fee2cad" />

<img width="918" height="415" alt="image" src="https://github.com/user-attachments/assets/25fe9c17-f86b-4efd-8b70-cf48f46c2acc" />

<img width="926" height="419" alt="image" src="https://github.com/user-attachments/assets/13ea09ff-1713-46f6-861d-d91ce4f8b527" />

<img width="931" height="407" alt="image" src="https://github.com/user-attachments/assets/55224c93-9dfd-4c22-b928-b34be96061e5" />

<img width="932" height="347" alt="image" src="https://github.com/user-attachments/assets/6a59931c-e2c9-48b2-b548-26efc9cbe87e" />

## References

- [Kaggle E-commerce Dataset](https://www.kaggle.com/datasets/abhayayare/e-commerce-dataset)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
