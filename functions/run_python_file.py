import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):

    base_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(base_dir, file_path))

    if not target_path.startswith(base_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
    
    if not target_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
    try:
        output = []
        result = subprocess.run(
             ["python", target_path, *args],
             capture_output=True,
             timeout=30,
             cwd=base_dir,
             text=True
        )
        if result.stdout:
             output.append(f"STDOUT: {result.stdout}")
        if result.stdout:
             output.append(f"STDERR: {result.stderr}")
        if result.returncode != 0:
            output.append(f'Process exited with code {result.returncode}')
        if not output:
             return "No output produced"
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}" 