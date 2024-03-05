import json
import os
import sys


def patch(path: str, path_to_patch: str):
    validate_args(path, path_to_patch)
    f = open(path_to_patch, "r")
    data = json.load(f)
    for key in data:
        print(key)


def validate_args(path: str, path_to_patch: str):
    if (
        not os.path.exists(path)
        or not os.path.exists(path_to_patch)
        or not os.path.isdir(path)
        or not os.path.isfile(path_to_patch)
    ):
        raise FileNotFoundError(
            f"Invalid arguments, {path} must exist and be a directory, {path_to_patch} must exist and be a file"
        )
    if path_to_patch.split(".")[-1] != "json":
        raise ValueError(f"Invalid arguments, {path_to_patch} must be a json file")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Invalid number of arguments")
    patch(sys.argv[1], sys.argv[2])
