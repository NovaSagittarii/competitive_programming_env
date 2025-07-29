import re
import os
import json


def main():
    dirs = ["kactl/content"]
    out = {}
    process_files_in_directories(dirs, lambda f, c: process(out, f, c))

    with open(".vscode/kactl.code-snippets", "w") as f:
        f.write(json.dumps(out))


def process(out: dict, path: str, code: str):
    """
    Generated using Gemini (convert JS to Python)
    """
    if not path.endswith(".h"):
        return
    path = "kactl/" + path

    code = re.sub(r"#pragma[^\n]+\n+", "", code)
    code = code.replace("$", "\\$")
    code = code.strip()
    body_lines = code.split("\n")
    body_lines.extend(["", "$0"])
    body_lines.sort(key=lambda x: x.startswith("#include"), reverse=True)

    for i, s in enumerate(body_lines):
        if s.startswith("#include"):
            body_lines[i] = f"${{{i+1}:{s}}}"

    out[path] = {
        "scope": "cpp",
        "prefix": path,
        "body": body_lines,
    }


def process_files_in_directories(directory_paths, f):
    """
    Generated using Gemini:
    given a list of paths to directories, for every file run the function f(path_relative_to_directory, file_content)

    Iterates through a list of directory paths, and for every file found,
    runs the function f(path_relative_to_directory, file_content).

    Args:
        directory_paths (list): A list of strings, where each string is a path to a directory.
        f (function): The function to run for each file. It should accept two arguments:
                      (path_relative_to_directory, file_content).
    """
    for base_directory in directory_paths:
        if not os.path.isdir(base_directory):
            print(f"Warning: '{base_directory}' is not a valid directory. Skipping.")
            continue

        print(f"Processing directory: {base_directory}")
        for root, _, files in os.walk(base_directory):
            for filename in files:
                file_path_absolute = os.path.join(root, filename)

                # Calculate the path relative to the base_directory
                # os.path.relpath handles cases where root is the same as base_directory
                path_relative_to_directory = os.path.relpath(
                    file_path_absolute, base_directory
                )

                try:
                    with open(file_path_absolute, "r", encoding="utf-8") as file:
                        file_content = file.read()
                    f(path_relative_to_directory, file_content)
                except UnicodeDecodeError:
                    print(
                        f"Could not decode {file_path_absolute} with utf-8. Trying binary read."
                    )
                    try:
                        with open(
                            file_path_absolute, "rb"
                        ) as file:  # Read as binary if UTF-8 fails
                            file_content = file.read()
                        f(path_relative_to_directory, file_content)
                    except Exception as e:
                        print(f"Error reading file (binary) {file_path_absolute}: {e}")
                except Exception as e:
                    print(f"Error reading file {file_path_absolute}: {e}")


if __name__ == "__main__":
    main()
