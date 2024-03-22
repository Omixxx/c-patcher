from types.TsvFileInput import TsvFileInput


def apply_patches(patch_objects: list[TsvFileInput]):
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
