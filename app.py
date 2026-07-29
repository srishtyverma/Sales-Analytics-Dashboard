from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = 'onlineshopping_secret_key'


load_dotenv()
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}


def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"DB Error: {e}")
        return None

def get_db_cursor(conn):
    return conn.cursor(dictionary=True)

# ─── HOME / DASHBOARD ──────────────────────────────────────────────────────────

@app.route('/')
def home():
    conn = get_db_connection()
    stats = {}
    recent_orders = []
    top_products = []
    revenue_by_city = []

    if conn:
        cur = get_db_cursor(conn)

        cur.execute("SELECT COUNT(*) AS cnt FROM users")
        stats['total_customers'] = cur.fetchone()['cnt']

        cur.execute("SELECT COUNT(*) AS cnt FROM products")
        stats['total_products'] = cur.fetchone()['cnt']

        cur.execute("SELECT COUNT(*) AS cnt FROM orders")
        stats['total_orders'] = cur.fetchone()['cnt']

        cur.execute("SELECT COALESCE(SUM(total_amount),0) AS rev FROM orders WHERE order_status='Delivered'")
        stats['total_revenue'] = cur.fetchone()['rev']

        cur.execute("""
            SELECT u.name AS customer, o.order_date, o.order_status, o.total_amount
            FROM orders o
            JOIN users u ON u.user_id = o.user_id
            ORDER BY o.order_date DESC LIMIT 5
        """)
        recent_orders = cur.fetchall()

        cur.execute("""
            SELECT p.product_name, p.category, SUM(oi.quantity) AS units_sold
            FROM order_items oi
            JOIN products p ON p.product_id = oi.product_id
            GROUP BY p.product_id
            ORDER BY units_sold DESC LIMIT 5
        """)
        top_products = cur.fetchall()

        cur.execute("""
            SELECT u.city, COUNT(o.order_id) AS orders, COALESCE(SUM(o.total_amount),0) AS revenue
            FROM users u
            JOIN orders o ON o.user_id = u.user_id
            GROUP BY u.city ORDER BY revenue DESC LIMIT 5
        """)
        revenue_by_city = cur.fetchall()

        cur.close()
        conn.close()

    return render_template('home.html', stats=stats,
                           recent_orders=recent_orders,
                           top_products=top_products,
                           revenue_by_city=revenue_by_city)

# ─── CUSTOMERS ─────────────────────────────────────────────────────────────────

@app.route('/customers')
def customers():
    search = request.args.get('search', '').strip()
    city_filter = request.args.get('city', '').strip()
    conn = get_db_connection()
    customers_list = []
    cities = []

    if conn:
        cur = get_db_cursor(conn)
        cur.execute("SELECT DISTINCT city FROM users ORDER BY city")
        cities = [r['city'] for r in cur.fetchall()]

        query = """
            SELECT u.user_id, u.name, u.email, u.city, u.gender, u.signup_date,
                   COUNT(o.order_id) AS order_count,
                   COALESCE(SUM(o.total_amount),0) AS total_spent
            FROM users u
            LEFT JOIN orders o ON o.user_id = u.user_id
            WHERE 1=1
        """
        params = []
        if search:
            query += " AND (u.name LIKE %s OR u.email LIKE %s)"
            params += [f'%{search}%', f'%{search}%']
        if city_filter:
            query += " AND u.city = %s"
            params.append(city_filter)
        query += " GROUP BY u.user_id ORDER BY u.name"

        cur.execute(query, params)
        customers_list = cur.fetchall()
        cur.close()
        conn.close()

    return render_template('customers.html', customers=customers_list,
                           cities=cities, search=search, city_filter=city_filter)

# ─── PRODUCTS ──────────────────────────────────────────────────────────────────

@app.route('/products')
def products():
    search = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    conn = get_db_connection()
    products_list = []
    categories = []

    if conn:
        cur = get_db_cursor(conn)
        cur.execute("SELECT DISTINCT category FROM products ORDER BY category")
        categories = [r['category'] for r in cur.fetchall()]

        query = """
            SELECT p.product_id, p.product_name, p.category, p.brand, p.price,
                   COALESCE(SUM(oi.quantity),0) AS units_sold
            FROM products p
            LEFT JOIN order_items oi ON oi.product_id = p.product_id
            WHERE 1=1
        """
        params = []
        if search:
            query += " AND (p.product_name LIKE %s OR p.brand LIKE %s)"
            params += [f'%{search}%', f'%{search}%']
        if category_filter:
            query += " AND p.category = %s"
            params.append(category_filter)
        query += " GROUP BY p.product_id ORDER BY p.product_name"

        cur.execute(query, params)
        products_list = cur.fetchall()
        cur.close()
        conn.close()

    return render_template('products.html', products=products_list,
                           categories=categories, search=search,
                           category_filter=category_filter)

