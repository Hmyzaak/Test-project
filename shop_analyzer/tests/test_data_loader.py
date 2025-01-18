import unittest
import pandas as pd
from shop_analyzer.src.data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    def setUp(self):
        """Nastavení prostředí pro testování."""
        self.valid_file = "test_data/valid_data.csv"
        self.invalid_file = "test_data/missing_columns.csv"
        self.empty_file = "test_data/empty.csv"
        self.loader = DataLoader(self.valid_file)

    def test_load_data_valid_file(self):
        """Test načtení platného CSV souboru."""
        data = self.loader.load_data()
        self.assertIsInstance(data, pd.DataFrame)

    def test_load_data_file_not_found(self):
        """Test, že chyba FileNotFoundError je vyhozena pro neexistující soubor."""
        self.loader.file_path = "non_existent.csv"
        with self.assertRaises(FileNotFoundError):
            self.loader.load_data()

    def test_validate_data_missing_columns(self):
        """Test zachycení chybějících sloupců."""
        invalid_loader = DataLoader(self.invalid_file)
        data = invalid_loader.load_data()
        with self.assertRaises(ValueError) as e:
            invalid_loader.validate_data(data)
        self.assertIn("Chybějící sloupce", str(e.exception))

    def test_validate_data_correct_format(self):
        """Test validace platného souboru."""
        data = self.loader.load_data()
        validated_data = self.loader.validate_data(data)
        self.assertIsInstance(validated_data, pd.DataFrame)


if __name__ == "__main__":
    unittest.main()
