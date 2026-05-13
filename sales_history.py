import tkinter as tk
from tkinter import ttk, messagebox
import os

# COLORS
BG = "#0F1923"
CARD = "#1E2D3D"
ACCENT = "#00C896"
TEXT = "#E8F4F8"
MUTED = "#7A9BB5"
WHITE = "#FFFFFF"

# WINDOW
root = tk.Tk()

root.title("Charley Mart - Sales History")
root.geometry("1000x700")
root.configure(bg=BG)

# TITLE
title = tk.Label(
    root,
    text="SALES HISTORY",
    font=("Courier New", 24, "bold"),
    bg=BG,
    fg=ACCENT
)

title.pack(pady=20)

# TABLE FRAME
table_frame = tk.Frame(root, bg=BG)
table_frame.pack(fill="both", expand=True, padx=20, pady=20)

# TABLE
columns = ("Receipt File",)

history_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=25
)

history_table.heading("Receipt File", text="Receipt File")
history_table.column("Receipt File", width=900)

history_table.pack(side="left", fill="both", expand=True)

# SCROLLBAR
scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=history_table.yview
)

history_table.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")


# LOAD RECEIPTS
def load_receipts():

    # CLEAR TABLE
    for row in history_table.get_children():
        history_table.delete(row)

    # CREATE RECEIPTS FOLDER IF MISSING
    os.makedirs("receipts", exist_ok=True)

    # GET FILES
    files = os.listdir("receipts")

    # SORT NEWEST FIRST
    files.sort(reverse=True)

    for file in files:

        history_table.insert(
            "",
            tk.END,
            values=(file,)
        )


# OPEN RECEIPT
def open_receipt():

    selected = history_table.selection()

    if not selected:

        messagebox.showwarning(
            "No Selection",
            "Select a receipt first."
        )

        return

    filename = history_table.item(selected[0])["values"][0]

    filepath = os.path.join("receipts", filename)

    # READ FILE
    with open(filepath, "r") as file:

        content = file.read()

    # NEW WINDOW
    receipt_window = tk.Toplevel(root)

    receipt_window.title(filename)
    receipt_window.geometry("600x700")
    receipt_window.configure(bg=BG)

    # TEXT AREA
    text_area = tk.Text(
        receipt_window,
        font=("Courier New", 12),
        bg=CARD,
        fg=TEXT,
        insertbackground=WHITE,
        relief="flat"
    )

    text_area.pack(fill="both", expand=True, padx=20, pady=20)

    text_area.insert("1.0", content)

    text_area.config(state="disabled")


# OPEN BUTTON
open_btn = tk.Button(
    root,
    text="OPEN RECEIPT",
    font=("Courier New", 12, "bold"),
    bg=ACCENT,
    fg=WHITE,
    relief="flat",
    width=20,
    height=2,
    command=open_receipt
)

open_btn.pack(pady=10)

# INITIAL LOAD
load_receipts()

# RUN
root.mainloop()