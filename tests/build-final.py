"""
Here the idea is that it goes through folder whatsapp-analyse and combines all of them into a single file for purpose of creating an executable
"""

import sys

FILE_LST: list = [
    "../whatsapp-analyse/extractor.py",
    "../whatsapp-analyse/operations.py",
    "../whatsapp-analyse/flags.py",
    "../whatsapp-analyse/whatsapp-analyse.py"
] # in order of dependence (i.e, the 1st one is one which doesn't depend on others, next one either is also the same or depends on previous)

MODULES_LST: list = ["re", "sys", "json", "argparse"]

print("Designed to work on a unix based system, not windows, for windows use changes need to be made in how file path are treated")


def remove_user_defined_module_references(main_str: str, sub_string: str) -> str:
    pos:int = main_str.find(sub_string)
    while pos != -1:
        main_str = main_str[:pos] + main_str[pos+len(sub_string)+1:] # +1 as module functions add a extra '.' in the line

        pos = main_str.find(sub_string)

    return main_str


with open("./whatsapp-analyse-full", "w") as fh:
    fh.write("#!/usr/bin/env python3\n\n")

    for module in MODULES_LST:
        fh.write("import " + module + "\n")

    for file in FILE_LST:
        try:
            pass
        except:
            print(file, "not found")
            sys.exit()

        with open(file) as fh_read:
            in_docstring: bool = False
            for line in fh_read:
                if line[0] == "#": # single line comment skip
                    pass
                elif line == "\"\"\"\n": # Skip doc strings
                    in_docstring = not in_docstring
                elif "import " in line: # Skip import module
                    pass
                elif not in_docstring:
                    for file in FILE_LST:
                        file_name_without_py = file.split("/")[-1][:-3]
                        if file_name_without_py in line:
                            line = remove_user_defined_module_references(line, file_name_without_py)
                    fh.write(line)

print()
print("Done :)")

