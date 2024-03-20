import csv
import os
import sys
from collections import namedtuple


class MethodInfo:
    def __init__(
        self,
        name: str,
        startLine: int,
        endLine: int,
        classPath: str,
        readabilityScore: float,
        label: str,
        originalMethod: str,
        abstractMethod: str,
        model_prediction: str,
        manual_flag: str,
    ):
        self.name = name
        self.startLine = startLine
        self.endLine = endLine
        self.classPath = classPath
        self.readabilityScore = readabilityScore
        self.label = label
        self.originalMethod = originalMethod
        self.abstractMethod = abstractMethod
        self.model_prediction = model_prediction
        self.manual_flag = manual_flag


def customMethodInfoDecoder(obj):
    return namedtuple("X", obj.keys())(*obj.values())


def validate_args(path: str, path_to_patches: str):
    if (
        not os.path.exists(path)
        or not os.path.exists(path_to_patches)
        or not os.path.isdir(path)
        or not os.path.isdir(path_to_patches)
    ):
        raise FileNotFoundError(
            f"Invalid arguments, {path} must exist and be a directory, {path_to_patches} must exist and be a directory."
        )


def get_patch_objects(path_to_result_csv: str) -> list[MethodInfo]:
    list_of_patch_objects: list[MethodInfo] = []
    with open(path_to_result_csv, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter="\t")
        for row in csv_reader:
            list_of_patch_objects.append(
                MethodInfo(
                    row["name"],
                    int(row["startLine"]),
                    int(row["endLine"]),
                    row["classPath"],
                    float(row["readabilityScore"]),
                    row["label"],
                    row["original_method"],
                    row["abstract_method"],
                    row["model_prediction"],
                    row["manual_flag"],
                )
            )

    return list_of_patch_objects


def apply_patches(patch_objects: list[MethodInfo]):
    for patch in patch_objects:
        with open(patch.classPath, "r") as file:
            lines = file.readlines()

        before = lines[0 : patch.startLine - 1]
        afther = lines[patch.endLine + 1 : len(lines)]
        with open(patch.classPath, "w") as file:
            file.write("")
            file.writelines(before)
            file.writelines(patch.originalMethod)
            file.writelines(afther)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Invalid number of arguments")
    path = sys.argv[1]
    path_to_patches = sys.argv[2]

    # validate_args(path, path_to_patches)
    patch_objects: list[MethodInfo] = get_patch_objects(path_to_patches)
    os.chdir(path)
    for patch in patch_objects:
        print(patch.classPath)
    # apply_patches(patch_objects)
