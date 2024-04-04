import sys, os, subprocess
import modules.utils as utils


def patch(class_path: str, start_line: int, end_line: int, patch: str):
    with open(class_path, "r") as file:
        file_lines = file.readlines()
        # lines index start form 0 in file_lines!!
        below_original_method = file_lines[end_line - 1 :]
        above_original_method = file_lines[: start_line - 1]
        patched_file = (
            "".join(above_original_method) + patch + "".join(below_original_method)
        )
        with open(class_path, "w") as file:
            file.write(patched_file)

tsv_file_path = sys.argv[1]
project_path = sys.argv[2]

rows = utils.extract_rows(tsv_file_path)
os.chdir(project_path)
for row in rows:

    if row.does_contain_errors == "":
        break

    if bool(row.does_contain_errors) == True:
        continue

    patch(row.classPath, int(row.startLine), row.endLine, row.detokenized_method)
    
        
