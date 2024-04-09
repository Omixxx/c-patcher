import sys
import modules.utils as utils


tsv = sys.argv[1]
line_number = sys.argv[2]

rows = utils.extract_rows(tsv)

row = rows[int(line_number) - 1]

with open(f"{row.name}.java", "w") as f:
    f.write(row.originalMethod)
    f.write("\n")
    f.write(row.detokenized_method)
