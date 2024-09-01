"""Defines class responsible for transactions' table in database."""
import sqlite3

import laptop_db
import customers_db


class TransactionsDatabase(laptop_db.laptopDatabase, customers_db.CustomersDatabase):
    """This class operates on a table 'transactions' in database."""

    def __init__(self, d_base):
        """Inits TransactionsDatabase."""
        self.conn = sqlite3.connect(d_base)
        self.c_cursor = self.conn.cursor()
        self.c_cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                customer_id INTEGER NOT NULL,
                laptop_id INTEGER NOT NULL,
                date DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (laptop_id) REFERENCES laptop(laptop_id)             
                )""")
        self.conn.commit()

    def insert_transaction(self, customer_id, laptop_id):
        """Inserts transaction to a database."""
        self.c_cursor.execute("INSERT INTO transactions (customer_id, laptop_id)"
                              " VALUES (?,?)", (customer_id, laptop_id))
        self.conn.commit()

    def search_transactions(self, customer_id):
        """Returns transactions that meet the criteria."""
        self.c_cursor.execute('''SELECT transactions.transaction_id, laptop.brand,
         laptop.model,laptop.color,laptop.year,laptop.price, transactions.date 
        FROM transactions 
        INNER JOIN laptop 
        USING (laptop_id)
        WHERE transactions.customer_id=? ''', (customer_id,))
        return self.c_cursor.fetchall()

    def all_transactions(self):
        """Returns all transactions."""
        self.c_cursor.execute('''SELECT transactions.transaction_id,customers.name,
        customers.lastname, laptop.brand, laptop.model,laptop.color,laptop.year,laptop.price,
        transactions.date 
                FROM transactions 
                INNER JOIN laptop 
                USING (laptop_id)
                INNER JOIN customers
                USING (customer_id)
                ''')
        return self.c_cursor.fetchall()

    def remove_transaction(self, id_transaction):
        """Deletes transaction from a database."""
        self.c_cursor.execute("SELECT laptop_id FROM transactions WHERE transaction_id=?",
                              (id_transaction,))
        found_laptop_id = self.c_cursor.fetchone()
        self.c_cursor.execute("UPDATE laptop SET instock=1 WHERE laptop_id=?", (found_laptop_id[0],))
        self.conn.commit()
        self.c_cursor.execute("DELETE FROM transactions WHERE transaction_id=?", (id_transaction,))
        self.conn.commit()
