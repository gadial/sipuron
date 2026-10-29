"""Convert a Google Forms response CSV to a year-specific Sipuron YAML file."""

import argparse
import csv
import re
from pathlib import Path

import yaml


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="Google Forms CSV export")
    parser.add_argument(
        "--year",
        type=int,
        help="Submission year (inferred from a 4-digit year in the filename when omitted)",
    )
    return parser.parse_args()


def get_year(csv_file, explicit_year):
    if explicit_year:
        return explicit_year
    match = re.search(r"(?:19|20)\d{2}", csv_file.stem)
    if match:
        return int(match.group())
    raise SystemExit(
        "Could not infer the year from the filename. Pass it explicitly, for example: --year 2026"
    )


def extract_keyword(value):
    """Turn a Forms value such as '1. סוף' into 'סוף'."""
    value = value.strip()
    if not value:
        return ""
    _, separator, keyword = value.partition(" ")
    return keyword.strip() if separator else value


def convert(csv_file):
    stories = []
    keywords = []
    authors = []
    with csv_file.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        for row_number, row in enumerate(reader, start=2):
            if len(row) < 4:
                raise SystemExit(f"Row {row_number} has {len(row)} columns; expected at least 4")
            timestamp, author, keyword_value, story = row[:4]
            keyword = extract_keyword(keyword_value)
            stories.append({
                "time": timestamp,
                "author": author,
                "keyword": keyword,
                "story": story,
                "length": len(story),
            })
            if author not in authors:
                authors.append(author)
            if keyword not in keywords:
                keywords.append(keyword)
    return {"stories": stories, "keywords": keywords, "authors": authors}


def main():
    args = parse_args()
    year = get_year(args.csv_file, args.year)
    output_file = Path("data") / f"year_{year}.yml"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    data = convert(args.csv_file)
    with output_file.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=False)
    print(f"Wrote {output_file} ({len(data['stories'])} stories)")


if __name__ == "__main__":
    main()
