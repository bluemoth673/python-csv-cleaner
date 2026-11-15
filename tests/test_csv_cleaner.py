import csv
import tempfile
import unittest
from pathlib import Path

from csv_cleaner import clean_csv


class CsvCleanerTests(unittest.TestCase):
    def test_removes_duplicates_blank_rows_and_whitespace(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "input.csv"
            output = root / "output.csv"
            report = root / "report.txt"

            source.write_text(
                "name,email\n Alice , alice@example.com\n"
                "Alice,alice@example.com\n  ,  \nBob,bob@example.com\n",
                encoding="utf-8",
            )

            result = clean_csv(source, output, report)

            with output.open(newline="", encoding="utf-8-sig") as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["name"], "Alice")
            self.assertEqual(result["duplicates_removed"], 1)
            self.assertEqual(result["blank_rows_removed"], 1)
            self.assertEqual(result["missing_by_column"]["email"], 0)


if __name__ == "__main__":
    unittest.main()
