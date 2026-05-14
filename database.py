import sqlite3
import hashlib

DATABASE_NAME = "pos_system.db"


def connect_db():

    conn = sqlite3.connect(DATABASE_NAME)

    return conn


def create_tables():

    conn = connect_db()

    cursor = conn.cursor()

    # PRODUCTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock_quantity INTEGER DEFAULT 0
    )
    """)

    # SALES TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_amount REAL NOT NULL,
        payment REAL NOT NULL,
        change_amount REAL NOT NULL,
        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # SALE ITEMS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sale_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sale_id INTEGER,
        product_name TEXT,
        quantity INTEGER,
        unit_price REAL,
        subtotal REAL,

        FOREIGN KEY (sale_id)
        REFERENCES sales(id)
    )
    """)

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    conn.commit()

    conn.close()

    print("Database tables ready!")


# ADD PRODUCT
def add_product(barcode, name, price, stock_quantity):

    conn = connect_db()

    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO products (
            barcode,
            name,
            price,
            stock_quantity
        )
        VALUES (?, ?, ?, ?)
        """, (
            barcode,
            name,
            price,
            stock_quantity
        ))

        conn.commit()

        print(f"{name} added successfully!")

    except sqlite3.IntegrityError:

        print(
            f"Product with barcode "
            f"{barcode} already exists!"
        )

    conn.close()


# FIND PRODUCT BY BARCODE
def find_product_by_barcode(barcode):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM products
    WHERE barcode = ?
    """, (barcode,))

    product = cursor.fetchone()

    conn.close()

    return product


# UPDATE STOCK
def update_stock(product_id, quantity_sold):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE products
    SET stock_quantity = stock_quantity - ?
    WHERE id = ?
    """, (
        quantity_sold,
        product_id
    ))

    conn.commit()

    conn.close()


# GET ALL PRODUCTS
def get_all_products():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM products
    ORDER BY name ASC
    """)

    products = cursor.fetchall()

    conn.close()

    return products


# SAVE SALE
def save_sale(cart, total_amount, payment, change):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO sales (
        total_amount,
        payment,
        change_amount
    )
    VALUES (?, ?, ?)
    """, (
        total_amount,
        payment,
        change
    ))

    sale_id = cursor.lastrowid

    for product_id in cart:

        item = cart[product_id]

        cursor.execute("""
        INSERT INTO sale_items (
            sale_id,
            product_name,
            quantity,
            unit_price,
            subtotal
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            sale_id,
            item["name"],
            item["quantity"],
            item["price"],
            item["subtotal"]
        ))

    conn.commit()

    conn.close()

    return sale_id


# TOTAL SALES REVENUE
def get_total_sales():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT IFNULL(SUM(total_amount), 0)
    FROM sales
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# TOTAL TRANSACTIONS
def get_total_transactions():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM sales
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


# TOTAL PRODUCTS SOLD
def get_total_products_sold():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT IFNULL(SUM(quantity), 0)
    FROM sale_items
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# TOP SELLING PRODUCTS
def get_top_products():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        product_name,
        SUM(quantity) as total_qty
    FROM sale_items
    GROUP BY product_name
    ORDER BY total_qty DESC
    LIMIT 5
    """)

    products = cursor.fetchall()

    conn.close()

    return products


# LOW STOCK PRODUCTS
def get_low_stock_products():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        name,
        stock_quantity
    FROM products
    WHERE stock_quantity <= 5
    ORDER BY stock_quantity ASC
    """)

    products = cursor.fetchall()

    conn.close()

    return products


# UPDATE PRODUCT
def update_product(
    product_id,
    barcode,
    name,
    price,
    stock_quantity
):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE products
    SET
        barcode = ?,
        name = ?,
        price = ?,
        stock_quantity = ?
    WHERE id = ?
    """, (
        barcode,
        name,
        price,
        stock_quantity,
        product_id
    ))

    conn.commit()

    conn.close()


# DELETE PRODUCT
def delete_product(product_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM products
    WHERE id = ?
    """, (product_id,))

    conn.commit()

    conn.close()


# HASH PASSWORD
def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# CREATE DEFAULT ADMIN USER
def create_default_users():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE username = 'admin'
    """)

    existing_admin = cursor.fetchone()

    if not existing_admin:

        hashed_password = hash_password("admin123")

        cursor.execute("""
        INSERT INTO users (
            username,
            password,
            role
        )
        VALUES (?, ?, ?)
        """, (
            "admin",
            hashed_password,
            "admin"
        ))

        print("Default admin created!")

    conn.commit()

    conn.close()


# CREATE DEFAULT CASHIER USER
def create_cashier_user():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE username = 'cashier'
    """)

    existing_cashier = cursor.fetchone()

    if not existing_cashier:

        hashed_password = hash_password("cash123")

        cursor.execute("""
        INSERT INTO users (
            username,
            password,
            role
        )
        VALUES (?, ?, ?)
        """, (
            "cashier",
            hashed_password,
            "cashier"
        ))

        print("Default cashier created!")

    conn.commit()

    conn.close()


# VERIFY LOGIN
def verify_login(username, password):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, username, password, role
    FROM users
    WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    if user:

        stored_password = user[2]

        hashed_input = hash_password(password)

        if hashed_input == stored_password:

            return {
                "id": user[0],
                "username": user[1],
                "role": user[3]
            }

    return None

# DELETE PRODUCT
def delete_product(product_id):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM products
    WHERE id = ?
    """, (product_id,))

    conn.commit()

    conn.close()