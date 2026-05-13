import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    create_tables,
    add_product,
    get_all_products
)

# DATABASE
create_tables()

# WINDOW
root = tk.Tk()

root.title("Charley Mart - Product Manager")
root.geometry("900x650")
root.configure(bg="#0F1923")

# COLORS
BG = "#0F1923"
CARD = "#1E2D3D"
ACCENT = "#00C896"
TEXT = "#E8F4F8"
MUTED = "#7A9BB5"
WHITE = "#FFFFFF"

# FONTS
TITLE_FONT = ("Courier New", 22, "bold")
LABEL_FONT = ("Courier New", 12)
BUTTON_FONT = ("Courier New", 12, "bold")

# TITLE
title = tk.Label(
    root,
    text="PRODUCT MANAGEMENT",
    font=TITLE_FONT,
    bg=BG,
    fg=ACCENT
)

title.pack(pady=20)

# FORM FRAME
form_frame = tk.Frame(root, bg=CARD)
form_frame.pack(fill="x", padx=20, pady=10)

# BARCODE
tk.Label(
    form_frame,
    text="Barcode",
    font=LABEL_FONT,
    bg=CARD,
    fg=TEXT
).grid(row=0, column=0, padx=10, pady=10)

barcode_entry = tk.Entry(
    form_frame,
    font=LABEL_FONT,
    width=25
)

barcode_entry.grid(row=0, column=1, padx=10)

# PRODUCT NAME
tk.Label(
    form_frame,
    text="Product Name",
    font=LABEL_FONT,
    bg=CARD,
    fg=TEXT
).grid(row=1, column=0, padx=10, pady=10)

name_entry = tk.Entry(
    form_frame,
    font=LABEL_FONT,
    width=25
)

name_entry.grid(row=1, column=1, padx=10)

# PRICE
tk.Label(
    form_frame,
    text="Price",
    font=LABEL_FONT,
    bg=CARD,
    fg=TEXT
).grid(row=2, column=0, padx=10, pady=10)

price_entry = tk.Entry(
    form_frame,
    font=LABEL_FONT,
    width=25
)

price_entry.grid(row=2, column=1, padx=10)

# STOCK
tk.Label(
    form_frame,
    text="Stock Quantity",
    font=LABEL_FONT,
    bg=CARD,
    fg=TEXT
).grid(row=3, column=0, padx=10, pady=10)

stock_entry = tk.Entry(
    form_frame,
    font=LABEL_FONT,
    width=25
)

stock_entry.grid(row=3, column=1, padx=10)


# TABLE
columns = ("ID", "Barcode", "Name", "Price", "Stock")

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150)

table.pack(fill="both", expand=True, padx=20, pady=20)


# LOAD PRODUCTS
def load_products():

    for row in table.get_children():
        table.delete(row)

    products = get_all_products()

    for product in products:

        table.insert("", tk.END, values=(
            product[0],
            product[1],
            product[2],
            f"GHS {product[3]:.2f}",
            product[4]
        ))


# ADD PRODUCT
def save_product():

    try:

        barcode = barcode_entry.get()
        name = name_entry.get()
        price = float(price_entry.get())
        stock = int(stock_entry.get())

        add_product(barcode, name, price, stock)

        messagebox.showinfo(
            "Success",
            f"{name} added successfully!"
        )

        barcode_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        stock_entry.delete(0, tk.END)

        load_products()

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# SAVE BUTTON
save_btn = tk.Button(
    form_frame,
    text="ADD PRODUCT",
    font=BUTTON_FONT,
    bg=ACCENT,
    fg=WHITE,
    relief="flat",
    command=save_product
)

save_btn.grid(row=4, column=0, columnspan=2, pady=20)

# INITIAL LOAD
load_products()

# RUN
root.mainloop()