"""Defines a class responsible for Transactions' Window for Admin."""

import tkinter as tk
import tkinter.messagebox
import tkinter.ttk

import laptop
import laptop_db
import shared
import transactions_db

GEOMETRY_SIZE = '800x450'
COLS = ('ID', 'NAME', 'SURNAME', 'BRAND', 'MODEL', 'COLOR', 'YEAR', 'PRICE', 'DATE')
COL_SIZE = [(25, 25), (100, 100), (100, 100), (50, 50), (100, 100), (50, 50), (50, 50),
            (50, 50), (111, 111)]


class TransactionBase:
    """Base class for transactions."""

    def __init__(self, laptop_app):
        """Inits TransactionBase."""
        self.laptop_app = laptop_app
        self.selected_item = None
        self.table = None

    def select_item(self, event):
        """Stores an index of selected item."""
        if self.table.selection():
            self.selected_item = self.table.set(self.table.selection())

    def exit(self):
        """Finishes program."""
        exit_v = tkinter.messagebox.askyesno("laptop Dealer Management Database System",
                                             "Do you want to exit?")
        if exit_v > 0:
            self.laptop_app.destroy()
            return


class TransactionDisplayer(TransactionBase):
    """This class displays Transactions' Window for Admin."""

    def __init__(self, laptop_app):
        """Inits TransactionDisplayer."""
        TransactionBase.__init__(self, laptop_app)
        self.laptop_app.geometry(GEOMETRY_SIZE)
        self.laptop_app.title('Transaction Editor')
        self.laptop_app.configure(bg=shared.BG_COLOR)
        laptop_db.laptopDatabase(shared.DATABASE)
        self.trans_db = transactions_db.TransactionsDatabase(shared.DATABASE)

    def transactions(self):
        """Displays all transactions that are in database."""
        for i in self.table.get_children():
            self.table.delete(i)
        for row in self.trans_db.all_transactions():
            self.table.insert('', tk.END, values=row)

    def remove_transaction(self):
        """Removes selected transaction."""
        try:
            self.trans_db.remove_transaction(self.selected_item[COLS[0]])
            self.transactions()
        except TypeError:
            pass

    def back(self):
        """Turns back to laptop Manager Panel."""
        self.laptop_app.destroy()
        self.laptop_app = tk.Tk()
        laptop_window = laptop.laptop(self.laptop_app)
        laptop_window.init_window()
        laptop_window.populate_list()
        self.laptop_app.mainloop()

    def init_window(self):
        """Inits frames and buttons."""
        # Creating window
        main_frame = tk.Frame(self.laptop_app)
        main_frame.configure(bg=shared.BG_COLOR)
        main_frame.grid()
        # frames

        button_frame = tk.Frame(main_frame, width=735, height=40, bd=1, relief=tk.RIDGE,
                                bg=shared.BG_COLOR)
        button_frame.pack(side=tk.TOP)

        table_frame = tk.Frame(main_frame, bd=0, width=735,
                               height=310, padx=80, pady=10, relief=tk.RIDGE, bg=shared.BG_COLOR)
        table_frame.pack(side=tk.TOP)

        # creating table

        self.table = tkinter.ttk.Treeview(table_frame, columns=COLS, show='headings', height=10)
        self.table.grid()

        for x, y in zip(COLS, COL_SIZE):
            self.table.column(x, minwidth=y[0], width=y[1], anchor=tk.CENTER)
            self.table.heading(x, text=x)

        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_y.configure(command=self.table.yview())
        scroll_y.grid(row=0, column=3, sticky='ns')

        self.table.configure(yscrollcommand=scroll_y.set)
        self.table.bind('<ButtonRelease-1>', self.select_item)

        # buttons

        back_button = tk.Button(button_frame, text='< Back', width=15, command=self.back,
                                bg=shared.BG_COLOR)
        back_button.grid(column=1, row=0, sticky=tk.W)

        book_button = tk.Button(button_frame, text='Remove Transaction', width=15,
                                command=self.remove_transaction, bg=shared.BG_COLOR)
        book_button.grid(column=2, row=0, sticky=tk.W)

        exit_button = tk.Button(button_frame, text='Exit', width=15, command=self.exit,
                                bg=shared.BG_BUTTON)
        exit_button.grid(column=3, row=0, sticky=tk.W)
