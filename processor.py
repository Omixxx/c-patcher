import os
import hashlib
import sys
import subprocess
import modules.utils as utils
from modules.custom_types.TsvFileInput import TsvFileInput

TEMP_FILE = "temp_file.java"
ESCAPE_CHAR = "//"


def create_file(file_path: str, content: str = ""):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write(content)


def calculate_hash(file_path: str) -> str:
    hash_obj = hashlib.new("sha256")
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def prepare_to_manual_evaluation(row: TsvFileInput):

    with open(TEMP_FILE, "w") as file:
        for line in row.originalMethod.split("\n"):
            file.write(f"{ESCAPE_CHAR}{line}\n")

        for word in row.partially_detokenized_method.split(" "):
            if word != "":
                file.write(f"{utils.to_camel_case(word)} ")


def get_detokenized_method(file_path: str) -> str:
    with open(file_path, "r") as file:
        lines = file.readlines()
    output = ""
    for line in lines:
        if not line.startswith(ESCAPE_CHAR):
            output += line
    return output


def evaluate(tsv_path: str, rows: list[TsvFileInput]):
    create_file(TEMP_FILE)

    for row in rows:
        if row.is_diff == "False":
            continue

        if row.detokenized_method != "" or row.does_contain_errors == "True":
            continue

        prepare_to_manual_evaluation(row)
        before_hash = calculate_hash(TEMP_FILE)
        subprocess.run(["nvim", TEMP_FILE])
        after_hash = calculate_hash(TEMP_FILE)

        if before_hash == after_hash:
            row.does_contain_errors = bool.__str__(True)
            continue

        row.does_contain_errors = bool.__str__(False)
        row.detokenized_method = get_detokenized_method(TEMP_FILE)

        if row.detokenized_method == "":
            break

    utils.update_tsv(tsv_path, rows)



if __name__ == "__main__":
    tsv_path = sys.argv[1]
    rows: list[TsvFileInput] = utils.extract_rows(tsv_path)
    evaluate(tsv_path, rows)
