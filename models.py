class Item:
    """Класс товара"""
    def __init__(self, id: int, name: str, quantity: int, price: float):
        self.id = id
        self.name = name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"Item(id={self.id}, name='{self.name}', quantity={self.quantity}, price={self.price})"


class Inventory:
    """Класс инвентаря"""
    def __init__(self):
        self.items = []

    def add_item(self, item: Item):
        self.items.append(item)

    def find_item(self, item_id: int) -> Item | None:
        for item in self.items:
            if item.id == item_id:
                return item
        return None