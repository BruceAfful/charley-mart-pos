import sqlite3

DATABASE_NAME = "charley_mart.db"


def connect_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

    print("Database and products table created successfully!")


def add_product(barcode, name, price, stock_quantity):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO products (barcode, name, price, stock_quantity)
        VALUES (?, ?, ?, ?)
        """, (barcode, name, price, stock_quantity))

        conn.commit()

        print(f"{name} added successfully!")

    except sqlite3.IntegrityError:
        print(f"Product with barcode {barcode} already exists!")

    conn.close()


def view_products():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")

    products = cursor.fetchall()

    conn.close()

    return products


def find_product_by_barcode(barcode):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM products WHERE barcode = ?
    """, (barcode,))

    product = cursor.fetchone()

    conn.close()

    return product


def update_stock(product_id, quantity_sold):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE products
    SET stock_quantity = stock_quantity - ?
    WHERE id = ?
    """, (quantity_sold, product_id))

    conn.commit()
    conn.close()