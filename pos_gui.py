import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from database import (
    create_tables,
    add_product,
    find_product_by_barcode,
    update_stock
)

# DATABASE SETUP
create_tables()

# SAMPLE PRODUCTS
add_product("1001", "Coca Cola", 15.00, 20)
add_product("1002", "Indomie Noodles", 7.50, 50)
add_product("1003", "Milo 400g", 35.00, 15)

# ── COLOUR PALETTE ──────────────────────────────────────────
BG         = "#0F1923"   # deep navy background
PANEL      = "#162030"   # slightly lighter panel
CARD       = "#1E2D3D"   # card / row surfaces
ACCENT     = "#00C896"   # emerald-green accent
ACCENT2    = "#FF6B35"   # warm orange (remove / danger)
TEXT       = "#E8F4F8"   # near-white text
MUTED      = "#7A9BB5"   # secondary / muted text
BORDER     = "#253545"   # subtle border
HIGHLIGHT  = "#0D3349"   # treeview selected row
WHITE      = "#FFFFFF"

# ── FONTS ───────────────────────────────────────────────────
F_TITLE    = ("Courier New", 22, "bold")
F_SUB      = ("Courier New", 11, "bold")
F_LABEL    = ("Courier New", 12)
F_ENTRY    = ("Courier New", 14)
F_TOTAL    = ("Courier New", 26, "bold")
F_BTN      = ("Courier New", 12, "bold")
F_HDR      = ("Courier New", 11, "bold")
F_SMALL    = ("Courier New", 9)

# ── ROOT WINDOW ─────────────────────────────────────────────
root = tk.Tk()
root.title("Charley Mart POS")
root.geometry("1100x720")
root.configure(bg=BG)
root.resizable(False, False)

# ── CART STORAGE ────────────────────────────────────────────
cart = {}
total_amount = 0


# ════════════════════════════════════════════════════════════
#   HELPERS
# ════════════════════════════════════════════════════════════

