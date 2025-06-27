# Inventory Management System

A simple graphical Python application for inveentory management.

## Features
- Graphical interface (Tkinter)
- Automatic product ID generation
- CRUD operations:
  - Adding a product
  - Deleting the selected product
  - View the entire inventory
- Data storage in an SQLite database (`inventory.db')
- The code is organized into modules (`app.py `, `database.py `, `models.py `)
- The ability to launch via the GUI (`run.py `)
- Supports export to CSV (via CLI)

## Project structure
inventory-system/
├── app.py              #Graphical interface
├── database.py         # Working with SQLite
├── models.py           #Item and Inventory classes (optional)
├── main.py             #CLI version (alternative to GUI)
├── run.py              #Launching the GUI application
├── requirements.txt    #Dependencies
├── README.md           #Documentation
├── inventory.db        #Database (automatically created)


## Installation
```bash
git clone https://github.com/dca134/inventory-system
cd inventory-system
pip install -r requirements.txt
python run.py 