#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, CENTER, W, NO, YES
from backend import insert, read, delete, update


def main():
    window = Application()
    window.mainloop()


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        
        self.title("Film Database")
        self.geometry("900x500")
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(8, weight=1)

        self.window_label = tk.Label(self, text="Film Database", font=('Arial 12 bold'))
        self.window_label.grid(row=0, column=0, columnspan=4, pady=15, padx=15)

        # Entry fields and labels
        self.title_label = tk.Label(self, text="Title:")
        self.title_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.title_entry = tk.Entry(self)
        self.title_entry.grid(row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5)

        self.length_label = tk.Label(self, text="Length:")
        self.length_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.length_entry = tk.Entry(self)
        self.length_entry.grid(row=2, column=1, columnspan=3, sticky="ew", padx=5, pady=5)

        self.year_label = tk.Label(self, text="Year:")
        self.year_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)

        self.year_entry = tk.Entry(self)
        self.year_entry.grid(row=3, column=1, columnspan=3, sticky="ew", padx=5, pady=5)

        self.frame = Form(self)
        self.frame.grid(row=4, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)


class Form(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        for i in range(4):
            self.columnconfigure(i, weight=1)

        self.rowconfigure(0, weight=1)
        self.parent = parent

        self.insert = insert
        self.read = read
        self.delete = delete
        self.update = update

        # Buttons
        self.insert_button = tk.Button(self, text="Insert", width=20, bg="#0099ff", command=self.insert_film)
        self.insert_button.grid(row=5, column=0, sticky="e", padx=5, pady=5)

        self.view_button = tk.Button(self, text="View", width=20, bg="#ffff00", command=self.view_all)
        self.view_button.grid(row=5, column=1, sticky="e", padx=5, pady=5)

        self.delete_button = tk.Button(self, text="Delete", width=20, bg="#e62e00", command=self.delete_film)
        self.delete_button.grid(row=5, column=2, sticky="e", padx=5, pady=5)

        self.update_button = tk.Button(self, text="Update", width=20, bg="#00ff00", command=self.update_film)
        self.update_button.grid(row=5, column=3, sticky="e", padx=5, pady=5) 

        self.clear_button = tk.Button(self, text="Clear", width=20, bg="#ffa500", command=self.clear_fields)
        self.clear_button.grid(row=5, column=4, sticky="e", padx=5, pady=5) 

        self.tree_frame = tk.Frame(self)
        self.tree_frame.grid(row=8, column=0, columnspan=5, sticky="nsew", padx=5, pady=5)
        self.tree_frame.columnconfigure(0, weight=1)
        self.tree_frame.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(self.tree_frame)
        self.tree['columns'] = ('id', 'title', 'length', 'year')

        self.tree.column('#0', width=0, stretch=NO)
        self.tree.column('id', anchor=CENTER, width=10)
        self.tree.column('title', anchor=W, width=300, minwidth=200, stretch=YES)
        self.tree.column('length', anchor=CENTER, width=50)
        self.tree.column('year', anchor=CENTER, width=50)

        self.tree.heading('#0', text='', anchor=W)
        self.tree.heading('id', text='id')
        self.tree.heading('title', text='title')
        self.tree.heading('length', text='length')
        self.tree.heading('year', text='year')

        self.tree.bind("<<TreeviewSelect>>", self.select_film)
        self.tree.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        
    def insert_film(self):
        '''Insert record into database'''
        
        self.insert(self.parent.title_entry.get(), self.parent.length_entry.get(), self.parent.year_entry.get())
        self.parent.title_entry.delete(0, tk.END)
        self.parent.length_entry.delete(0, tk.END)
        self.parent.year_entry.delete(0, tk.END)
        self.view_all()

    def select_film(self, e):
        '''Select a film'''

        self.parent.title_entry.delete(0, tk.END)
        self.parent.length_entry.delete(0, tk.END)
        self.parent.year_entry.delete(0, tk.END)

        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            values = item['values']

            self.parent.title_entry.insert(0, values[1])
            self.parent.length_entry.insert(0, values[2])
            self.parent.year_entry.insert(0, values[3])

    def update_film(self):
        '''Update a record in database'''

        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            id = item['values'][0]
            self.update(id, self.parent.title_entry.get(), self.parent.length_entry.get(), self.parent.year_entry.get())
        self.view_all()

    def delete_film(self):
        '''Delete films from database'''

        for i in self.tree.selection():
            t = self.tree.item(i)
            id = t['values'][0]
            self.delete(id)
        self.view_all()

    def clear_fields(self):
        '''Clear fields'''

        self.parent.title_entry.delete(0, tk.END)
        self.parent.length_entry.delete(0, tk.END)
        self.parent.year_entry.delete(0, tk.END)

    def view_all(self):
        '''View all records'''

        self.tree.delete(*self.tree.get_children())
        rows = self.read()
        for idx, record in enumerate(rows):
            self.tree.insert(parent='', index='end', text="", values=(record[0], record[1], record[2], record[3]))


if __name__ == "__main__":
    main()
