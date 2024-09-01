"""Tests for module laptop_db.py"""
import unittest

import laptop_db


class laptopDBTest(unittest.TestCase):
    """Tests for some functions in laptopDatabase class."""

    def setUp(self) -> None:
        self.laptop_db = laptop_db.laptopDatabase(':memory:')
        self.laptop_db.insert("Audi", "A1", "Blue", 2003, 25000)

    def test_fetch_brand(self):
        row = self.laptop_db.fetch()
        self.assertEqual(row[0][1], "Audi")

    def test_fetch_model(self):
        row = self.laptop_db.fetch()
        self.assertEqual(row[0][2], "A1")

    def test_fetch_color(self):
        row = self.laptop_db.fetch()
        self.assertEqual(row[0][3], "Blue")

    def test_fetch_year(self):
        row = self.laptop_db.fetch()
        self.assertEqual(row[0][4], 2003)

    def test_fetch_price(self):
        row = self.laptop_db.fetch()
        self.assertEqual(row[0][6], 25000)

    def test_default_instock_value(self):
        row = self.laptop_db.isout(1)
        self.assertEqual(row[0], 1)

    def test_available(self):
        row = self.laptop_db.fetch_available()
        self.assertEqual(row[0][1], "Audi")

    def test_out_of_stock(self):
        self.laptop_db.outofstock(1)
        row = self.laptop_db.isout(1)
        self.assertEqual(row[0], 0)


if __name__ == '__main__':
    unittest.main()
