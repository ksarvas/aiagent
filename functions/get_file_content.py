import os
from google.genai import types
from functions.config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        full_path_absolute = os.path.abspath(full_path)
        working_directory_absolute = os.path.abspath(working_directory)
        if not full_path_absolute.startswith(working_directory_absolute):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path_absolute):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(full_path_absolute, 'r') as file:
            file_content_string = file.read(MAX_CHARS + 1)
            if len(file_content_string) > MAX_CHARS:
                file_content_string = file_content_string[:MAX_CHARS]
                file_content_string += f"[...File \"{file_path}\" truncated at {MAX_CHARS} characters]"
        return file_content_string
    except FileNotFoundError:
        return f'Error: File "{file_path}" not found in working directory "{working_directory}"'
    except PermissionError:
        return f'Error: Permission denied for file "{file_path}" in working directory "{working_directory}"'
    except OSError as e:
        return f'Error: OS error occurred while accessing file "{file_path}": {str(e)}'
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read content from, relative to the working directory.",
            ),
        },
    ),
)
    