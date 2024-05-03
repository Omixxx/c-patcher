from modules import utils
import sys
from decimal import Decimal
from modules.custom_types.TsvFileInput import TsvFileInput


def _print_rows(rows: list[TsvFileInput]):
    for row in rows:
        print(
            "[",
            row.readabilityScore,
            ",",
            Decimal(row.readabilityScore) + Decimal(row.manual_readability_score),
            "],",
        )


tsv_file: str = sys.argv[1]

rows: list[TsvFileInput] = utils.extract_rows(tsv_file)
# i = 0
# for row in rows:
#     if i > 100:
#         break
#     i += 1
#     if row.manual_readability_score == "":
#         continue
#     _rows.append(row)


def compute_increments_decrements(rows: list[TsvFileInput]) -> tuple[int, int]:
    increments = 0
    decrements = 0
    for row in rows:
        if row.manual_readability_score == "":
            continue
        if Decimal(row.manual_readability_score) > 0:
            increments += 1

        if Decimal(row.manual_readability_score) < 0:
            decrements += 1
    return increments, decrements


rows = rows[:100]
low_rows = [x for x in rows if x.label == "LOW"]
medium_rows = [x for x in rows if x.label == "MID"]
high_rows = [x for x in rows if x.label == "HIGH"]


low_increments, low_decrements = compute_increments_decrements(low_rows)
medium_increments, medium_decrements = compute_increments_decrements(medium_rows)
high_increments, high_decrements = compute_increments_decrements(high_rows)
print("Low increments", low_increments)
print("Low decrements", low_decrements)
print("Medium increments", medium_increments)
print("Medium decrements", medium_decrements)
print("High increments", high_increments)
print("High decrements", high_decrements)
