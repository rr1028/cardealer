"""Defines class responsible for laptop Manager Window for customer. """
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk

import laptop
import laptop_db
import customer_edit_account
import customer_transaction_gui
import shared
import transactions_db

GEOMETRY_SIZE = '735x450'
COLS = ('ID', 'BRAND', 'MODEL', 'COLOR', 'YEAR', 'PRICE (PLN)')
COL_SIZE = [(25, 25), (100, 100), (100, 100), (90, 90), (50, 50), (80, 80)]


class laptopDisplayer(laptop.laptopBase):
    """This class displays Available laptop List Window for customer and contains
        functionality for buttons."""

    def __init__(self, laptop_app):
        """Inits laptopDisplayer."""
        super().__init__(laptop_app)
        self.laptop_app.geometry(GEOMETRY_SIZE)
        self.laptop_app.title('Available laptop List')
        self.laptop_app.configure(bg=shared.BG_COLOR)
        self.data_base = laptop_db.laptopDatabase(shared.DATABASE)
        self.trans_db = transactions_db.TransactionsDatabase(shared.DATABASE)

    def populate_list(self):
        """Displays all laptop which are in database."""
        for i in self.table.get_children():
            self.table.delete(i)
        for row in self.data_base.fetch_available():
            self.table.insert('', tk.END, values=[row[0], row[1], row[2], row[3], row[4], row[6]])

    def select_item(self, event):
        """Fills fields with selected laptop's data."""

        if self.table.selection():
            self.selected_item = self.table.set(self.table.selection())

            self.brand_entry.delete(0, tk.END)
            self.brand_entry.insert(tk.END, self.selected_item[COLS[1]])

            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(tk.END, self.selected_item[COLS[2]])

            self.color_entry.delete(0, tk.END)
            self.color_entry.insert(tk.END, self.selected_item[COLS[3]])

            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(tk.END, self.selected_item[COLS[4]])

            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(tk.END, self.selected_item[COLS[5]])

    def search_laptop(self):
        """Displays laptop that met given criteria. """
        for i in self.table.get_children():
            self.table.delete(i)

        for row in self.data_base.search_available(*[f.get() for f in self.db_fields]):
            self.table.insert('', tk.END, values=[row[0], row[1], row[2], row[3], row[4], row[6]])

    def my_transactions(self):
        """Turns to Transactions Panel."""

        self.laptop_app.destroy()
        self.laptop_app = tk.Tk()
        my_transactions_window = customer_transaction_gui.TransactionCustomerDisplayer(self.laptop_app)
        my_transactions_window.init_window()
        my_transactions_window.my_transactions()
        self.laptop_app.mainloop()

    def book_laptop(self):
        """Books selected laptop"""
        try:
            is_laptop = self.data_base.isout(self.selected_item[COLS[0]])
            if is_laptop[0] == 0:
                pass
            else:
                self.data_base.outofstock(self.selected_item[COLS[0]])
                tkinter.messagebox.showinfo("Book Successful", "Book Successful")
                self.populate_list()
                self.trans_db.insert_transaction(shared.LOGGED_ID, self.selected_item[COLS[0]])
        except TypeError:
            pass

    def edit_account(self):
        """Turns to Customer Edit Account."""
        self.laptop_app.destroy()
        self.laptop_app = tk.Tk()
        edit_account_window = customer_edit_account.CustomerEditAccount(self.laptop_app)
        edit_account_window.init_window()
        self.laptop_app.mainloop()

        # frames

    def init_window(self):
        """Inits frames and labels."""

        main_frame = tk.Frame(self.laptop_app)
        main_frame.configure(bg=shared.BG_COLOR)
        main_frame.grid()

        data_frame = tk.Frame(main_frame, bd=0, width=700, height=100, padx=100, relief=tk.RIDGE,
                              bg=shared.BG_COLOR)
        data_frame.pack(side=tk.TOP)
        button_frame = tk.Frame(main_frame, width=700, height=40, bd=1, relief=tk.RIDGE,
                                bg=shared.BG_COLOR)
        button_frame.pack(side=tk.TOP)

        table_frame = tk.Frame(main_frame, bd=0, width=735, height=310, padx=80,
                               pady=10, relief=tk.RIDGE, bg=shared.BG_COLOR)
        table_frame.pack(side=tk.TOP)

        brand_label = tk.Label(data_frame, text='Brand Name', font=shared.FONT_SIZE, pady=20,
                               bg=shared.BG_COLOR)
        brand_label.grid(row=0, column=0, sticky=tk.E)
        self.brand_entry = tk.Entry(data_frame, textvariable=self.brand_text, font=shared.FONT_SIZE,
                                    bg=shared.LISTBOX_COLOR)
        self.brand_entry.grid(row=0, column=1)

        model_label = tk.Label(data_frame, text='Model Name', font=shared.FONT_SIZE,
                               bg=shared.BG_COLOR)
        model_label.grid(row=0, column=2, sticky=tk.E, padx=(30, 0))
        self.model_entry = tk.Entry(data_frame, textvariable=self.model_text, font=shared.FONT_SIZE,
                                    bg=shared.LISTBOX_COLOR)
        self.model_entry.grid(row=0, column=3)

        color_label = tk.Label(data_frame, text='laptop Color', font=shared.FONT_SIZE,
                               bg=shared.BG_COLOR)
        color_label.grid(row=1, column=0, sticky=tk.E)
        self.color_entry = tk.Entry(data_frame, textvariable=self.color_text, font=shared.FONT_SIZE,
                                    bg=shared.LISTBOX_COLOR)
        self.color_entry.grid(row=1, column=1)

        year_label = tk.Label(data_frame, text='laptop Year ', font=shared.FONT_SIZE,
                              bg=shared.BG_COLOR)
        year_label.grid(row=1, column=2, sticky=tk.E)
        self.year_entry = tk.Entry(data_frame, textvariable=self.year_text, font=shared.FONT_SIZE,
                                   bg=shared.LISTBOX_COLOR)
        self.year_entry.grid(row=1, column=3)

        price_label = tk.Label(data_frame, text='laptop Price', font=shared.FONT_SIZE, pady=20,
                               bg=shared.BG_COLOR)
        price_label.grid(row=2, column=0, sticky=tk.E)
        self.price_entry = tk.Entry(data_frame, textvariable=self.price_text, font=shared.FONT_SIZE,
                                    bg=shared.LISTBOX_COLOR)
        self.price_entry.grid(row=2, column=1)
        # creating table
        self.table = tkinter.ttk.Treeview(table_frame, columns=COLS, show='headings', height=10)
        self.table.grid()

        for x, y in zip(COLS, COL_SIZE):
            self.table.column(x, minwidth=y[0], width=y[1], anchor=tk.CENTER)
            self.table.heading(x, text=x)

        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_x.configure(command=self.table.xview())

        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_y.configure(command=self.table.yview())
        scroll_y.grid(row=0, column=3, sticky='ns')

        self.table.configure(xscrollcommand=scroll_x.set)
        self.table.configure(yscrollcommand=scroll_y.set)
        self.table.bind('<ButtonRelease-1>', self.select_item)

        # buttons

        clear_button = tk.Button(button_frame, text='Clear', width=12, command=self.clear_text,
                                 bg=shared.BG_COLOR)
        clear_button.grid(column=0, row=0, sticky=tk.W)

        display_button = tk.Button(button_frame, text='Display', width=12,
                                   command=self.populate_list, bg=shared.BG_COLOR)
        display_button.grid(column=1, row=0, sticky=tk.W)

        search_button = tk.Button(button_frame, text='Search', width=12, command=self.search_laptop,
                                  bg=shared.BG_COLOR)
        search_button.grid(column=2, row=0, sticky=tk.W)

        book_button = tk.Button(button_frame, text='Book A laptop', width=12, command=self.book_laptop,
                                bg=shared.BG_COLOR)
        book_button.grid(column=3, row=0, sticky=tk.W)

        menu_button = tk.Button(button_frame, text='My Transactions', width=12,
                                command=self.my_transactions, bg=shared.BG_COLOR)
        menu_button.grid(column=4, row=0, sticky=tk.W)

        edit_button = tk.Button(button_frame, text='Edit Account', width=12,
                                command=self.edit_account, bg=shared.BG_COLOR)
        edit_button.grid(column=5, row=0, sticky=tk.W)

        exit_button = tk.Button(button_frame, text='Exit', width=12, command=self.exit,
                                bg=shared.BG_BUTTON)
        exit_button.grid(column=6, row=0, sticky=tk.W)
