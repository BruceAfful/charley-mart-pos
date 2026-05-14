import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    create_tables,
    add_product,
    get_all_products,
    update_product,
    delete_product
)

# DATABASE
create_tables()

# COLORS
BG      = "#0F1923"
CARD    = "#1E2D3D"
ACCENT  = "#00C896"
TEXT    = "#E8F4F8"
MUTED   = "#7A9BB5"
WHITE   = "#FFFFFF"
WARNING = "#FF6B35"
DANGER  = "#C0392B"

# FONTS
TITLE_FONT  = ("Courier New", 22, "bold")
LABEL_FONT  = ("Courier New", 12)
BUTTON_FONT = ("Courier New", 12, "bold")

# WINDOW
root = tk.Tk()

root.title("Product Manager")
root.geometry("1000x700")
root.configure(bg=BG)

# CURRENT SELECTED PRODUCT
selected_product_id = None

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

# PRODUCT TABLE
columns = (
    "ID",
    "Barcode",
    "Name",
    "Price",
    "Stock"
)

table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for col in columns:

    table.heading(col, text=col)
    table.column(col, width=180)

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


# CLEAR FORM
def clear_form():

    global selected_product_id

    selected_product_id = None

    barcode_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    stock_entry.delete(0, tk.END)


# VALIDATE FORM FIELDS
def get_form_values():

    barcode = barcode_entry.get().strip()
    name = name_entry.get().strip()
    price_str = price_entry.get().strip()
    stock_str = stock_entry.get().strip()

    if not barcode or not name or not price_str or not stock_str:
        messagebox.showwarning(
            "Missing Fields",
            "Please fill in all fields before saving."
        )
        return None

    try:
        price = float(price_str)
    except ValueError:
        messagebox.showerror(
            "Invalid Price",
            "Price must be a valid number."
        )
        return None

    try:
        stock = int(stock_str)
    except ValueError:
        messagebox.showerror(
            "Invalid Stock",
            "Stock quantity must be a whole number."
        )
        return None

    if price < 0 or stock < 0:
        messagebox.showerror(
            "Invalid Values",
            "Price and stock cannot be negative."
        )
        return None

    return barcode, name, price, stock


# SAVE NEW PRODUCT
def save_product():

    values = get_form_values()

    if values is None:
        return

    barcode, name, price, stock = values

    add_product(barcode, name, price, stock)

    messagebox.showinfo(
        "Success",
        f"{name} added successfully!"
    )

    clear_form()

    load_products()


# SELECT PRODUCT FROM TABLE
def select_product(event):

    global selected_product_id

    selected = table.selection()

    if not selected:
        return

    values = table.item(selected[0])["values"]

    selected_product_id = values[0]

    barcode = values[1]
    name = values[2]
    price = str(values[3]).replace("GHS ", "")
    stock = values[4]

    clear_form()

    selected_product_id = values[0]

    barcode_entry.insert(0, barcode)
    name_entry.insert(0, name)
    price_entry.insert(0, price)
    stock_entry.insert(0, stock)


# UPDATE EXISTING PRODUCT
def edit_product():

    global selected_product_id

    if selected_product_id is None:

        messagebox.showwarning(
            "No Selection",
            "Select a product from the table first."
        )

        return

    values = get_form_values()

    if values is None:
        return

    barcode, name, price, stock = values

    update_product(
        selected_product_id,
        barcode,
        name,
        price,
        stock
    )

    messagebox.showinfo(
        "Updated",
        f"{name} updated successfully!"
    )

    clear_form()

    load_products()


# DELETE PRODUCT
def remove_product():

    global selected_product_id

    if selected_product_id is None:

        messagebox.showwarning(
            "No Selection",
            "Select a product from the table first."
        )

        return

    name = name_entry.get().strip() or "this product"

    confirmed = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete '{name}'?\n"
        "This cannot be undone."
    )

    if not confirmed:
        return

    delete_product(selected_product_id)

    messagebox.showinfo(
        "Deleted",
        f"'{name}' has been removed."
    )

    clear_form()

    load_products()


# BIND TABLE CLICK
table.bind("<<TreeviewSelect>>", select_product)

# BUTTON FRAME
button_frame = tk.Frame(root, bg=BG)
button_frame.pack(pady=10)

# ADD BUTTON
save_btn = tk.Button(
    button_frame,
    text="ADD PRODUCT",
    font=BUTTON_FONT,
    bg=ACCENT,
    fg=WHITE,
    relief="flat",
    width=18,
    command=save_product
)

save_btn.pack(side="left", padx=10)

# UPDATE BUTTON
update_btn = tk.Button(
    button_frame,
    text="UPDATE PRODUCT",
    font=BUTTON_FONT,
    bg=WARNING,
    fg=WHITE,
    relief="flat",
    width=18,
    command=edit_product
)

update_btn.pack(side="left", padx=10)

# DELETE BUTTON
delete_btn = tk.Button(
    button_frame,
    text="DELETE PRODUCT",
    font=BUTTON_FONT,
    bg=DANGER,
    fg=WHITE,
    relief="flat",
    width=18,
    command=remove_product
)

delete_btn.pack(side="left", padx=10)

# CLEAR BUTTON
clear_btn = tk.Button(
    button_frame,
    text="CLEAR FORM",
    font=BUTTON_FONT,
    bg="#444",
    fg=WHITE,
    relief="flat",
    width=18,
    command=clear_form
)

clear_btn.pack(side="left", padx=10)

# INITIAL LOAD
load_products()

# RUN
root.mainloop()