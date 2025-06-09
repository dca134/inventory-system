import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
from database import Database

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.selected_item = None
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Инвентарная система v2.0")
        self.root.geometry("1000x700")

        style = ThemedStyle(self.root)
        style.set_theme("arc")

        self.create_tabs()
        self.load_data()

    def create_tabs(self):
        self.tab_control = ttk.Notebook(self.root)

        self.tab_view = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_view, text="Все товары")
        self.setup_view_tab()

        self.tab_edit = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_edit, text="Добавить/Изменить")
        self.setup_edit_tab()

        self.tab_control.pack(expand=1, fill="both")

    def setup_view_tab(self):
        container = ttk.Frame(self.tab_view)
        container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            container,
            columns=("ID", "Название", "Количество", "Цена"),
            show="headings",
            selectmode="browse"
        )

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        columns = {
            "ID": {"width": 50, "anchor": "w"},
            "Название": {"width": 200, "anchor": "w"},
            "Количество": {"width": 100, "anchor": "center"},
            "Цена": {"width": 100, "anchor": "e"}
        }

        for col, params in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, **params)

        self.setup_view_buttons()

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def setup_view_buttons(self):
        btn_frame = ttk.Frame(self.tab_view)
        btn_frame.pack(pady=10)

        buttons = [
            ("Обновить", self.load_data),
            ("Изменить", self.edit_selected),
            ("Удалить", self.delete_selected)
        ]

        for text, command in buttons:
            ttk.Button(btn_frame, text=text, command=command).pack(side="left", padx=5)

    def setup_edit_tab(self):
        fields = [
            ("Название:", "entry_name"),
            ("Количество:", "entry_quantity"),
            ("Цена:", "entry_price")
        ]

        for row, (label_text, attr_name) in enumerate(fields):
            ttk.Label(self.tab_edit, text=label_text).grid(row=row, column=0, padx=5, pady=5, sticky="e")
            entry = ttk.Entry(self.tab_edit)
            entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")
            setattr(self, attr_name, entry)

        # Добавляем скрытое поле для ID
        self.entry_id = ttk.Entry(self.tab_edit)
        self.entry_id.grid_forget()

        self.setup_edit_buttons()

    def setup_edit_buttons(self):
        btn_frame = ttk.Frame(self.tab_edit)
        btn_frame.grid(row=3, columnspan=2, pady=10)

        buttons = [
            ("Добавить", self.add_item),
            ("Обновить", self.update_item),
            ("Очистить", self.clear_form)
        ]

        for text, command in buttons:
            ttk.Button(btn_frame, text=text, command=command).pack(side="left", padx=5)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        items = self.db.get_all_items()
        for item in items:
            self.tree.insert("", "end", values=item)

    def add_item(self):
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()

        if not name or not quantity or not price:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        self.db.add_item(name, int(quantity), float(price))
        self.load_data()
        self.clear_form()

    def edit_selected(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите товар для редактирования.")
            return

        values = self.tree.item(selected, "values")
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, values[0])
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, values[1])
        self.entry_quantity.delete(0, tk.END)
        self.entry_quantity.insert(0, values[2])
        self.entry_price.delete(0, tk.END)
        self.entry_price.insert(0, values[3])
        self.tab_control.select(self.tab_edit)

    def update_item(self):
        item_id = self.entry_id.get()
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()

        if not item_id or not name or not quantity or not price:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        self.db.update_item(int(item_id), name, int(quantity), float(price))
        self.load_data()
        self.clear_form()
        self.tab_control.select(self.tab_view)

    def delete_selected(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Выбор", "Выберите товар для удаления.")
            return

        item_id = self.tree.item(selected, "values")[0]
        confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот товар?")
        if confirm:
            self.db.delete_item(int(item_id))
            self.load_data()

    def clear_form(self):
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)

    def __init__(self, root):
        self.root = root
        self.setup_styles()
        # ... остальной код ...
    
    def setup_styles(self):
        self.style = ThemedStyle(self.root)
        self.style.set_theme("arc")
        
        # Кастомизация кнопок
        self.style.configure('TButton', 
                           padding=0,
                           height=28,
                           font=('Helvetica', 11))
        
        # Для всех кнопок в приложении
        self.style.map('TButton',
                     foreground=[('active', 'black')],
                     background=[('active', '#e6e6e6')])