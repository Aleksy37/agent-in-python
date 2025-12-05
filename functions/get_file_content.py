import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    cwd_abs_path = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, file_path)
    absolute_path = os.path.abspath(full_path)

    if not absolute_path.startswith(cwd_abs_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
    if not os.path.isfile(absolute_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(absolute_path, "r") as f:
            file_contents_string = f.read(MAX_CHARS + 1)
        if len(file_contents_string) > MAX_CHARS:
            return file_contents_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_contents_string
    except OSError as e:
            return f"Error: {e}"
    