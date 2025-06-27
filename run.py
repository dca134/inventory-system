from app import InventoryApp
from database import Database
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    db = Database("inventory.db") 
    app = InventoryApp(root, db) 
    root.mainloop()