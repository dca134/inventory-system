from models import Item, Inventory
from database import Database
from tabulate import tabulate


def main():
    db = Database("inventory.db")

    while True:
        print("\n1. Add a Product")
        print("2. View Inventory")
        print("3. Delete a Product")
        print("4. Product Editing")
        print("5. Exit")

        choice = input("Select an Action: ").strip()

        if choice == "1":
            print("\n Add a Product")
            name = input("Product Name: ").strip()
            quantity_str = input("Quantity: ").strip()
            price_str = input("Price: ").strip()

            try:
                quantity = int(quantity_str)
                price = float(price_str)
                if quantity < 0 or price < 0:
                    print("Error: Quantity and price cannot be negative.")
                    continue
            except ValueError:
                print("Error: The quantity must be an innteger, and the price must be a number..")
                continue

            try:
                db.add_item(name, quantity, price)
                print(f"Product '{name}' add: {quantity} quant, €{price}")
            except Exception as e:
                print(f"Error during adding: {e}")

        elif choice == "2":
            print("\nInventory")
            items = db.get_all_items()
            if not items:
                print("The inventory is empty.")
            else:
                headers = ["ID", "Product Name", "Quantity", "Price (€)"]
                print(tabulate(items, headers=headers, tablefmt="grid"))


        elif choice == "3":
            print("\n Deleting a Product")
            id_str = input("Enter the product ID: ").strip()
            if not id_str.isdigit():
                print("Error: The ID must be a number.")
                continue
            try:
                db.delete_item(int(id_str))
                print("he product has been deleted.")
            except Exception as e:
                print(f"Error during deleting: {e}")

        elif choice == "4":
            print("\nProduct Editing")
            id_str = input("Enter the product ID: ").strip()
            name = input("New Product Name: ").strip()
            quantity_str = input("New quantity: ").strip()
            price_str = input("New price: ").strip()

            if not id_str.isdigit():
                print("Error: The ID must be a number.")
                continue

            try:
                quantity = int(quantity_str)
                price = float(price_str)
                db.update_item(int(id_str), name, quantity, price)
                print("The product has been updated.")
            except Exception as e:
                print(f"Error during the update: {e}")

        elif choice == "5":
            print("Exit...")
            break

        else:
            print(" Wrong choice. Please enter a number from 1 to 5..")

if __name__ == "__main__":
    main()
