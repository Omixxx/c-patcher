import csv
import sys
from modules.custom_types.TsvFileInput import TsvFileInput
import modules.utils as utils


def remove_tokens(model_prediction: str) -> str:
    tokens = {
        "$indentation$": "\t",
        "$whitespace$": " ",
        "$newline$": "\n",
    }

    for token in tokens:
        model_prediction = model_prediction.replace(token, tokens[token])

    return model_prediction


if __name__ == "__main__":
    tsv_path = sys.argv[1]
    rows: list[TsvFileInput] = utils.extract_rows(tsv_path)
    for row in rows:
        if row.abstractMethod != row.model_prediction:
            row.is_diff = bool.__str__(True)
            row.partially_detokenized_method = remove_tokens(row.model_prediction)

    with open(tsv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = TsvFileInput.attributes_as_list_of_strings()
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(vars(row))
