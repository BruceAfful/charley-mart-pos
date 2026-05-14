import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

from database import (
    create_tables,
    create_default_users,
    create_cashier_user,
    verify_login
)

# DATABASE
create_tables()
create_default_users()
create_cashier_user()

# COLORS
BG    = "#0F1923"
CARD  = "#1E2D3D"
ACCENT = "#00C896"
TEXT  = "#E8F4F8"
WHITE = "#FFFFFF"

# WINDOW
root = tk.Tk()

root.title("POS System — Login")
root.geometry("500x520")
root.configure(bg=BG)
root.resizable(False, False)

# CARD
card = tk.Frame(
    root,
    bg=CARD,
    width=350,
    height=400
)

card.place(relx=0.5, rely=0.5, anchor="center")

# TITLE
title = tk.Label(
    card,
    text="POS SYSTEM",
    font=("Courier New", 24, "bold"),
    bg=CARD,
    fg=ACCENT
)

title.pack(pady=(40, 10))

subtitle = tk.Label(
    card,
    text="ROLE-BASED LOGIN",
    font=("Courier New", 12),
    bg=CARD,
    fg=TEXT
)

subtitle.pack(pady=(0, 30))

# USERNAME
username_label = tk.Label(
    card,
    text="Username",
    font=("Courier New", 12),
    bg=CARD,
    fg=TEXT
)

username_label.pack(anchor="w", padx=40)

username_entry = tk.Entry(
    card,
    font=("Courier New", 14),
    width=25
)

username_entry.pack(pady=(5, 20))

# PASSWORD
password_label = tk.Label(
    card,
    text="Password",
    font=("Courier New", 12),
    bg=CARD,
    fg=TEXT
)

password_label.pack(anchor="w", padx=40)

password_entry = tk.Entry(
    card,
    font=("Courier New", 14),
    width=25,
    show="*"
)

password_entry.pack(pady=(5, 20))

# LOGIN INFO
info_label = tk.Label(
    card,
    text=(
        "ADMIN → Full Access\n"
        "CASHIER → POS Only"
    ),
    font=("Courier New", 10),
    bg=CARD,
    fg="#7A9BB5",
    justify="center"
)

info_label.pack(pady=(0, 20))


# LOGIN FUNCTION
def login():

    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:

        messagebox.showwarning(
            "Missing Fields",
            "Please enter both a username and password."
        )

        return

    user = verify_login(username, password)

    if user:

        messagebox.showinfo(
            "Login Successful",
            f"Welcome, {user['username']}!\n"
            f"Role: {user['role'].upper()}"
        )

        root.destroy()

        if user["role"] == "admin":

            subprocess.Popen(
                [sys.executable, "admin_menu.py"]
            )

        elif user["role"] == "cashier":

            subprocess.Popen(
                [sys.executable, "pos_gui.py"]
            )

    else:

        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )

        password_entry.delete(0, tk.END)
        password_entry.focus()


# LOGIN BUTTON
login_btn = tk.Button(
    card,
    text="LOGIN",
    font=("Courier New", 12, "bold"),
    bg=ACCENT,
    fg=WHITE,
    relief="flat",
    width=20,
    height=2,
    command=login
)

login_btn.pack()

# BIND ENTER KEY TO LOGIN
root.bind("<Return>", lambda e: login())

# AUTO FOCUS
username_entry.focus()

# RUN
root.mainloop()