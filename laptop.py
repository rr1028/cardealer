"""Defines class responsible for laptop Manager Window for Admin. """

import tkinter as tk
import tkinter.messagebox
import tkinter.ttk

import admin_transactions_gui
import laptop_db
import shared

GEOMETRY_SIZE = '750x450'
COLS = ('ID', 'BRAND', 'MODEL', 'COLOR', 'YEAR', 'AVAILABLE (0/1)', 'PRICE (PLN)')
COL_SIZE = [(25, 25), (100, 100), (100, 100), (90, 90), (50, 50), (100, 100), (80, 80)]


class laptopBase:
    """Base class for displaying laptop."""

    def __init__(self, laptop_app):
        """Inits laptop."""
        self.laptop_app = laptop_app
        self.data_b = laptop_db.laptopDatabase(shared.DATABASE)
        self.selected_item = None
        self.brand_entry = None
        self.model_entry = None
        self.color_entry = None
        self.year_entry = None
        self.price_entry = None

        self.table = None

        self.brand_text = tk.StringVar()
        self.model_text = tk.StringVar()
        self.color_text = tk.StringVar()
        self.year_text = tk.StringVar()
        self.price_text = tk.StringVar()

        self.text_fields = [self.brand_text, self.model_text, self.color_text, self.year_text,
                            self.price_text]
        self.db_fields = [self.year_text, self.price_text, self.brand_text, self.model_text,
                          self.color_text]

    def clear_text(self):
        """Clears all entries."""
        self.brand_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.color_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def exit(self):
        """Finishes program."""
        i_exit = tkinter.messagebox.askyesno("laptop Dealer Management Database System",
                                             "Do you want to exit?")
        if i_exit > 0:
            self.laptop_app.destroy()
            return


