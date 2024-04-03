import sys
from modules.custom_types.TsvFileInput import TsvFileInput
import modules.utils as utils
import subprocess, os, logging


TEMP_FILE_NAME = "DummyClass.java"
CURRENT_DIR = os.getcwd()
RSM_DIR = CURRENT_DIR + "/lib/"


def __parse_rms_output(output: str) -> float:
    lines = output.replace("\n", "").split(" ")
    score = lines[-1].split("\t")[-1]
    return float(score) if score.strip() != "NaN" else 0.0


def __wrap_in_a_temp_dummy_class_file(text: str):
    with open(TEMP_FILE_NAME, "w") as f:
        f.write("class DummyClass{\n" + text + "\n}")


def __compute_readability(text: str) -> float:
    os.chdir(RSM_DIR)
    __wrap_in_a_temp_dummy_class_file(text)
    result = subprocess.run(
        ["java", "-jar", "rsm.jar", TEMP_FILE_NAME], capture_output=True
    )
    os.chdir(CURRENT_DIR)
    return __parse_rms_output(result.stdout.decode())


logging.basicConfig(level=logging.INFO)
tsv_path = sys.argv[1]
rows: list[TsvFileInput] = utils.extract_rows(tsv_path)
line_number = 0
for row in rows:

    row.predictions_readability_score = ""
    if row.does_contain_errors == "":
        break

    if row.does_contain_errors == "True":
        line_number += 1
        continue

    score = __compute_readability(row.detokenized_method)
    row.predictions_readability_score = score.__str__()
    logging.info(
        f"{row.name} -> line {line_number}\noriginal score: {row.readabilityScore}\nprediction score: {str(score)}\n\n"
    )
    line_number += 1

print("Writing to file...")
utils.update_tsv(tsv_path, rows)
print("Done!")
