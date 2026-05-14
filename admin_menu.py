import tkinter as tk
import subprocess
import sys

# COLORS
BG    = "#0F1923"
CARD  = "#1E2D3D"
ACCENT = "#00C896"
TEXT  = "#E8F4F8"
WHITE = "#FFFFFF"

# WINDOW
root = tk.Tk()

root.title("Admin Control Panel")
root.geometry("600x500")
root.configure(bg=BG)

# TITLE
title = tk.Label(
    root,
    text="ADMIN CONTROL PANEL",
    font=("Courier New", 24, "bold"),
    bg=BG,
    fg=ACCENT
)

title.pack(pady=40)


# BUTTON FACTORY
def create_button(text, command):

    btn = tk.Button(
        root,
        text=text,
        font=("Courier New", 14, "bold"),
        bg=CARD,
        fg=WHITE,
        relief="flat",
        width=25,
        height=2,
        command=command
    )

    btn.pack(pady=10)

    return btn


# OPEN POS
create_button(
    "OPEN POS SYSTEM",
    lambda: subprocess.Popen(
        [sys.executable, "pos_gui.py"]
    )
)

# OPEN PRODUCT MANAGER
create_button(
    "PRODUCT MANAGEMENT",
    lambda: subprocess.Popen(
        [sys.executable, "admin_panel.py"]
    )
)

# OPEN DASHBOARD
create_button(
    "SALES DASHBOARD",
    lambda: subprocess.Popen(
        [sys.executable, "dashboard.py"]
    )
)

# OPEN SALES HISTORY
create_button(
    "SALES HISTORY",
    lambda: subprocess.Popen(
        [sys.executable, "sales_history.py"]
    )
)

# RUN
root.mainloop()