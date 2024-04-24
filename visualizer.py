from modules import utils
import sys
from decimal import Decimal
from modules.custom_types.TsvFileInput import TsvFileInput


def _print_rows(rows: list[TsvFileInput]):
    for row in rows:
        print(
            row.name,
            row.label,
            Decimal(row.predictions_readability_score) - Decimal(row.readabilityScore),
            row.manual_readability_score,
        )


tsv_file: str = sys.argv[1]

rows: list[TsvFileInput] = utils.extract_rows(tsv_file)
rows = [
    x
    for x in rows
    if x.manual_readability_score != ""
    and Decimal(x.manual_readability_score) != Decimal(0)
]
low_rows = [x for x in rows if x.label == "LOW"]
medium_rows = [x for x in rows if x.label == "MID"]
high_rows = [x for x in rows if x.label == "HIGH"]

_print_rows(low_rows)
_print_rows(medium_rows)
_print_rows(high_rows)
