import unittest
from helloworld import format_name

class TestFormatName(unittest.TestCase):

    def test_with_valid_name(self):
        """
        Testet die Funktion `format_name` mit einem gültigen Namen.
        """
        # Aufrufen der Funktion `format_name` mit dem Namen "Max Mustermann"
        name = format_name("Max Mustermann")

        # Überprüfen der Ausgabe
        self.assertEqual(name, "MAX MUSTERMANN")

    def test_with_empty_name(self):
        """
        Testet die Funktion `format_name` mit einem leeren Namen.
        """
        # Aufrufen der Funktion `format_name` mit einem leeren Namen
        name = format_name("")

        # Überprüfen der Ausgabe
        self.assertEqual(name, "")

if __name__ == "__main__":
    unittest.main()