import sqlite3
from typing import Optional, Union

class Database:
    def __init__(self, db_path="inventory.db"):
        self.conn = sqlite3.connect(db_path)
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
        """Добавляет товар и возвращает его ID"""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)",
                (name, quantity, price)
            )
            return cursor.lastrowid 
    
    def get_all_items(self) -> list:
        """Возвращает список всех товаров"""
        with self.conn:
            return self.conn.execute(
                "SELECT id, name, quantity, price FROM items ORDER BY id"
            ).fetchall()
    
    def update_item(self, item_id: int, name: str, quantity: int, price: float) -> bool:
        """Обновляет данные товара"""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE items SET name=?, quantity=?, price=? WHERE id=?",
                (name, quantity, price, item_id)
            )
            return cursor.rowcount > 0
    
    def delete_item(self, item_id: int) -> bool:
        """Удаляет товар по ID"""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
            return cursor.rowcount > 0
        
    def get_next_id(self) -> int:
        cursor = self.conn.cursor()
        cursor.execute("SELECT MAX(id) FROM items")
        max_id = cursor.fetchone()[0]
        return max_id + 1 if max_id else 1
    
    def item_exists(self, item_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM items WHERE id = ?", (item_id,))
        return cursor.fetchone() is not None