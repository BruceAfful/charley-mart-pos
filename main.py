from database import (
    create_tables,
    add_product,
    find_product_by_barcode,
    update_stock
)

create_tables()

# SAMPLE PRODUCTS
add_product("1001", "Coca Cola", 15.00, 20)
add_product("1002", "Indomie Noodles", 7.50, 50)
add_product("1003", "Milo 400g", 35.00, 15)

# CART
cart = []

print("\n========== CHARLEY MART POS ==========")

while True:

    barcode = input("\nScan barcode (or type 'done'): ")

    if barcode.lower() == "done":
        break

    product = find_product_by_barcode(barcode)

    if product:

        product_id = product[0]
        product_barcode = product[1]
        product_name = product[2]
        product_price = product[3]
        stock_quantity = product[4]

        print(f"Available Stock: {stock_quantity}")

        quantity = int(input("Enter quantity: "))

        if quantity > stock_quantity:
            print("Not enough stock available!")
            continue

        product_found_in_cart = False

        # CHECK IF PRODUCT ALREADY EXISTS IN CART
        for item in cart:

            if item["id"] == product_id:

                item["quantity"] += quantity
                item["subtotal"] = item["quantity"] * item["price"]

                product_found_in_cart = True

                print(f"{product_name} quantity updated in cart!")
                break

        # IF PRODUCT NOT IN CART, ADD NEW ITEM
        if not product_found_in_cart:

            subtotal = product_price * quantity

            cart.append({
                "id": product_id,
                "name": product_name,
                "price": product_price,
                "quantity": quantity,
                "subtotal": subtotal
            })

            print(f"{product_name} added to cart!")

    else:
        print("Product not found!")

# DISPLAY RECEIPT
print("\n========== RECEIPT ==========")

total = 0

for item in cart:

    print(
        f"{item['name']} | "
        f"GHS {item['price']} x "
        f"{item['quantity']} = "
        f"GHS {item['subtotal']}"
    )

    total += item['subtotal']

print("-" * 40)
print(f"TOTAL: GHS {round(total, 2)}")

# PAYMENT VALIDATION
while True:

    payment = float(input("\nAmount Paid: GHS "))

    if payment < total:
        print("Insufficient payment!")
    else:
        break

change = payment - total

print(f"CHANGE: GHS {round(change, 2)}")

# UPDATE STOCK
for item in cart:
    update_stock(item["id"], item["quantity"])

print("\nSale completed successfully!")
print("Inventory updated!")
print("Thank you for shopping at Charley Mart!")