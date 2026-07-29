# OnlineShopping DB — Flask GUI

## Setup
1. Install dependencies:
   pip install flask mysql-connector-python

2. Update DB credentials in app.py:
   DB_CONFIG = {
       'host': 'localhost',
       'database': 'onlineshoppingdb',
       'user': 'root',
       'password': 'YOUR_PASSWORD'
   }

3. Run:
   python app.py

4. Open: http://localhost:5000

## Pages
- / → Dashboard with stats, recent orders, top products
- /customers → Customer list with search + city filter
- /products → Product catalog with search + category filter
- /orders → Joined orders view (users + orders + order_items + products)
- /add → Insert customers, products, and orders
# Sales-Analytics-Dashboard
