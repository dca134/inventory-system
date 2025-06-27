import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class InventoryApp:
    def __init__(self, root, inventory):
        self.root = root
        self.inventory = inventory
        self.root.title("Inventory System")
        self.root.geometry("700x500")

        # Make the window and table area resizable
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Input fields
        tk.Label(self.root, text="Product Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_name = tk.Entry(self.root)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self.root, text="Quantity:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_quantity = tk.Entry(self.root)
        self.entry_quantity.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self.root, text="Price (€):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_price = tk.Entry(self.root)
        self.entry_price.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Button to add a product
        btn_add = tk.Button(self.root, text="Add Product", command=self.add_item)
        btn_add.grid(row=3, column=0, columnspan=2, pady=10)

        # Table frame with vertical scrollbar
        frame = tk.Frame(self.root)
        frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            frame,
            columns=("id", "name", "quantity", "price"),
            show="headings",
            yscrollcommand=scrollbar.set
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Product Name")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("price", text="Price (€)")

        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)

        # Button to delete selected product
        btn_delete = tk.Button(self.root, text="Delete Selected Product", command=self.delete_selected_item)
        btn_delete.grid(row=5, column=0, columnspan=2, pady=10)

        # Load product data into the table on startup
        self.refresh_table()

    def add_item(self):
        name = self.entry_name.get().strip()
        quantity_str = self.entry_quantity.get().strip()
        price_str = self.entry_price.get().strip()

        if not name or not quantity_str or not price_str:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            quantity = int(quantity_str)
            price = float(price_str)
            if quantity < 0 or price < 0:
                messagebox.showerror("Error", "Quantity and price must be non-negative.")
                return
        except ValueError:
            messagebox.showerror("Error", "Quantity must be an integer and price must be a number.")
            return

        try:
            self.inventory.add_item(name, quantity, price)
            self.refresh_table()
            self.clear_fields()
            messagebox.showinfo("Success", "Product added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {e}")

    def delete_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete.")
            return

        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected product?")
        if not confirm:
            return

        item_id = self.tree.item(selected[0])["values"][0]
        try:
            self.inventory.delete_item(item_id)
            self.refresh_table()
            messagebox.showinfo("Success", "Product deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete product: {e}")

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.inventory.get_all_items():
            self.tree.insert("", "end", values=item)

    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)

# Optional direct launch
if __name__ == "__main__":
    root = tk.Tk()
    db = Database("inventory.db")
    app = InventoryApp(root, db)
    root.mainloop()

