import sys, os
import modules.utils as utils


def patch(class_path: str, start_line: int, end_line: int, patch: str) -> str:
    with open(class_path, "r") as file:
        file_lines = file.readlines()
        # lines index start form 0 in file_lines!!
        below_original_method = file_lines[end_line - 1 :]
        above_original_method = file_lines[: start_line - 1]
        return "".join(above_original_method) + patch + "".join(below_original_method)


tsv_file_path = sys.argv[1]
project_path = sys.argv[2]

rows = utils.extract_rows(tsv_file_path)
current_path = os.getcwd()
os.chdir(project_path)
patch_output: list[str] = []
i = 0
for row in rows:
    if row.detokenized_method == "":
        continue

    patch_output.append(
        patch(row.classPath, int(row.startLine), row.endLine, row.detokenized_method)
    )
    if i == 0:
        break
    i += 1

os.chdir(current_path)
with open("out.java", "w") as file:
    file.write(patch_output[0])
