import os

def get_files_info(working_directory, directory="."):
    cwd_abs_path = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory, directory)
    absolute_path = os.path.abspath(full_path)

    if not absolute_path.startswith(cwd_abs_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'
    
    lines = []
    try:
        for entry in os.listdir(absolute_path):
            file_path = os.path.join(absolute_path, entry)
            try:
                size = os.path.getsize(file_path)
                is_dir = os.path.isdir(file_path)
                line = f'- {entry}: file_size={size} bytes, is_dir={is_dir}'
                lines.append(line)
            except OSError as e:
                return f"Error: {e}"
    except OSError as e:
        return f"Error: {e}"
    return "\n".join(lines)