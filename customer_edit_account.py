"""Defines class responsible for editing Customer's data. """
import tkinter as tk
import tkinter.messagebox

import laptop_displayer
import customers_db
import main
import shared

GEOMETRY_SIZE = '600x200'


class CustomerEditAccount:
    """This class displays Customer Edit Panel and contains
        functionality for buttons."""

    def __init__(self, customer_app):
        """Inits CustomerEditAccount"""
        self.customer_app = customer_app
        self.customer_app.geometry(GEOMETRY_SIZE)
        self.customer_app.configure(bg=shared.BG_COLOR)
        self.customer_app.title('Customer Edit Panel')

        self.d_base = customers_db.CustomersDatabase(shared.DATABASE)
        self.customer_data = self.d_base.user_data(shared.LOGGED_ID)
        self.name_text = tk.StringVar(value=self.customer_data[1])
        self.lastname_text = tk.StringVar(value=self.customer_data[2])
        self.email_text = tk.StringVar(value=self.customer_data[3])
        self.access_key_text = tk.StringVar(value=self.customer_data[4])
        self.phone_text = tk.StringVar(value=self.customer_data[6])
        self.text_fields = [self.name_text, self.lastname_text, self.email_text,
                            self.access_key_text, self.phone_text]

    def update_customer(self):
        """Updates customer's data."""
        for field in self.text_fields:
            if not field.get():
                tkinter.messagebox.showerror("Required Fields", "Please include all fields")
                return

            try:
                if not isinstance(int(self.access_key_text.get()), int):
                    tkinter.messagebox.showerror("Access Key can't be a text",
                                                 "Please write a numeric key")
                    return
            except ValueError:
                tkinter.messagebox.showerror("Access Key can't be a text",
                                             "Please write a numeric key")
                return

            try:
                if not isinstance(int(self.phone_text.get()), int):
                    tkinter.messagebox.showerror("Number can't include characters",
                                                 "Please write your number using.. numbers :)")
                    return
            except ValueError:
                tkinter.messagebox.showerror("Number can't include characters",
                                             "Please write your number using.. numbers :)")
                return
            if len(self.access_key_text.get()) < shared.ACCESS_KEY_LENGTH:
                tkinter.messagebox.showerror("Access key fail",
                                             "Access key must have at least 3 digits")
                return

        self.d_base.update(shared.LOGGED_ID, self.name_text.get().capitalize(),
                           self.lastname_text.get().capitalize(),
                           self.email_text.get(),
                           self.access_key_text.get(), self.phone_text.get())
        tkinter.messagebox.showinfo("Update Successful", "Success!")

        self.customer_app.destroy()
        self.customer_app = tk.Tk()
        laptop_display_window = laptop_displayer.laptopDisplayer(self.customer_app)
        laptop_display_window.init_window()
        laptop_display_window.populate_list()
        self.customer_app.mainloop()

    def back(self):
        """Turns to Available laptop List."""
        self.customer_app.destroy()
        self.customer_app = tk.Tk()
        laptop_display_window = laptop_displayer.laptopDisplayer(self.customer_app)
        laptop_display_window.init_window()
        laptop_display_window.populate_list()
        self.customer_app.mainloop()

    def delete_account(self):
        """Deletes customer's account and exits application."""
        important = tkinter.messagebox.askyesno("Registration Panel",
                                                "Do you want to delete your account? You "
                                                "can't undo this")
        if important > 0:
            self.d_base.remove(shared.LOGGED_ID)
            self.customer_app.destroy()
            return

    def back_menu(self):
        """Turns back to login/registration panel."""
        self.customer_app.destroy()
        self.customer_app = tk.Tk()
        main_window = main.MainClass(self.customer_app)
        main_window.window_init()

        self.customer_app.mainloop()

    def init_window(self):
        """Inits frames and labels."""

        # Create window

        # frames
        main_frame = tk.Frame(self.customer_app)
        main_frame.configure(bg=shared.BG_COLOR)
        main_frame.grid()

        data_frame = tk.Frame(main_frame, bd=0, width=700, height=100, padx=50, relief=tk.RIDGE,
                              bg=shared.BG_COLOR)
        data_frame.pack(side=tk.TOP)
        button_frame = tk.Frame(main_frame, width=735, height=40, bd=1, relief=tk.RIDGE,
                                bg=shared.BG_COLOR)
        button_frame.pack(side=tk.TOP)

        name_label = tk.Label(data_frame, text='Name', font=shared.FONT_SIZE, pady=20,
                              bg=shared.BG_COLOR)
        name_label.grid(row=0, column=0, sticky=tk.E)
        name_entry = tk.Entry(data_frame, textvariable=self.name_text, font=shared.FONT_SIZE,
                              bg=shared.LISTBOX_COLOR)
        name_entry.grid(row=0, column=1)

        lastname_label = tk.Label(data_frame, text='Lastname', font=shared.FONT_SIZE,
                                  bg=shared.BG_COLOR)
        lastname_label.grid(row=0, column=2, sticky=tk.E, padx=(30, 0))
        lastname_entry = tk.Entry(data_frame, textvariable=self.lastname_text,
                                  font=shared.FONT_SIZE, bg=shared.LISTBOX_COLOR)
        lastname_entry.grid(row=0, column=3)

        email_label = tk.Label(data_frame, text='Email', font=shared.FONT_SIZE, bg=shared.BG_COLOR)
        email_label.grid(row=1, column=0, sticky=tk.E)
        email_entry = tk.Entry(data_frame, textvariable=self.email_text, font=shared.FONT_SIZE,
                               bg=shared.LISTBOX_COLOR)
        email_entry.grid(row=1, column=1)

        access_key_label = tk.Label(data_frame, text='Access Key', font=shared.FONT_SIZE,
                                    bg=shared.BG_COLOR)
        access_key_label.grid(row=1, column=2, sticky=tk.E)
        access_key_entry = tk.Entry(data_frame, textvariable=self.access_key_text,
                                    font=shared.FONT_SIZE, bg=shared.LISTBOX_COLOR)
        access_key_entry.grid(row=1, column=3)

        phone_label = tk.Label(data_frame, text='Phone Number', font=shared.FONT_SIZE, pady=20,
                               bg=shared.BG_COLOR)
        phone_label.grid(row=2, column=0, sticky=tk.E)
        phone_entry = tk.Entry(data_frame, textvariable=self.phone_text, font=shared.FONT_SIZE,
                               bg=shared.LISTBOX_COLOR)
        phone_entry.grid(row=2, column=1)

        # buttons

        back_button = tk.Button(button_frame, text='<Back', width=12, command=self.back,
                                bg=shared.BG_COLOR)
        back_button.grid(column=0, row=0, sticky=tk.W)

        add_button = tk.Button(button_frame, text='Update Account', width=12,
                               command=self.update_customer,
                               bg=shared.BG_COLOR)
        add_button.grid(column=1, row=0, sticky=tk.W)

        delete_button = tk.Button(button_frame, text='Delete Account', width=12,
                                  command=self.delete_account,
                                  bg=shared.BG_COLOR)
        delete_button.grid(column=2, row=0, sticky=tk.W)

        exit_button = tk.Button(button_frame, text='Log out', width=12,
                                command=self.back_menu, bg=shared.BG_BUTTON)
        exit_button.grid(column=3, row=0, sticky=tk.W)