class laptop(laptopBase):
    """This class displays laptop Manager Window for Admin."""

    def __init__(self, laptop_app):
        """Inits laptop."""
        super().__init__(laptop_app)
        self.laptop_app.geometry(GEOMETRY_SIZE)
        self.laptop_app.title('laptop Manager')
        self.laptop_app.configure(bg=shared.BG_COLOR)
        self.data_b = laptop_db.laptopDatabase(shared.DATABASE)

    def populate_list(self):
        """Displays all laptop which are in database."""
        for i in self.table.get_children():
            self.table.delete(i)
        for row in self.data_b.fetch():
            self.table.insert('', tk.END, values=row)

    def add_laptop(self):
        """Adds a laptop to database."""
        for field in self.text_fields:
            if not field.get():
                tkinter.messagebox.showerror("Required Fields", "Please include all fields")
                return
        try:
            if not isinstance(int(self.year_text.get()), int):
                tkinter.messagebox.showerror("Year can't be a text", "Please write an integer")
                return
        except ValueError:
            tkinter.messagebox.showerror("Year can't be a text", "Please write an integer")
            return

        try:
            if not isinstance(float(self.price_text.get()), float):
                tkinter.messagebox.showerror("Price can't be a text", "Please write a real number")
                return
        except ValueError:
            tkinter.messagebox.showerror("Price can't be a text", "Please write a real number")
            return

        self.data_b.insert(*[f.get().capitalize() for f in self.text_fields])

        # clear list
        for i in self.table.get_children():
            self.table.delete(i)

        self.populate_list()
        self.clear_text()

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
            self.price_entry.insert(tk.END, self.selected_item[COLS[6]])

    def remove_laptop(self):
        """Removes laptop from database and updates listbox."""
        if not self.table.selection():
            return

        self.data_b.remove(self.selected_item[COLS[0]])
        self.clear_text()
        self.populate_list()

    def search_laptop(self):
        """Displays laptop that met given criteria. """
        for i in self.table.get_children():
            self.table.delete(i)

        for row in self.data_b.search(*[f.get() for f in self.db_fields]):
            self.table.insert('', tk.END, values=row)

    def update_laptop(self):
        """Updates laptop's data."""
        for field in self.text_fields:
            if not field.get():
                tkinter.messagebox.showerror("Required Fields", "Please include all fields")
                return
        try:
            if not isinstance(int(self.year_text.get()), int):
                tkinter.messagebox.showerror("Year can't be a text", "Please write an integer")
                return
        except ValueError:
            tkinter.messagebox.showerror("Year can't be a text", "Please write an integer")
            return

        try:
            if not isinstance(float(self.price_text.get()), float):
                tkinter.messagebox.showerror("Price can't be a text", "Please write a real number")
                return
        except ValueError:
            tkinter.messagebox.showerror("Price can't be a text", "Please write a real number")
            return
        try:
            self.data_b.update(self.selected_item[COLS[0]],
                               *[f.get().capitalize() for f in self.text_fields])
            self.populate_list()
        except TypeError:
            pass

    def all_transactions(self):
        """Turns to Transactions Panel."""

        self.laptop_app.destroy()
        self.laptop_app = tk.Tk()
        all_transactions_window = admin_transactions_gui.TransactionDisplayer(self.laptop_app)
        all_transactions_window.init_window()
        all_transactions_window.transactions()
        self.laptop_app.mainloop()

    def init_window(self):
        """Initializes window and buttons."""
        # Creating window

        # frames
        main_frame = tk.Frame(self.laptop_app)
        main_frame.configure(bg=shared.BG_COLOR)
        main_frame.grid()

        data_frame = tk.Frame(main_frame, bd=0, width=700, height=100, padx=100, relief=tk.RIDGE,
                              bg=shared.BG_COLOR)
        data_frame.pack(side=tk.TOP)
        button_frame = tk.Frame(main_frame, width=735, height=40, bd=1, relief=tk.RIDGE,
                                bg=shared.BG_COLOR)
        button_frame.pack(side=tk.TOP)

        table_frame = tk.Frame(main_frame, bd=0, width=735, height=310, padx=80, pady=10,
                               relief=tk.RIDGE, bg=shared.BG_COLOR)
        table_frame.pack(side=tk.TOP)

        # entries

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

        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_y.configure(command=self.table.yview())
        scroll_y.grid(row=0, column=3, sticky='ns')

        self.table.configure(yscrollcommand=scroll_y.set)
        self.table.bind('<ButtonRelease-1>', self.select_item)

        # buttons

        add_button = tk.Button(button_frame, text='Add laptop', width=12, command=self.add_laptop,
                               bg=shared.BG_COLOR)
        add_button.grid(column=0, row=0, sticky=tk.W)

        update_button = tk.Button(button_frame, text='Update', width=12, command=self.update_laptop,
                                  bg=shared.BG_COLOR)
        update_button.grid(column=1, row=0, sticky=tk.W)

        remove_button = tk.Button(button_frame, text='Remove', width=12, command=self.remove_laptop,
                                  bg=shared.BG_COLOR)
        remove_button.grid(column=2, row=0, sticky=tk.W)

        clear_button = tk.Button(button_frame, text='Clear', width=12, command=self.clear_text,
                                 bg=shared.BG_COLOR)
        clear_button.grid(column=3, row=0, sticky=tk.W)

        display_button = tk.Button(button_frame, text='Display', width=12,
                                   command=self.populate_list,
                                   bg=shared.BG_COLOR)
        display_button.grid(column=4, row=0, sticky=tk.W)

        search_button = tk.Button(button_frame, text='Search', width=12, command=self.search_laptop,
                                  bg=shared.BG_COLOR)
        search_button.grid(column=5, row=0, sticky=tk.W)

        trans_button = tk.Button(button_frame, text='All Transactions', width=12,
                                 command=self.all_transactions,
                                 bg=shared.BG_COLOR)
        trans_button.grid(column=6, row=0, sticky=tk.W)

        exit_button = tk.Button(button_frame, text='Exit', width=12, command=self.exit,
                                bg=shared.BG_BUTTON)
        exit_button.grid(column=7, row=0, sticky=tk.W)
