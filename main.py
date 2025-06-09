from models import Item, Inventory
from database import Database
from tabulate import tabulate

def main():
    db = Database()
    inventory = Inventory()

    while True:
        print("\n1. Добавить товар")
        print("2. Просмотреть инвентарь")
        print("3. Удалить товар")
        print("4. Редактирование товара")
        print("5. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            item = Item(
                id=int(input("ID товара: ")),
                name=input("Название: "),
                quantity=int(input("Количество: ")),
                price=float(input("Цена: €"))
            )
            db.add_item(item) # type: ignore
            print("Товар добавлен!")

        elif choice == "2":
            print("\nТекущий инвентарь:")
            # Здесь будет вывод из БД (допишем позже)
            items = db.get_all_items()

            if not items:
                print("Инвентарь пуст!")
            else:
                # Красивый вывод в таблице
                headers = ["ID", "Название", "Количество", "Цена", "Общая стоимость"]
                table = []

                for item in items:
                    item_id, name, quantity, price = item
                    total = quantity * price
                    table.append([item_id, name, quantity, f"{price:.2f} ₸", f"{total:.2f} ₸"])

                print(tabulate(table, headers=headers, tablefmt="grid"))

        elif choice == "3":
            print("\nУдаление товара")
            try:
                item_id = int(input("Введите ID товара для удаления: "))
        
                # Сначала проверяем существование товара
                if not db.item_exists(item_id):
                    print(f"Ошибка: товар с ID {item_id} не найден!")
                    continue
            
                # Запрашиваем подтверждение
                confirm = input(f"Вы уверены, что хотите удалить товар {item_id}? (y/n): ").lower()
                if confirm == 'y':
                    if db.delete_item(item_id):
                        print(f"Товар с ID {item_id} успешно удалён!")
                    else:
                        print("Ошибка при удалении!")
            except ValueError:
                print("Ошибка: ID должен быть числом!")

        elif choice == "4":
            print("\nРедактирование товара")
            try:
                item_id = int(input("ID товара для редактирования: "))  # Редактирование
            
            # Проверяем существование товара
                if not db.item_exists(item_id):
                    print("Ошибка: товар с таким ID не найден!")
                    continue

                print("Оставьте поле пустым, если не нужно изменять")
                new_name = input("Новое название: ").strip() or None
                new_quantity_input = input("Новое количество: ").strip()
                new_quantity = int(new_quantity_input) if new_quantity_input else None
                new_price_input = input("Новая цена: ").strip()
                new_price = float(new_price_input) if new_price_input else None

                if db.update_item(item_id, new_name, new_quantity, new_price): # type: ignore
                    print("Товар успешно обновлён!")
                else:
                    print("Данные не были изменены (возможно, вы не ввели новые значения)")
            except ValueError:
                print("Ошибка: введите корректные числовые значения!")

        elif choice == "5":
            break

if __name__ == "__main__":
    main()