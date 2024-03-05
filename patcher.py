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


def get_patch_objects(path_to_patches: str) -> list[MethodInfo]:
    patch_objects: list[MethodInfo] = []
    for root, directories, files in os.walk(path_to_patches):
        for file in files:
            if not file.endswith(".json"):
                continue
            f = open(os.path.join(root, file), "r")
            patch_objects.append(json.load(f, object_hook=customMethodInfoDecoder))
            f.close()
    return patch_objects


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Invalid number of arguments")
    path = sys.argv[1]
    path_to_patches = sys.argv[2]

    validate_args(path, path_to_patches)
    patch_objects: list[MethodInfo] = get_patch_objects(path_to_patches)

    for patch in patch_objects:
        print(patch.readabilityScore)
