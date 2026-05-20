import os
import py_compile
import traceback

with open("syntax_check.log", "w") as log:
    for root, dirs, files in os.walk("backend"):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                try:
                    py_compile.compile(filepath, doraise=True)
                except py_compile.PyCompileError as e:
                    log.write(f"Syntax error in {filepath}:\n{str(e)}\n\n")
