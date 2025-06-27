import sqlite3
from typing import Optional, Union

class Database:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self._create_tables()

    def _create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL
                )
            """)

    def add_item(self, name: str, quantity: int, price: float) -> int:
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)",
                (name, quantity, price)
            )
            last_id = cursor.lastrowid
            if last_id is None:
                raise RuntimeError("Couldn't get the id of the inserted product.")
            return last_id


    def get_all_items(self) -> list:
        #Returns a list of all products
        with self.conn:
            return self.conn.execute(
                "SELECT id, name, quantity, price FROM items ORDER BY id"
            ).fetchall()

    def delete_item(self, item_id: int):
        # deeletes an item by id
        with self.conn:
            self.conn.execute("DELETE FROM items WHERE id = ?", (item_id,))

    def update_item(self, item_id: int, name: str, quantity: int, price: float):
        # updates product iformation
        with self.conn:
            self.conn.execute(
                "UPDATE items SET name = ?, quantity = ?, price = ? WHERE id = ?",
                (name, quantity, price, item_id)
            )
