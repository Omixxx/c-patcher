import csv


def compute_diffs(tsv_path: str, field_a: str, field_b: str, diff_field: str):
    with open(tsv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)

    for row in rows:
        if row[field_a] == row[field_b]:
            row[diff_field] = False
        else:
            row[diff_field] = True

    with open(tsv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = reader.fieldnames or [
            field_a,
            field_b,
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
