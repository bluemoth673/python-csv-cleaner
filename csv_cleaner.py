#!/usr/bin/env python3
"""Clean a CSV file without changing the original.

Features:
- Trims leading/trailing whitespace from cells.
- Collapses repeated spaces inside cells.
- Removes completely empty rows.
- Removes duplicate rows (after whitespace cleanup).
- Reports missing values and cleaning statistics.
"""

import argparse
import csv
from pathlib import Path


def clean_value(value):
    """Normalize whitespace in a single cell."""
    return " ".join((value or "").split())


def clean_csv(input_path, output_path, report_path):
    input_path = Path(input_path)
    output_path = Path(output_path)
    report_path = Path(report_path)

    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if input_path.resolve() == output_path.resolve():
        raise ValueError("Output must be a different file from the input.")

    with input_path.open("r", newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise ValueError("The CSV file must have a header row.")

        headers = reader.fieldnames
        cleaned_rows = []
        seen_rows = set()
        blank_rows_removed = 0
        duplicates_removed = 0

        for row in reader:
            cleaned = {key: clean_value(row.get(key, "")) for key in headers}

            if not any(cleaned.values()):
                blank_rows_removed += 1
                continue

            row_key = tuple(cleaned.get(key, "") for key in headers)
            if row_key in seen_rows:
                duplicates_removed += 1
                continue

            seen_rows.add(row_key)
            cleaned_rows.append(cleaned)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8-sig") as destination:
        writer = csv.DictWriter(destination, fieldnames=headers)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    missing_by_column = {}
    for header in headers:
        missing_by_column[header] = sum(
            1 for row in cleaned_rows if not row.get(header, "")
        )

    report_lines = [
        "CSV CLEANING REPORT",
        "=" * 40,
        f"Input file: {input_path.name}",
        f"Output file: {output_path.name}",
        f"Rows kept: {len(cleaned_rows)}",
        f"Completely empty rows removed: {blank_rows_removed}",
        f"Duplicate rows removed: {duplicates_removed}",
        "",
        "Missing values by column (after cleaning):",
    ]
    report_lines.extend(
        f"- {column}: {count}" for column, count in missing_by_column.items()
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    return {
        "rows_kept": len(cleaned_rows),
        "blank_rows_removed": blank_rows_removed,
        "duplicates_removed": duplicates_removed,
        "missing_by_column": missing_by_column,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Clean whitespace, blank rows, and duplicate rows in a CSV."
    )
    parser.add_argument("input", help="Path to the original CSV file")
    parser.add_argument(
        "--output", default="cleaned.csv", help="Output CSV path (default: cleaned.csv)"
    )
    parser.add_argument(
        "--report", default="cleaning_report.txt",
        help="Text report path (default: cleaning_report.txt)"
    )
    args = parser.parse_args()

    try:
        result = clean_csv(args.input, args.output, args.report)
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))

    print("CSV cleaning complete.")
    print(f"Rows kept: {result['rows_kept']}")
    print(f"Blank rows removed: {result['blank_rows_removed']}")
    print(f"Duplicate rows removed: {result['duplicates_removed']}")
    print(f"Cleaned CSV: {args.output}")
    print(f"Report: {args.report}")


if __name__ == "__main__":
    main()
