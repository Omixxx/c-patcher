import os
import sys
from modules.types.TsvFileInput import TsvFileInput
import modules.utils as utils
import modules.diff_evaluator as diff


def validate_args(path: str, path_to_patches: str):
    if (
        not os.path.exists(path)
        or not os.path.exists(path_to_patches)
        or not os.path.isdir(path)
        or not os.path.isdir(path_to_patches)
    ):
        raise FileNotFoundError(
            f"Invalid arguments, {path} must exist and be a directory,\
            {path_to_patches} must exist and be a directory."
        )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Invalid number of arguments")
    tsv_file_path = sys.argv[1]
    original_project = sys.argv[2]

    diff.compute_diffs(tsv_file_path, "abstract_method", "model_prediction", "is_diff")

    # validate_args(path, path_to_patches)

    # rows: list[TsvFileInput] = utils.extract_rows(path_to_patches)
    # os.chdir(path)
    # for row in rows:
    #     row = utils.remove_tokens(row)
    #
    # print(rows[10].is_diff)

    # apply_patches(patch_objects)
