GST_RATE = 0.10
DISCOUNT_THRESHOLD = 100.00
DISCOUNT_RATE = 0.05

menu = []
inventory = []
seating = [
    ['Table 1', 4, True],
    ['Table 2', 2, False],
    ['Table 3', 5, True]
]


def add_menu_item(menu_list, name, price, available=True):
    if not name or price < 0:
        print("Invalid menu item or price.")
        return

    if any(item['name'].lower() == name.lower() for item in menu_list):
        print(f"Menu item already exists: {name}")
        return

    menu_list.append({
        'name': name,
        'price': price,
        'available': available
    })
    print(f"Added menu item: {name}")


def remove_menu_item(menu_list, name):
    for item in menu_list:
        if item['name'].lower() == name.lower():
            menu_list.remove(item)
            print(f"Removed menu item: {name}")
            return
    print(f"Menu item not found: {name}")


def update_menu_item(menu_list, name, price=None, available=None):
    for item in menu_list:
        if item['name'].lower() == name.lower():
            if price is not None:
                if price >= 0:
                    item['price'] = price
                else:
                    print("Price cannot be negative.")
                    return

            if available is not None:
                item['available'] = available

            print(f"Updated menu item: {name}")
            return

    print(f"Menu item not found: {name}")


def view_menu(menu_list):
    if not menu_list:
        print("No menu items available.")
        return

    print("\n--- Menu ---")
    for item in menu_list:
        status = "Available" if item['available'] else "Unavailable"
        print(f"{item['name']} - ${item['price']:.2f} - {status}")


def add_inventory_item(inventory_list, name, quantity):
    if not name or quantity < 0:
        print("Invalid inventory entry.")
        return

    for item in inventory_list:
        if item['name'].lower() == name.lower():
            item['stock'] += quantity
            print(f"Updated inventory: {name} stock is now {item['stock']}")
            return

    inventory_list.append({
        'name': name,
        'stock': quantity
    })
    print(f"Added inventory item: {name} - Stock: {quantity}")


def remove_inventory_item(inventory_list, name):
    for item in inventory_list:
        if item['name'].lower() == name.lower():
            inventory_list.remove(item)
            print(f"Removed inventory item: {name}")
            return
    print(f"Inventory item not found: {name}")


def view_inventory(inventory_list):
    if not inventory_list:
        print("No inventory items.")
        return

    print("\n--- Inventory ---")
    for item in inventory_list:
        print(f"{item['name']} - Stock: {item['stock']}")


def validate_integer(prompt, min_value=None):
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Input must be at least {min_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")


def validate_float(prompt, min_value=None):
    while True:
        try:
            value = float(input(prompt))
            if min_value is not None and value < min_value:
                print(f"Input must be at least {min_value}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def process_online_orders():
    num_orders = validate_integer("Enter the number of online orders: ", 1)

    for i in range(1, num_orders + 1):
        print(f"\nProcessing online order #{i}")
        order = []

        while True:
            name = input("Order item name (or 'done' to finish): ").strip()
            if name.lower() == 'done':
                break

            qty = validate_integer("Quantity: ", 1)
            order.append((name, qty))

        if order:
            calculate_bill(order)
        else:
            print("No items in this online order.")


def calculate_bill(order_list):
    subtotal = 0.0

    print("\n--- Bill ---")
    for name, qty in order_list:
        for item in menu:
            if item['name'].lower() == name.lower():
                if not item['available']:
                    print(f"{name} is currently unavailable.")
                    break

                line_total = item['price'] * qty
                print(f"{item['name']} x {qty} = ${line_total:.2f}")
                subtotal += line_total
                break
        else:
            print(f"Menu item not found: {name}")

    print(f"Subtotal: ${subtotal:.2f}")

    discount = 0.0
    if subtotal >= DISCOUNT_THRESHOLD:
        discount = subtotal * DISCOUNT_RATE
        print(f"Discount ({DISCOUNT_RATE * 100:.0f}%): -${discount:.2f}")

    gst = (subtotal - discount) * GST_RATE
    print(f"GST ({GST_RATE * 100:.0f}%): +${gst:.2f}")

    total = subtotal - discount + gst
    print(f"Total: ${total:.2f}\n")

    return total


def place_order_and_checkout():
    order = []

    while True:
        name = input("Order item name (enter 'done' when finished): ").strip()
        if name.lower() == 'done':
            break

        qty = validate_integer("Quantity: ", 1)
        order.append((name, qty))

    if order:
        calculate_bill(order)
    else:
        print("No items were ordered.")


def main():
    while True:
        print("\n=== Bondi Breeze Bistro System ===")
        print("1. View menu")
        print("2. Add menu item")
        print("3. Remove menu item")
        print("4. Update menu item")
        print("5. View inventory")
        print("6. Add inventory")
        print("7. Remove inventory")
        print("8. Place order and checkout")
        print("9. Process online orders")
        print("10. Exit")

        choice = validate_integer("Choose an option (1-10): ", 1)

        if choice == 1:
            view_menu(menu)

        elif choice == 2:
            name = input("Enter new menu item name: ").strip()
            price = validate_float("Enter price: ", 0)
            available = input("Is it available? (y/n): ").strip().lower() == 'y'
            add_menu_item(menu, name, price, available)

        elif choice == 3:
            name = input("Enter the name of the item to remove: ").strip()
            remove_menu_item(menu, name)

        elif choice == 4:
            name = input("Enter the name of the item to update: ").strip()

            price_input = input("New price (leave blank to skip): ").strip()
            if price_input:
                try:
                    price = float(price_input)
                    if price < 0:
                        print("Price cannot be negative.")
                        continue
                except ValueError:
                    print("Invalid price entered.")
                    continue
            else:
                price = None

            available_input = input("Is it available? (y/n/leave blank to skip): ").strip().lower()
            if available_input == 'y':
                available = True
            elif available_input == 'n':
                available = False
            else:
                available = None

            update_menu_item(menu, name, price, available)

        elif choice == 5:
            view_inventory(inventory)

        elif choice == 6:
            item_name = input("Item name: ").strip()
            quantity = validate_integer("Number of items to add: ", 0)
            add_inventory_item(inventory, item_name, quantity)

        elif choice == 7:
            item_name = input("Item name: ").strip()
            remove_inventory_item(inventory, item_name)

        elif choice == 8:
            place_order_and_checkout()

        elif choice == 9:
            process_online_orders()

        elif choice == 10:
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()