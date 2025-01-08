#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, CENTER, W, NO, YES
from backend import insert, read, delete, update


def insert_data():
    '''Insert record into database'''
    
    insert(title_entry.get(), length_entry.get(), year_entry.get())
    title_entry.delete(0, tk.END)
    length_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    view_all()


def select_film(e):
    '''Select a film'''

    title_entry.delete(0, tk.END)
    length_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)

    selected = tree.selection()
    if selected:
        item = tree.item(selected)
        values = item['values']

        title_entry.insert(0, values[1])
        length_entry.insert(0, values[2])
        year_entry.insert(0, values[3])


def update_film():
    '''Update a record in database'''

    selected = tree.selection()
    if selected:
        item = tree.item(selected)
        id = item['values'][0]
        update(id, title_entry.get(), length_entry.get(), year_entry.get())


def delete_film():
    '''Delete films from database'''

    for i in tree.selection():
        t = tree.item(i)
        id = t['values'][0]
        delete(id)
    view_all()


def view_all():
    '''View all records'''

    tree.delete(*tree.get_children())
    rows = read()
    for idx, record in enumerate(rows):
        tree.insert(parent='', index='end', text="", values=(record[0], record[1], record[2], record[3]))
        

window = tk.Tk()
window.title("Film Database")
window.geometry("900x500")
window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=1)
window.rowconfigure(8, weight=1)

window_label = tk.Label(window, text="Film Database", font=('Arial 12 bold'))
window_label.grid(row=0, column=0, pady=15, padx=15) 

title_label = tk.Label(window, text="Title:")
title_label.grid(row=1, column=0, sticky="w", padx=5, pady=5) 
title_entry = tk.Entry(window)
title_entry.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5) 

length_label = tk.Label(window, text="Length:")
length_label.grid(row=2, column=0, sticky="w", padx=5, pady=5) 
length_entry = tk.Entry(window)
length_entry.grid(row=2, column=1, columnspan=3, sticky="ew", padx=5, pady=5) 

year_label = tk.Label(window, text="Year:")
year_label.grid(row=3, column=0, sticky="w", padx=5, pady=5) 
year_entry = tk.Entry(window)
year_entry.grid(row=3, column=1, columnspan=3, sticky="ew", padx=5, pady=5) 

button_frame = tk.Frame(window)
button_frame.grid(row=4, column=0, columnspan=4, sticky="w", padx=5, pady=5)

insert_button = tk.Button(button_frame, text="Insert", width=10, bg="#0099ff", command=insert_data)
insert_button.pack(side=tk.LEFT, padx=2)

view_button = tk.Button(button_frame, text="View", width=10, bg="#ffff00", command=view_all)
view_button.pack(side=tk.LEFT, padx=2)

delete_button = tk.Button(button_frame, text="Delete", width=10, bg="#e62e00", command=delete_film)
delete_button.pack(side=tk.LEFT, padx=2)

update_button = tk.Button(button_frame, text="Update", width=10, bg="#00ff00", command=update_film)
update_button.pack(side=tk.LEFT, padx=2)

tree = ttk.Treeview(window)
tree['columns'] = ('id', 'title', 'length', 'year')

tree.column('#0', width=0, stretch=NO)
tree.column('id', anchor=CENTER, width=10)
tree.column('title', anchor=W, width=300, minwidth=200, stretch=YES)
tree.column('length', anchor=CENTER, width=50)
tree.column('year', anchor=CENTER, width=50)

tree.heading('#0', text='', anchor=W)
tree.heading('id', text='id')
tree.heading('title', text='title')
tree.heading('length', text='length')
tree.heading('year', text='year')

tree.bind("<<TreeviewSelect>>", select_film)
tree.grid(row=8, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)


window.mainloop()