# ─── ORDERS (JOIN) ─────────────────────────────────────────────────────────────

@app.route('/orders')
def orders():
    search = request.args.get('search', '').strip()
    status_filter = request.args.get('status', '').strip()
    conn = get_db_connection()
    orders_list = []

    if conn:
        cur = get_db_cursor(conn)
        query = """
            SELECT u.name AS customer_name, u.city,
                   p.product_name, p.category,
                   oi.quantity, oi.item_price, oi.item_total AS item_total,
                   o.order_id, o.order_date, o.order_status, o.total_amount
            FROM users u
            JOIN orders o ON u.user_id = o.user_id
            JOIN order_items oi ON o.order_id = oi.order_id
            JOIN products p ON oi.product_id = p.product_id
            WHERE 1=1
        """
        params = []
        if search:
            query += " AND (u.name LIKE %s OR p.product_name LIKE %s)"
            params += [f'%{search}%', f'%{search}%']
        if status_filter:
            query += " AND o.order_status = %s"
            params.append(status_filter)
        query += " ORDER BY o.order_date DESC"

        cur.execute(query, params)
        orders_list = cur.fetchall()
        cur.close()
        conn.close()

    return render_template('orders.html', orders=orders_list,
                           search=search, status_filter=status_filter)

# ─── ADD DATA ──────────────────────────────────────────────────────────────────

@app.route('/add', methods=['GET', 'POST'])
def add_data():
    conn = get_db_connection()
    users_list = []
    products_list = []

    if conn:
        cur = get_db_cursor(conn)
        cur.execute("SELECT user_id, name FROM users ORDER BY name")
        users_list = cur.fetchall()
        cur.execute("SELECT product_id, product_name, price FROM products ORDER BY product_name")
        products_list = cur.fetchall()
        cur.close()

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'customer':
            name = request.form.get('name')
            email = request.form.get('email')
            city = request.form.get('city')
            gender = request.form.get('gender')
            signup_date = request.form.get('signup_date') or datetime.now().strftime('%Y-%m-%d')
            try:
                cur = get_db_cursor(conn)
                user_id = request.form.get('user_id')
                cur.execute("INSERT INTO users (user_id, name, email, city, gender, signup_date) VALUES (%s,%s,%s,%s,%s,%s)",
                (user_id, name, email, city, gender, signup_date))
                conn.commit()
                cur.close()
                flash('Customer added successfully!', 'success')
            except Error as e:
                flash(f'Error: {e}', 'error')

        elif form_type == 'product':
            product_name = request.form.get('product_name')
            category = request.form.get('category')
            brand = request.form.get('brand')
            price = request.form.get('price')
            try:
                cur = get_db_cursor(conn)
                product_id = request.form.get('product_id_new')
                cur.execute("INSERT INTO products (product_id, product_name, category, brand, price) VALUES (%s,%s,%s,%s,%s)",
                (product_id, product_name, category, brand, price))
                conn.commit()
                cur.close()
                flash('Product added successfully!', 'success')
            except Error as e:
                flash(f'Error: {e}', 'error')

        elif form_type == 'order':
            user_id = request.form.get('user_id')
            product_id = request.form.get('product_id')
            quantity = int(request.form.get('quantity', 1))
            order_status = request.form.get('order_status')
            order_date = request.form.get('order_date') or datetime.now().strftime('%Y-%m-%d')
            try:
                cur = get_db_cursor(conn)
                cur.execute("SELECT price FROM products WHERE product_id=%s", (product_id,))
                row = cur.fetchone()
                if row:
                    price = float(row['price'])
                    item_total = price * quantity
                    order_id_new = request.form.get('order_id_new')
                    order_item_id = request.form.get('order_item_id')
                    cur.execute("INSERT INTO orders (order_id, user_id, order_date, order_status, total_amount) VALUES (%s,%s,%s,%s,%s)",
                    (order_id_new, user_id, order_date, order_status, item_total))
                    cur.execute("INSERT INTO order_items (order_item_id, order_id, product_id, user_id, quantity, item_price, item_total) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (order_item_id, order_id_new, product_id, user_id, quantity, price, item_total))
                    conn.commit()
                    flash('Order placed successfully!', 'success')
                else:
                    flash('Product not found.', 'error')
                cur.close()
            except Error as e:
                flash(f'Error: {e}', 'error')

        if conn:
            conn.close()
        return redirect(url_for('add_data'))

    if conn:
        conn.close()
    return render_template('add_data.html', users=users_list, products=products_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
