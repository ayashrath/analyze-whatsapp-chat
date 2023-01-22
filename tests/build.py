"""
Here the idea is that it goes through folder whatsapp-analyse and combines all of them into a single file for purpose of creating an executable
"""

import sys

FILE_LST: list = [
    "../whatsapp-analyse/extractor.py",
    "../whatsapp-analyse/operations.py",
    "../whatsapp-analyse/flags.py",
    "../whatsapp-analyse/whatsapp_analyse.py"
]  # in order of dependence (i.e, the 1st one is one which doesn't depend on others, next one either is also the same or depends on previous)

MODULES_LST: list = ["re", "sys", "json", "argparse"]  # These are the modules needed by the project

BUILD_ON_UNIX_SYSTEM: bool = True  # Used as unix based use '/' in file path while windows uses '\'

print("Designed to work on a unix based system, not windows, for windows use changes need to be made in how file path "
      "are treated")


def remove_user_defined_module_references(main_str: str, sub_str: str) -> str:
    """
    It goes through a string and removes occurrence of sub-string passed to it
    Intended to remove the name of module and '.' from line containing -> module_name.func_name()
    """

    pos: int = main_str.find(sub_str)
    while pos != -1:
        main_str = main_str[:pos] + main_str[pos+len(sub_str)+1:]  # +1 as module functions add an extra '.' in the line

        pos = main_str.find(sub_str)

    return main_str


with open("./whatsapp-analyse-full", "w", encoding="utf-8") as fh:
    if BUILD_ON_UNIX_SYSTEM:
        fh.write("#!/usr/bin/env python3\n\n")

    for module in MODULES_LST:
        fh.write("import " + module + "\n")

    for file in FILE_LST:
        try:
            with open(file, encoding="utf-8") as fh_read:
                in_docstring: bool = False
                for line in fh_read:
                    if line[0] == "#":  # single line comment skip
                        pass
                    elif line == "\"\"\"\n":  # Skip doc strings
                        in_docstring = not in_docstring
                    elif "import " in line:  # Skip import module
                        pass
                    elif not in_docstring:
                        for project_file in FILE_LST:
                            if BUILD_ON_UNIX_SYSTEM:
                                file_name_without_py = project_file.rsplit("/", maxsplit=1)[-1][:-3]
                            else:
                                file_name_without_py = project_file.rsplit("\\", maxsplit=1)[-1][:-3]
                            if file_name_without_py in line:
                                line = remove_user_defined_module_references(line, file_name_without_py)
                        fh.write(line)
        except FileNotFoundError:
            print()
            print(file, "not found")
            sys.exit()

print()
print("Done :)")
