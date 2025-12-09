import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Create a file or overwrite the contents of a file that already exists, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file we want to write to, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    cwd_abs_path = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(full_path)

    if not absolute_path.startswith(cwd_abs_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(absolute_path):
        try:
            os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
        except OSError as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(absolute_path) and os.path.isdir(absolute_path):
            return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(absolute_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except OSError as e:
        return f"Error: writting to file: {e}"