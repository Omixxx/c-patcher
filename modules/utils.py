import csv
import wordninja
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





def to_camel_case(word):
    assert word != ""

    begin_trailing_chars, end_trailing_chars, word = __remove_trailing_char(word)
    words = wordninja.split(word)
    if len(words) <= 1:
        return word
    print(begin_trailing_chars, end_trailing_chars)
    camel_case_word = "".join(
        begin_trailing_chars
        + words[0]
        + "".join(word.capitalize() for word in words[1:])
        + end_trailing_chars
    )

    return camel_case_word

def __remove_trailing_char(word: str):
    trailing_characters = set(".,;:()[]{}<>!@#$%^&*-_+=|\\/?><")
    alphabet = set("abcdefghijklmnopqrstuvwxyz")
    begin_trailing_chars = ""
    end_trailing_chars = ""

    is_only_trailing_chars = True
    for char in word:
        if char.lower() in alphabet:
            is_only_trailing_chars = False
            break

    if is_only_trailing_chars:
        return begin_trailing_chars, end_trailing_chars, ""

    while word and word[-1] in trailing_characters:
        end_trailing_chars += word[-1]
        word = word[:-1]

    while word and word[0] in trailing_characters:
        begin_trailing_chars += word[0]
        word = word[1:]

    return begin_trailing_chars, end_trailing_chars[::-1], word

