import csv
import wordninja
from modules.custom_types.TsvFileInput import TsvFileInput
from binarytree import Node

TRAILING_CHARACTERS = set('\t".,;:()[]{}<>!@#$%^&*-_+=|\\/?><\n')


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


def update_tsv(tsv_path: str, rows: list[TsvFileInput]):
    with open(tsv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = TsvFileInput.attributes_as_list_of_strings()
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow(vars(row))


def __to_camel_case(word: str):
    if len(word.strip()) == 0:
        return ""

    if word[0] in TRAILING_CHARACTERS:
        return word

    words = wordninja.split(word)
    camel_case_word = (words[0] if len(words) > 0 else "") + "".join(
        [w.capitalize() for w in words[1:]]
    )

    return camel_case_word


def generate_trailing_parse_tree(word: str):
    root = Node(word)
    word_list = list(word)
    for char in word_list:
        if char in TRAILING_CHARACTERS:
            index = word_list.index(char)
            root.value = char
            root.left = Node("".join(word_list[:index]))
            root.right = generate_trailing_parse_tree("".join(word_list[index + 1 :]))
            break

    return root


def resolve(root: Node | None) -> str:
    if root is None:
        return ""

    left = __to_camel_case(root.left.value) if root.left else ""
    middle = (
        __to_camel_case(root.value)
        if root.value not in TRAILING_CHARACTERS
        else root.value
    )
    right = resolve(root.right)
    return "".join(left + middle + right)


def to_camel_case(word: str) -> str:
    word = word.replace("    ", "\t")
    result: str = ""
    separator = ""
    for w in word.split(" "):
        root = generate_trailing_parse_tree(w)
        result = result + separator + resolve(root)
        separator = " "
    return result
