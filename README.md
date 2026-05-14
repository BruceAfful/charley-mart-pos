# POS System

A desktop Point of Sale and Inventory Management System built with Python and SQLite.

## Features
- Role-based login (Admin and Cashier)
- Barcode-based product scanning
- Cart management with live totals
- Receipt generation (saved as .txt files)
- Product management (add, update, delete)
- Sales analytics dashboard
- Sales history viewer
- Automatic low-stock alerts

## Default Credentials
| Role    | Username | Password  |
|---------|----------|-----------|
| Admin   | admin    | admin123  |
| Cashier | cashier  | cash123   |

> Change these passwords after first login via the database directly or by extending the admin panel.

## How to Run

```bash
python login.py
```

- **Admin** gets access to the full Admin Control Panel (POS, Product Manager, Dashboard, Sales History).
- **Cashier** is taken directly to the POS screen.

## File Overview

| File               | Purpose                              |
|--------------------|--------------------------------------|
| `login.py`         | Entry point — role-based login       |
| `database.py`      | All database operations (SQLite)     |
| `pos_gui.py`       | POS screen (cashier and admin)       |
| `admin_menu.py`    | Admin hub linking all modules        |
| `admin_panel.py`   | Product management (add/update/delete)|
| `dashboard.py`     | Sales analytics dashboard            |
| `sales_history.py` | Receipt file viewer                  |
| `receipt.py`       | Receipt generation logic             |
| `main.py`          | Terminal-based POS (dev/testing)     |

## Requirements
- Python 3.x
- tkinter (included with standard Python)
- sqlite3 (included with standard Python)

No third-party packages required.