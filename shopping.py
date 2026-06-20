import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import tkinter.font as tkfont
from PIL import Image, ImageTk
import secrets
import hashlib
from dotenv import load_dotenv

load_dotenv()

username = "admin"
password = "haslo123"

FILENAME = 'products.json'
BG_COLOR = '#ffffff'
SOL = b'\xad&}\x1e\xf3\x90\x89\xd3\x04\t\xebxo\xc1\x15_'

def get_idx():
    ids = [ tree.item(i)['values'][0] for i in tree.get_children() ]
    return max(ids, default=0) + 1

def add_product():
    new_product_form()

def add_new_product():
    if not add_product_entry.get():
        return

    tree.insert('', 'end', values=(get_idx(), add_product_entry.get()))
    save_to_json()
    add_product_entry.delete(0, tk.END)
    window_new_product.destroy()

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
        messagebox.showerror('Błąd usunięcia produktu', 'Nie zaznaczono rekordu do usunięcia')

def encode_text(text: str) -> str:
    sol = secrets.token_hex(16)
    encoded_text = hashlib.pbkdf2_hmac(hash_name='sha256', password=bytearray(text, encoding="utf-8"), salt=bytearray(sol, encoding="utf-8"), iterations=3)
    full_hash = sol + encoded_text.hex()

    return full_hash

def verify_credentials() -> bool:
    return (
        login_entry.get() == username and
        password_entry.get() == password
    )

def verify_user():
    
    if verify_credentials():
        login_window.destroy()
        product_form()
    else:
        messagebox.showerror('Błąd logowania', f'Błędny login lub hasło')

def product_form():
    global tree, entry_product, window
    
    window = tk.Tk()
    window.title('Lista zakupów')
    window.configure(background=BG_COLOR)

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
    product_add = tk.Button(window, text="Dodaj produkt", command=add_product)
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
    
def new_product_form():
    global window_new_product, add_product_entry
    
    window_new_product = tk.Toplevel(window)
    window_new_product.title('Nowy product')
    window_new_product.configure(background=BG_COLOR)

    SCREEN_WIDTH = window_new_product.winfo_screenwidth()
    SCREEN_HEIGHT = window_new_product.winfo_screenheight()

    WIDTH = 400
    HEIGHT = 500

    x = (SCREEN_WIDTH - WIDTH) // 2
    y = (SCREEN_HEIGHT - HEIGHT) // 2

    window_new_product.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')
    
    head_lbl = tk.Label(window_new_product, text='Nowy produkt', font=tkfont.Font(size=30, weight='bold'), bg=BG_COLOR)
    head_lbl.pack(pady=(30,10))
    
    add_product_lbl = tk.Label(window_new_product, text='Product name:', anchor='w', padx=75, bg=BG_COLOR)
    add_product_lbl.pack(fill='x')
    
    add_product_entry = tk.Entry(window_new_product, width=40)
    add_product_entry.pack(pady=5)
    
    add_product_btn = tk.Button(window_new_product, text='Dodaj', width=35, border=1, command=add_new_product)
    add_product_btn.pack(fill='x', ipady=5, padx=75, pady=20)
    
def login_form():
    
    global login_entry, password_entry, login_window
    
    login_window = tk.Tk()
    login_window.title('Logowanie')
    login_window.resizable(False, False)
    login_window.configure(background=BG_COLOR)
    
    SCREEN_WIDTH = login_window.winfo_screenwidth()
    SCREEN_HEIGHT = login_window.winfo_screenheight()

    WIDTH = 400
    HEIGHT = 500

    x = (SCREEN_WIDTH - WIDTH) // 2
    y = (SCREEN_HEIGHT - HEIGHT) // 2

    login_window.geometry(f'{WIDTH}x{HEIGHT}+{x}+{y}')

    head_lbl = tk.Label(login_window, text='Logowanie', font=tkfont.Font(size=30, weight='bold'), bg=BG_COLOR)
    head_lbl.pack(pady=(30,10))
    
    login_lbl = tk.Label(login_window, text='Login:', anchor='w', padx=75, bg=BG_COLOR)
    login_lbl.pack(fill='x')
    
    login_entry = tk.Entry(login_window, width=40)
    login_entry.pack(pady=5)
    
    password_lbl = tk.Label(login_window, text='Password:', anchor='w', padx=75, bg=BG_COLOR)
    password_lbl.pack(fill='x')
    
    password_entry = tk.Entry(login_window, width=40, show='*')
    password_entry.pack(pady=5)
    
    login_btn = tk.Button(login_window, text='Zaloguj', width=35, border=1, command=verify_user)
    login_btn.pack(fill='x', ipady=5, padx=75, pady=20)

    opened_image = Image.open('trolley.png')
    resized_img = opened_image.resize(size=(150, 150), resample=Image.Resampling.LANCZOS)
    
    photo = ImageTk.PhotoImage(resized_img)
    photo_lbl = tk.Label(login_window, image=photo)
    photo_lbl.pack(pady=(20, 10))
    photo_lbl.image = photo
    photo_lbl.configure(border=0)
    
    
    login_window.mainloop()

login_form()