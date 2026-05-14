from datetime import datetime
import os


def generate_receipt(cart, total_amount, payment, change):

    # CREATE RECEIPTS FOLDER IF IT DOESN'T EXIST
    os.makedirs("receipts", exist_ok=True)

    # UNIQUE RECEIPT NUMBER BASED ON TIMESTAMP
    now = datetime.now()

    receipt_number = now.strftime("%Y%m%d_%H%M%S")

    filename = f"receipts/receipt_{receipt_number}.txt"

    # BUILD RECEIPT CONTENT
    receipt = ""

    receipt += "================================\n"
    receipt += "          POS SYSTEM\n"
    receipt += "================================\n\n"

    receipt += f"Receipt No : {receipt_number}\n"
    receipt += f"Date       : {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    receipt += "--------------------------------\n"

    for product_id in cart:

        item = cart[product_id]

        line = (
            f"{item['name']} "
            f"x{item['quantity']} "
            f"= GHS {item['subtotal']:.2f}\n"
        )

        receipt += line

    receipt += "--------------------------------\n\n"

    receipt += f"TOTAL  :  GHS {total_amount:.2f}\n"
    receipt += f"PAID   :  GHS {payment:.2f}\n"
    receipt += f"CHANGE :  GHS {change:.2f}\n\n"

    receipt += "================================\n"
    receipt += "  Thank you for your purchase!\n"
    receipt += "================================\n"

    # SAVE TO FILE
    with open(filename, "w") as file:
        file.write(receipt)

    return filename