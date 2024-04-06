import sys, os, subprocess
from modules.custom_types.TsvFileInput import TsvFileInput 
import modules.utils as utils
import logging


def patch(class_path: str, start_line: int, end_line: int, patch: str):
    class_path_with_projectname_removed = "/".join(class_path.split("/")[1:])
    with open(class_path_with_projectname_removed, "r") as file:
        file_lines = file.readlines()
        # lines index start form 0 in file_lines!!
        below_original_method = file_lines[end_line:]
        above_original_method = file_lines[: start_line - 1]
        patched_file = (
            "".join(above_original_method) + patch + "".join(below_original_method)
        )
    with open(class_path_with_projectname_removed, "w") as file:
        file.write(patched_file)


def run_test_suite(row: TsvFileInput):
    # module_to_test = row.classPath.split("/")[1]
    command = ["mvn", "-Dcheckstyle.skip=true", "test", "-pl", "guava-tests"]
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    for line in process.stdout:
        logging.info(line.decode("utf-8").strip())

    status_code = process.wait()

    if status_code == 0:
        logging.info(f"Test suite passed for {row.classPath}")
        row.does_test_suite_pass = True.__str__()
    else:
        logging.info(f"Test suite failed for {row.classPath}")
        row.does_test_suite_pass = False.__str__()


logging.basicConfig(level=logging.INFO)
tsv_file_path = sys.argv[1]
project_path = sys.argv[2]

rows = utils.extract_rows(tsv_file_path)
current_dir = os.getcwd()
os.chdir(project_path)
i = 0
for row in rows:

    print(i)

    if i == 100:
        break

    if row.does_contain_errors == "":
        break

    if row.does_contain_errors == True.__str__():
        i = i + 1
        continue

    logging.info(f"Applying patches...")
    patch(row.classPath, row.startLine, row.endLine, row.detokenized_method)
    logging.info(f"Testing {row.classPath}")
    run_test_suite(row)
    logging.info("Removing patches...")
    subprocess.run(["git", "checkout", "."])
    print("\n")

    i = i + 1

os.chdir(current_dir)
utils.update_tsv(tsv_file_path, rows)
