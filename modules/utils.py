import csv
from modules.custom_types.TsvFileInput import TsvFileInput


def extract_rows(path_to_result_tsv: str) -> list[TsvFileInput]:
    list_of_patch_objects: list[TsvFileInput] = []
    with open(path_to_result_tsv, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter="\t")
        for row in csv_reader:
            list_of_patch_objects.append(
                TsvFileInput(
                    row["name"],
                    int(row["startLine"]),
                    int(row["endLine"]),
                    row["classPath"],
                    float(row["readabilityScore"]),
                    row["label"],
                    row["originalMethod"],
                    row["abstractMethod"],
                    row["model_prediction"],
                    row["is_diff"],
                    row["partially_detokenized_method"],
                    row["detokenized_method"],
                    row["predictions_readability_score"],
                    row["does_test_suite_pass"],
                    row["does_contain_errors"],
                )
            )

    return list_of_patch_objects

def update_tsv(tsv_path: str, rows:list[TsvFileInput]):
    with open(tsv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = TsvFileInput.attributes_as_list_of_strings()
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(vars(row))