def make_btn(parent, text, color, command, width=16):
    """Flat, borderless button with hover effect."""
    btn = tk.Button(
        parent,
        text=text,
        font=F_BTN,
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        relief="flat",
        bd=0,
        width=width,
        height=2,
        cursor="hand2",
        command=command,
    )
    # subtle hover lighten
    def on_enter(e):
        btn.config(bg=_lighten(color))
    def on_leave(e):
        btn.config(bg=color)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def _lighten(hex_color, amount=30):
    """Lighten a hex colour by a fixed amount."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = min(255, r + amount)
    g = min(255, g + amount)
    b = min(255, b + amount)
    return f"#{r:02x}{g:02x}{b:02x}"


def styled_separator(parent, pady=0):
    sep = tk.Frame(parent, bg=BORDER, height=1)
    sep.pack(fill="x", pady=pady)
    return sep


# ════════════════════════════════════════════════════════════
#   TREEVIEW STYLE
# ════════════════════════════════════════════════════════════
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "POS.Treeview",
    background=CARD,
    foreground=TEXT,
    fieldbackground=CARD,
    rowheight=38,
    font=("Courier New", 11),
    borderwidth=0,
)
style.configure(
    "POS.Treeview.Heading",
    background=BORDER,
    foreground=ACCENT,
    font=F_HDR,
    relief="flat",
    borderwidth=0,
)
style.map(
    "POS.Treeview",
    background=[("selected", HIGHLIGHT)],
    foreground=[("selected", ACCENT)],
)

# ════════════════════════════════════════════════════════════
#   LAYOUT SKELETON
# ════════════════════════════════════════════════════════════

# ── LEFT COLUMN (main POS area) ─────────────────────────────
left = tk.Frame(root, bg=BG)
left.place(x=0, y=0, width=760, height=720)

# ── RIGHT COLUMN (sidebar) ──────────────────────────────────
right = tk.Frame(root, bg=PANEL)
right.place(x=760, y=0, width=340, height=720)

# thin accent line between columns
tk.Frame(root, bg=ACCENT, width=2, height=720).place(x=758, y=0)


# ════════════════════════════════════════════════════════════
#   LEFT — HEADER
# ════════════════════════════════════════════════════════════

header = tk.Frame(left, bg=BG)
header.pack(fill="x", padx=24, pady=(20, 0))

tk.Label(
    header,
    text="● CHARLEY MART",
    font=F_TITLE,
    bg=BG,
    fg=ACCENT,
).pack(side="left")

tk.Label(
    header,
    text="POINT OF SALE",
    font=F_SMALL,
    bg=BG,
    fg=MUTED,
).pack(side="right", anchor="s", pady=(0, 4))

styled_separator(left, pady=(12, 0))


# ════════════════════════════════════════════════════════════
#   LEFT — BARCODE STRIP
# ════════════════════════════════════════════════════════════

scan_frame = tk.Frame(left, bg=CARD)
scan_frame.pack(fill="x", padx=24, pady=16)

tk.Label(
    scan_frame,
    text="  ▶  SCAN / ENTER BARCODE",
    font=F_SUB,
    bg=CARD,
    fg=MUTED,
    anchor="w",
).pack(fill="x", padx=12, pady=(10, 4))

entry_row = tk.Frame(scan_frame, bg=CARD)
entry_row.pack(fill="x", padx=12, pady=(0, 10))

barcode_entry = tk.Entry(
    entry_row,
    font=F_ENTRY,
    bg=BG,
    fg=ACCENT,
    insertbackground=ACCENT,
    relief="flat",
    bd=0,
    highlightthickness=2,
    highlightcolor=ACCENT,
    highlightbackground=BORDER,
)
barcode_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 10))


# ════════════════════════════════════════════════════════════
#   LEFT — CART TABLE
# ════════════════════════════════════════════════════════════

table_frame = tk.Frame(left, bg=BG)
table_frame.pack(fill="both", expand=True, padx=24)

columns = ("Product", "Unit Price", "Qty", "Subtotal")

cart_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    style="POS.Treeview",
    selectmode="browse",
)

col_widths = {"Product": 280, "Unit Price": 120, "Qty": 80, "Subtotal": 120}
for col in columns:
    cart_table.heading(col, text=col.upper())
    cart_table.column(col, width=col_widths[col], anchor="center")
cart_table.column("Product", anchor="w")

# scrollbar
sb = ttk.Scrollbar(table_frame, orient="vertical", command=cart_table.yview)
cart_table.configure(yscrollcommand=sb.set)

cart_table.pack(side="left", fill="both", expand=True)
sb.pack(side="right", fill="y")

# alternating row colours
cart_table.tag_configure("odd",  background=CARD)
cart_table.tag_configure("even", background="#192837")


# ════════════════════════════════════════════════════════════
#   LEFT — BOTTOM BUTTONS
# ════════════════════════════════════════════════════════════

styled_separator(left, pady=(12, 0))

btn_bar = tk.Frame(left, bg=BG)
btn_bar.pack(fill="x", padx=24, pady=16)

remove_btn = make_btn(btn_bar, "⊖  REMOVE ITEM",  ACCENT2,  lambda: remove_item(), width=18)
remove_btn.pack(side="left", padx=(0, 10))

clear_btn  = make_btn(btn_bar, "✕  CLEAR CART",   "#4A3040", lambda: clear_cart(),  width=18)
clear_btn.pack(side="left")

# item count badge (bottom right of left panel)
item_count_var = tk.StringVar(value="0 items")
tk.Label(
    btn_bar,
    textvariable=item_count_var,
    font=F_SMALL,
    bg=BG,
    fg=MUTED,
).pack(side="right", padx=4)


# ════════════════════════════════════════════════════════════
#   RIGHT SIDEBAR
# ════════════════════════════════════════════════════════════

# ── Store badge ─────────────────────────────────────────────
tk.Label(
    right,
    text="🛒",
    font=("Courier New", 36),
    bg=PANEL,
    fg=ACCENT,
).pack(pady=(30, 4))

tk.Label(
    right,
    text="CHARLEY MART",
    font=("Courier New", 13, "bold"),
    bg=PANEL,
    fg=TEXT,
).pack()

tk.Label(
    right,
    text="Retail Management System",
    font=F_SMALL,
    bg=PANEL,
    fg=MUTED,
).pack(pady=(2, 16))

styled_separator(right, pady=0)

# ── Total display ────────────────────────────────────────────
total_card = tk.Frame(right, bg=CARD)
total_card.pack(fill="x", padx=20, pady=20)

tk.Label(
    total_card,
    text="ORDER TOTAL",
    font=F_SMALL,
    bg=CARD,
    fg=MUTED,
).pack(pady=(14, 4))

total_label = tk.Label(
    total_card,
    text="GHS 0.00",
    font=F_TOTAL,
    bg=CARD,
    fg=ACCENT,
)
total_label.pack(pady=(0, 14))

# ── Quick stats ──────────────────────────────────────────────
stats_frame = tk.Frame(right, bg=PANEL)
stats_frame.pack(fill="x", padx=20, pady=(0, 20))

items_frame = tk.Frame(stats_frame, bg=BORDER)
items_frame.pack(fill="x", pady=2)

tk.Label(items_frame, text="ITEMS IN CART", font=F_SMALL, bg=BORDER, fg=MUTED).pack(side="left", padx=12, pady=8)
items_count_label = tk.Label(items_frame, text="0", font=("Courier New", 12, "bold"), bg=BORDER, fg=TEXT)
items_count_label.pack(side="right", padx=12)

lines_frame = tk.Frame(stats_frame, bg=CARD)
lines_frame.pack(fill="x", pady=2)

tk.Label(lines_frame, text="PRODUCT LINES", font=F_SMALL, bg=CARD, fg=MUTED).pack(side="left", padx=12, pady=8)
lines_label = tk.Label(lines_frame, text="0", font=("Courier New", 12, "bold"), bg=CARD, fg=TEXT)
lines_label.pack(side="right", padx=12)

styled_separator(right, pady=0)

# ── Checkout button ───────────────────────────────────────────
checkout_btn = make_btn(right, "⬤  CHECKOUT", ACCENT, lambda: checkout(), width=26)
checkout_btn.pack(padx=20, pady=24, fill="x")

# ── Last action status ────────────────────────────────────────
status_var = tk.StringVar(value="Ready — scan a product")
status_label = tk.Label(
    right,
    textvariable=status_var,
    font=F_SMALL,
    bg=PANEL,
    fg=MUTED,
    wraplength=290,
    justify="center",
)
status_label.pack(padx=20)

# ── Version footer ────────────────────────────────────────────
tk.Label(
    right,
    text="v1.0  |  Charley Mart POS",
    font=F_SMALL,
    bg=PANEL,
    fg="#2A3A4A",
).place(x=0, y=690, width=340)


# ════════════════════════════════════════════════════════════
#   CORE LOGIC  (unchanged from your original)
# ════════════════════════════════════════════════════════════

def refresh_cart():
    global total_amount

    for row in cart_table.get_children():
        cart_table.delete(row)

    total_amount = 0
    total_qty    = 0

    for idx, product_id in enumerate(cart):
        item = cart[product_id]
        tag  = "odd" if idx % 2 == 0 else "even"

        cart_table.insert(
            "", tk.END,
            iid=str(product_id),
            values=(
                item["name"],
                f"GHS {item['price']:.2f}",
                item["quantity"],
                f"GHS {item['subtotal']:.2f}",
            ),
            tags=(tag,),
        )

        total_amount += item["subtotal"]
        total_qty    += item["quantity"]

    total_label.config(text=f"GHS {total_amount:.2f}")
    item_count_var.set(f"{total_qty} item{'s' if total_qty != 1 else ''}")
    items_count_label.config(text=str(total_qty))
    lines_label.config(text=str(len(cart)))


def scan_product(event=None):
    barcode = barcode_entry.get().strip()
    if not barcode:
        return

    product = find_product_by_barcode(barcode)

    if product:
        product_id    = product[0]
        product_name  = product[2]
        product_price = product[3]
        stock_qty     = product[4]

        if stock_qty <= 0:
            messagebox.showerror("Out of Stock", f"{product_name} is out of stock!")
            barcode_entry.delete(0, tk.END)
            return

        if product_id in cart:
            cart[product_id]["quantity"] += 1
            cart[product_id]["subtotal"]  = (
                cart[product_id]["quantity"] * cart[product_id]["price"]
            )
            status_var.set(f"↑ Qty updated: {product_name}")
        else:
            cart[product_id] = {
                "name":     product_name,
                "price":    product_price,
                "quantity": 1,
                "subtotal": product_price,
            }
            status_var.set(f"✓ Added: {product_name}")

        refresh_cart()
        barcode_entry.delete(0, tk.END)

    else:
        messagebox.showerror("Not Found", "Product not found!")
        status_var.set("✗ Barcode not recognised")
        barcode_entry.delete(0, tk.END)


def remove_item():
    selected = cart_table.selection()
    if not selected:
        messagebox.showwarning("Nothing Selected", "Click a row first, then Remove Item.")
        return

    product_id = int(selected[0])
    name = cart[product_id]["name"]
    del cart[product_id]
    refresh_cart()
    status_var.set(f"✗ Removed: {name}")


def clear_cart():
    global cart
    if not cart:
        return
    if messagebox.askyesno("Clear Cart", "Remove all items from the cart?"):
        cart = {}
        refresh_cart()
        status_var.set("Cart cleared")


def checkout():
    global cart

    if not cart:
        messagebox.showwarning("Empty Cart", "Add products before checking out.")
        return

    payment = simpledialog.askfloat(
        "Payment",
        f"Total: GHS {total_amount:.2f}\n\nEnter amount paid (GHS):",
        parent=root,
    )

    if payment is None:
        return

    if payment < total_amount:
        messagebox.showerror("Insufficient Payment",
                             f"GHS {payment:.2f} is less than GHS {total_amount:.2f}.")
        return

    change = payment - total_amount

    for product_id in cart:
        update_stock(product_id, cart[product_id]["quantity"])

    messagebox.showinfo(
        "Sale Complete ✓",
        f"  Paid   : GHS {payment:.2f}\n"
        f"  Total  : GHS {total_amount:.2f}\n"
        f"  Change : GHS {change:.2f}\n\n"
        f"  Thank you for shopping at Charley Mart!",
    )

    cart = {}
    refresh_cart()
    status_var.set("Sale complete — ready for next customer")


# ════════════════════════════════════════════════════════════
#   BIND & LAUNCH
# ════════════════════════════════════════════════════════════

barcode_entry.bind("<Return>", scan_product)

scan_btn = make_btn(entry_row, "SCAN ↵", ACCENT, scan_product, width=10)
scan_btn.pack(side="left")

barcode_entry.focus()
root.mainloop()