import csv
from types.TsvFileInput import TsvFileInput


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
                    row["original_method"],
                    row["abstract_method"],
                    row["model_prediction"],
                    row["is_diff"],
                    row["partially_detokenized_method"],
                    row["detokenized_method"],
                )
            )

    return list_of_patch_objects


def remove_tokens(patch_object: TsvFileInput) -> TsvFileInput:
    tokens = {
        "$indentation$": "\t",
        "$whitespace$": " ",
        "$newline$": "\n",
    }

    for token in tokens:
        patch_object.model_prediction = patch_object.model_prediction.replace(
            token, tokens[token]
        )
    return patch_object
    # dobbiamo considerare che molti metodi hanno un $indentation$ ad inizio riga, quindi nel caso va rimosso
