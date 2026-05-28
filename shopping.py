import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import tkinter.font as tkfont

FILENAME = 'products.json'

def get_idx():
    ids = [ tree.item(i)['values'][0] for i in tree.get_children() ]
    return max(ids, default=0) + 1

def add_new_product():
    if not entry_product.get():
        return

    tree.insert('', 'end', values=(get_idx(), entry_product.get()))
    save_to_json()
    entry_product.delete(0, tk.END)

def save_to_json():
    data = []

    for child in tree.get_children():
        data.append(tree.item(child)["values"])

    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def read_from_json():

    if not os.path.exists(FILENAME):
        return
    
    with open(FILENAME, "r", encoding="utf-8") as f:
        data = json.load(f)

    for d in data:
        tree.insert('', 'end', values=(d[0], d[1]))

def remove_product():
    try:
        selected_id = tree.selection()
        tree.delete(selected_id)
        save_to_json()
    except:
        messagebox.showerror('Błąd', 'Nie zaznaczono rekordu do usunięcia')

def product_form():
    global tree, entry_product
    
    window = tk.Tk()
    window.title('Lista zakupów')

    SCREEN_WIDTH = window.winfo_screenwidth()
    SCREEN_HEIGHT = window.winfo_screenheight()

    WIDTH = 400
    HEIGHT = 500

    x = (SCREEN_WIDTH - WIDTH) // 2
    y = (SCREEN_HEIGHT - HEIGHT) // 2

    window.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')

    # wprowadzenie danych
    entry_product = tk.Entry(window, width=40)
    entry_product.pack(pady=10)

    # przyciski
    product_add = tk.Button(window, text="Dodaj produkt", command=add_new_product)
    product_add.pack(pady=5)

    product_del = tk.Button(window, text="Usuń produkt", command=remove_product)
    product_del.pack(pady=5)

    tree = ttk.Treeview(window, columns=('id', 'product'), show='headings', height=10)
    tree.heading('id', text='idx')
    tree.heading('product', text='produkt')

    tree.column('id', width=50, anchor='center')
    tree.column('product', width=300, anchor='center')
    tree.pack(pady=5)

    read_from_json()
    window.mainloop()
    
def login_form():
    
    login_window = tk.Tk()
    login_window.title('Logowanie')

    SCREEN_WIDTH = login_window.winfo_screenwidth()
    SCREEN_HEIGHT = login_window.winfo_screenheight()

    WIDTH = 400
    HEIGHT = 500

    x = (SCREEN_WIDTH - WIDTH) // 2
    y = (SCREEN_HEIGHT - HEIGHT) // 2

    login_window.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')

    head_lbl = tk.Label(login_window, text='Logowanie', font=tkfont.Font(size=30, weight='bold'), border=10)
    head_lbl.pack(pady=5)
    
    login_lbl = tk.Label(login_window, text='Login:', anchor='w')
    login_lbl.pack(pady=5)
    
    login_entry = tk.Entry(login_window, width=40)
    login_entry.pack(pady=5)
    
    password_entry = tk.Entry(login_window, width=40, show='*')
    password_entry.pack(pady=5)
    
    login_btn = tk.Button(login_window, text='Zaloguj')
    login_btn.pack(pady=5)
    
    login_window.mainloop()
    
login_form()