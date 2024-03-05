import json
import os
import sys
from collections import namedtuple


class MethodInfo:
    def __init__(
        self,
        name: str,
        method: str,
        startLine: int,
        endLine: int,
        classPath: str,
        readabilityScore: float,
    ):
        self.name = name
        self.method = method
        self.startLine = startLine
        self.endLine = endLine
        self.classPath = classPath
        self.readabilityScore = readabilityScore


def customMethodInfoDecoder(obj):
    return namedtuple("X", obj.keys())(*obj.values())


def patch(path: str, path_to_patch: str):
    print("cia")


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
    path = sys.argv[1]
    path_to_patch = sys.argv[2]

    validate_args(path, path_to_patch)
    f = open(path_to_patch, "r")
    method_info: MethodInfo = json.load(f, object_hook=customMethodInfoDecoder)
