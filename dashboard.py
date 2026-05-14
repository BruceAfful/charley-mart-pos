import tkinter as tk
from tkinter import ttk

from database import (
    create_tables,
    get_total_sales,
    get_total_transactions,
    get_total_products_sold,
    get_top_products,
    get_low_stock_products
)

# DATABASE
create_tables()

# COLORS
BG      = "#0F1923"
CARD    = "#1E2D3D"
ACCENT  = "#00C896"
TEXT    = "#E8F4F8"
MUTED   = "#7A9BB5"
WARNING = "#FF6B35"

# WINDOW
root = tk.Tk()

root.title("Sales Analytics Dashboard")
root.geometry("1100x700")
root.configure(bg=BG)

# TITLE
title = tk.Label(
    root,
    text="SALES ANALYTICS DASHBOARD",
    font=("Courier New", 24, "bold"),
    bg=BG,
    fg=ACCENT
)

title.pack(pady=20)

# TOP CARDS FRAME
cards_frame = tk.Frame(root, bg=BG)
cards_frame.pack(fill="x", padx=20)


# CARD FACTORY
def create_card(parent, title_text, value_text):

    card = tk.Frame(
        parent,
        bg=CARD,
        width=250,
        height=120
    )

    card.pack(side="left", padx=10)
    card.pack_propagate(False)

    tk.Label(
        card,
        text=title_text,
        font=("Courier New", 12),
        bg=CARD,
        fg=MUTED
    ).pack(pady=(20, 10))

    tk.Label(
        card,
        text=value_text,
        font=("Courier New", 22, "bold"),
        bg=CARD,
        fg=ACCENT
    ).pack()

    return card


# FETCH DATA
total_sales        = get_total_sales()
total_transactions = get_total_transactions()
total_products     = get_total_products_sold()

# SUMMARY CARDS
create_card(
    cards_frame,
    "TOTAL REVENUE",
    f"GHS {total_sales:.2f}"
)

create_card(
    cards_frame,
    "TRANSACTIONS",
    str(total_transactions)
)

create_card(
    cards_frame,
    "PRODUCTS SOLD",
    str(total_products)
)

# MAIN CONTENT FRAME
content_frame = tk.Frame(root, bg=BG)
content_frame.pack(fill="both", expand=True, padx=20, pady=20)

# TOP PRODUCTS FRAME
top_frame = tk.Frame(content_frame, bg=CARD)
top_frame.pack(side="left", fill="both", expand=True, padx=10)

# LOW STOCK FRAME
low_frame = tk.Frame(content_frame, bg=CARD)
low_frame.pack(side="left", fill="both", expand=True, padx=10)

# TOP PRODUCTS TITLE
tk.Label(
    top_frame,
    text="TOP SELLING PRODUCTS",
    font=("Courier New", 16, "bold"),
    bg=CARD,
    fg=ACCENT
).pack(pady=20)

# TOP PRODUCTS TABLE
top_table = ttk.Treeview(
    top_frame,
    columns=("Product", "Qty"),
    show="headings",
    height=15
)

top_table.heading("Product", text="Product")
top_table.heading("Qty", text="Quantity Sold")

top_table.column("Product", width=250)
top_table.column("Qty", width=120)

top_table.pack(fill="both", expand=True, padx=20, pady=20)

# LOAD TOP PRODUCTS
for product in get_top_products():

    top_table.insert(
        "",
        tk.END,
        values=product
    )

# LOW STOCK TITLE
tk.Label(
    low_frame,
    text="LOW STOCK ALERT",
    font=("Courier New", 16, "bold"),
    bg=CARD,
    fg=WARNING
).pack(pady=20)

# LOW STOCK TABLE
low_table = ttk.Treeview(
    low_frame,
    columns=("Product", "Stock"),
    show="headings",
    height=15
)

low_table.heading("Product", text="Product")
low_table.heading("Stock", text="Stock Left")

low_table.column("Product", width=250)
low_table.column("Stock", width=120)

low_table.pack(fill="both", expand=True, padx=20, pady=20)

# LOAD LOW STOCK
for product in get_low_stock_products():

    low_table.insert(
        "",
        tk.END,
        values=product
    )

# RUN
root.mainloop()