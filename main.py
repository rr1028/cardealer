"""Defines class responsible for Main Panel Window. """
import tkinter as tk
import customer_register_and_login
import shared

GEOMETRY_SIZE = '400x150'


class MainClass:
    """This class displays Main Panel Window for customer and contains
        functionality for buttons."""

    def __init__(self, main_app):
        """Inits MainClass."""
        self.main_app = main_app
        self.main_app.geometry(GEOMETRY_SIZE)
        self.main_app.title('Main Panel')
        self.main_app.configure(bg=shared.BG_COLOR)
        self.application = None

    def window_init(self):
        """Inits frames and buttons."""
        main_frame = tk.Frame(self.main_app)
        main_frame.configure(bg=shared.BG_COLOR)
        main_frame.grid()

        label_frame = tk.Frame(main_frame, bd=0, relief=tk.RIDGE, width=440, height=60,
                               padx=100, pady=10, bg=shared.BG_COLOR2)
        label_frame.pack(side=tk.TOP)

        button_frame = tk.Frame(main_frame, bd=0, width=400, height=100, padx=20, pady=30,
                                bg=shared.BG_COLOR)
        button_frame.pack(side=tk.BOTTOM)

        label = tk.Label(label_frame, text="Customer Login and Registration Panel",
                         bg=shared.BG_COLOR2)
        label.grid(row=0, column=0)
        register_button = tk.Button(button_frame, text='Register', width=12, padx=3,
                                    command=self.register, bg=shared.BG_COLOR)
        register_button.grid(column=9, row=5)

        login_button = tk.Button(button_frame, text='Login', width=12, command=self.login,
                                 bg=shared.BG_COLOR)
        login_button.grid(column=6, row=5)

    def login(self):
        """Displays Login Window."""
        self.main_app.destroy()
        self.main_app = tk.Tk()
        login_window = customer_register_and_login.CustomerLogin(self.main_app)
        login_window.init_window()
        self.main_app.mainloop()

    def register(self):
        """Displays Registration Window."""
        self.main_app.destroy()
        self.main_app = tk.Tk()
        register_window = customer_register_and_login.CustomerRegister(self.main_app)
        register_window.init_window()
        self.main_app.mainloop()


if __name__ == "__main__":
    laptop_app = tk.Tk()
    application = MainClass(laptop_app)
    application.window_init()
    laptop_app.mainloop()
