# Python CSV Cleaner

A beginner-friendly portfolio project that cleans CSV files using only Python's standard library.

## What it does

- Trims leading/trailing whitespace and collapses repeated spaces.
- Removes completely empty rows.
- Removes duplicate rows after whitespace cleanup.
- Counts missing values in each column.
- Creates a cleaned CSV and a plain-text report.
- Keeps the original input file unchanged.

## Requirements

- Python 3.9 or newer
- No paid tools and no third-party packages

## Run it

Open a terminal in this project folder.

```bash
python3 csv_cleaner.py sample_data/contacts_messy.csv --output cleaned.csv --report cleaning_report.txt
```

On Windows, use `python` instead of `python3` if needed.

You should see a completion message. Open `cleaned.csv` and `cleaning_report.txt` to inspect the results.

## Run the test

```bash
python3 -m unittest discover -s tests -v
```

## Example use cases

- Cleaning exported contact lists.
- Removing duplicate spreadsheet records saved as CSV.
- Preparing small datasets for analysis.

## Important limitations

- This tool removes only exact duplicate rows after whitespace normalization. It does not decide whether two different people are the same person.
- It does not guess missing values or alter dates, phone numbers, or email addresses.
- Always review the output before using it for important business records.

## Project structure

```text
python-csv-cleaner/
├── csv_cleaner.py
├── sample_data/
│   └── contacts_messy.csv
├── tests/
│   └── test_csv_cleaner.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Portfolio note

This is a demonstration project. When adapting it for a client, first confirm the CSV format, expected cleanup rules, sample input, output format, and how duplicate records should be identified.
# python-csv-cleaner
