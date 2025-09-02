import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        full_path_absolute = os.path.abspath(full_path)
        working_directory_absolute = os.path.abspath(working_directory)
        if not full_path_absolute.startswith(working_directory_absolute):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path_absolute):
            return f'Error: "{directory}" is not a directory'
        directory_contents = os.listdir(full_path_absolute)
        list_contents = []
        for content in directory_contents:
            content_path = os.path.join(full_path_absolute, content)
            if os.path.isdir(content_path):
                dir_size = os.path.getsize(content_path)
                list_contents.append(f"- {content}: file_size={dir_size} bytes, is_dir=True")
            elif os.path.isfile(content_path):
                file_size = os.path.getsize(content_path)
                list_contents.append(f"- {content}: file_size={file_size} bytes, is_dir=False")
            else:
                list_contents.append(f"- Unknown: {content}")
        return "\n".join(list_contents)
    except FileNotFoundError:
        return f'Error: Directory "{directory}" not found in working directory "{working_directory}"'
    except PermissionError:
        return f'Error: Permission denied for directory "{directory}" in working directory "{working_directory}"'
    except OSError as e:
        return f'Error: OS error occurred while accessing directory "{directory}": {str(e)}'
    except Exception as e:
        return f'Error: An unexpected error occurred: {str(e)}'
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
    
