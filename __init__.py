import tkinter as tk
from tkinter import ttk, messagebox

class InventoryApp:
    def __init__(self, root, inventory):
        self.root = root
        self.inventory = inventory
        self.root.title("Inventory System")
        self.root.geometry("700x500")

        #allowing the table and window to stretch when resizing
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # innput fields
        tk.Label(self.root, text="Product Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_name = tk.Entry(self.root)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self.root, text="Quantity:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.entry_quantity = tk.Entry(self.root)
        self.entry_quantity.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        tk.Label(self.root, text="Price:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.entry_price = tk.Entry(self.root)
        self.entry_price.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # add button
        btn_add = tk.Button(self.root, text="Add Products", command=self.add_item)
        btn_add.grid(row=3, column=0, columnspan=2, pady=10)

        # scrollablee table
        frame = tk.Frame(self.root)
        frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            frame,
            columns=("ID", "Product Name", "Quantity", "Price"),
            show="headings",
            yscrollcommand=scrollbar.set
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("Product Name", text="Product Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.tree.yview)

        if hasattr(self, 'refresh_table'):
            self.refresh_table()
        else:
            print("⚠️ Attention: refresh_table() method not found")

        
         #product deletion button
        btn_delete = tk.Button(self.root, text="Delete the selected product", command=self.delete_selected_item)
        btn_delete.grid(row=5, column=0, columnspan=2, pady=10)

    def delete_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Select the item to delete.")
            return

        confirm = messagebox.askyesno("Confirmation", "Delete the seleected product?")
        if not confirm:
            return

        item_id = self.tree.item(selected[0])["values"][0]
        try:
            self.inventory.delete_item(item_id)
            self.refresh_table()
            messagebox.showinfo("Success", "The product has been deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't delete the product: {e}")

    def clear_fields(self):
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)

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
                messagebox.showerror("Error", "Quantity and price cannot be negative.")
                return
        except ValueError:
            messagebox.showerror("Error", "The quantity must be an integer, and the price must be a number.")
            return

        try:
            self.inventory.add_item(name, quantity, price)
            self.refresh_table()
            self.clear_fields()
            messagebox.showinfo("Success", "Product added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Couldn't add product: {e}")



    # method of updating the table
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.inventory.get_all_items():
            self.tree.insert("", "end", values=item)


