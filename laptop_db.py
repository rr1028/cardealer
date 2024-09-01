"""Defines class responsible for laptop' table in database."""
import sqlite3


class laptopDatabase:
    """This class operates on a table 'laptop' in database."""

    def __init__(self, db):
        """Inits laptopDatabase."""
        self.conn = sqlite3.connect(db)
        self.c_cursor = self.conn.cursor()
        self.c_cursor.execute("""CREATE TABLE IF NOT EXISTS laptop (
                        laptop_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        brand TEXT,
                        model TEXT,
                        color TEXT,
                        year INTEGER,
                        instock INTEGER NOT NULL DEFAULT 1,
                        price REAL 
                        )""")
        self.conn.commit()

    def fetch(self):
        """Displays all laptop in database."""
        self.c_cursor.execute("SELECT laptop_id, brand, model, color, year, instock, price FROM laptop")
        return self.c_cursor.fetchall()

    def fetch_available(self):
        """Displays all laptop that are not booked by anybody."""
        self.c_cursor.execute(
            "SELECT laptop_id, brand, model, color, year, instock, price FROM laptop WHERE instock=1")
        return self.c_cursor.fetchall()

    def insert(self, brand, model, color, year, price):
        """Inserts laptop to a database."""
        self.c_cursor.execute("INSERT INTO laptop (brand,model,color,year,price) VALUES (?,?,?,?,?)",
                              (brand, model, color, year, price))
        self.conn.commit()

    def remove(self, id_laptop):
        """Deletes laptop from a database."""
        self.c_cursor.execute("DELETE FROM laptop WHERE laptop_id=?", (id_laptop,))
        self.conn.commit()

    def update(self, id_laptop, brand, model, color, year, price):
        """Updates chosen laptop."""
        self.c_cursor.execute(
            "UPDATE laptop SET brand=?, model=?,color=?,year=?,price=? WHERE laptop_id=?",
            (brand, model, color, year, price, id_laptop))
        self.conn.commit()

    def outofstock(self, id_laptop):
        """Sets status of chosen laptop to 0."""
        self.c_cursor.execute("UPDATE laptop SET instock=0 WHERE laptop_id=?", (id_laptop,))
        self.conn.commit()

    def isout(self, id_laptop):
        """Returns the column 'instock' of chosen laptop."""
        self.c_cursor.execute("SELECT instock FROM laptop WHERE laptop_id=?", (id_laptop,))
        return self.c_cursor.fetchone()

    def search(self, year, price, brand='', model='', color=''):
        """Returns laptop that meet the criteria."""
        self.c_cursor.execute(
            "SELECT laptop_id, brand, model, color, year, instock, price FROM laptop WHERE brand=? OR"
            " model=? OR color=? OR year=? OR price=?",
            (brand.capitalize(), model.capitalize(), color.capitalize(), year, price))
        return self.c_cursor.fetchall()

    def search_available(self, year, price, brand='', model='', color=''):
        """Returns laptop that meet the criteria."""
        self.c_cursor.execute(
            "SELECT laptop_id, brand, model, color, year, instock, price FROM laptop WHERE (brand=? OR"
            " model=? OR color=? OR year=? OR price=?) AND (instock=1)",
            (brand.capitalize(), model.capitalize(), color.capitalize(), year, price))
        return self.c_cursor.fetchall()
