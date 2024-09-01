"""Defines class responsible for customers' table in database."""
import sqlite3


class CustomersDatabase:
    """This class operates on a table 'customers' in database."""

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.c_cursor = self.conn.cursor()
        self.c_cursor.execute("""CREATE TABLE IF NOT EXISTS customers (
                        customer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        name TEXT,
                        lastname TEXT,
                        email TEXT,
                        access_key INTEGER NOT NULL,
                        permission INTEGER NOT NULL DEFAULT 1,
                        phone TEXT                            
                        )""")
        self.conn.commit()

    def fetch(self):
        """Returns all customers."""
        self.c_cursor.execute(
            "SELECT customer_id, name, lastname, email, access_key, permission, phone "
            "FROM customers")
        return self.c_cursor.fetchall()

    def insert(self, name, lastname, email, access_key, phone):
        """Inserts customer to a database."""
        self.c_cursor.execute("INSERT INTO customers (name,lastname,email,access_key,phone)"
                              " VALUES (?,?,?,?,?)",
                              (name, lastname, email, access_key, phone))
        self.conn.commit()

    def remove(self, id_customer):
        """Deletes customer from a database."""
        self.c_cursor.execute("DELETE FROM customers WHERE customer_id=?", (id_customer,))
        self.conn.commit()

    def update(self, id_customer, name, lastname, email, access_key, phone):
        """Updates chosen customer."""
        self.c_cursor.execute("UPDATE customers SET name=?, lastname=?,email=?,"
                              " access_key=?,phone=? WHERE customer_id=?",
                              (name, lastname, email, access_key, phone, id_customer))
        self.conn.commit()

    def search(self, name='', lastname='', email='', access_key='', phone=''):
        """Returns customers that meet the criteria."""
        self.c_cursor.execute(
            "SELECT customer_id, name, lastname, email, access_key, permission, phone"
            " FROM customers WHERE name=? OR lastname=? OR email=?"
            " OR access_key=? OR phone=? AND permission=1",
            (name.capitalize(), lastname.capitalize(), email, access_key, phone))
        return self.c_cursor.fetchall()

    def search_email(self, email=''):
        """Returns customers with given email."""
        self.c_cursor.execute(
            "SELECT customer_id, name, lastname, email, access_key, permission, phone"
            " FROM customers WHERE email=?", (email,))
        return self.c_cursor.fetchall()

    def search_user(self, email='', access_key=''):
        """Returns customers with given email and access key."""
        self.c_cursor.execute(
            "SELECT customer_id, name, lastname, email, access_key, permission, phone "
            "FROM customers WHERE email=? AND"
            " access_key=?", (email, access_key))
        return self.c_cursor.fetchall()

    def is_admin(self, email='', access_key=''):
        """Returns users that meet given criteria."""
        self.c_cursor.execute(
            "SELECT customer_id, name, lastname, email, access_key, permission, phone "
            "FROM customers WHERE email=? AND"
            " access_key=? AND permission=0", (email, access_key))
        return self.c_cursor.fetchall()

    def get_id(self, email='', access_key=''):
        """Returns id of logged customer."""
        self.c_cursor.execute("SELECT customer_id FROM customers WHERE"
                              " email=? AND access_key=?", (email, access_key))
        found_id = self.c_cursor.fetchone()
        return found_id[0]

    def user_data(self, id_customer):
        """Returns data of logged user."""
        self.c_cursor.execute(
            "SELECT customer_id, name, lastname, email, access_key, permission, phone "
            "FROM customers WHERE customer_id=?", (id_customer,))
        return self.c_cursor.fetchone()
