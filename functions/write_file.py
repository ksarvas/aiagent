import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(full_path) 
        if not full_path.startswith(working_directory):
            # Check if the full path is within the working directory
            # If not, return an error message
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(full_path):
            parent_directory = os.path.dirname(full_path)
            create_path = os.makedirs(parent_directory, exist_ok=True)
        with open(full_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except IsADirectoryError:
        return f'Error: "{file_path}" is a directory, not a file'
    except FileNotFoundError:
        return f'Error: Directory "{file_path}" not found in working directory "{working_directory}"'
    except PermissionError:
        return f'Error: Permission denied for directory "{file_path}" in working directory "{working_directory}"'
    except OSError as e:
        return f'Error: OS error occurred while accessing directory "{file_path}": {str(e)}'
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a Python file in the specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)