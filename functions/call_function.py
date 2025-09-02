import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file


def call_function(function_call_part, verbose=False):
    function_map = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
    }

    try:
        function_name = function_call_part.name
        function_args = function_call_part.args

        full_args = function_args.copy()
        full_args["working_directory"] = "./calculator"

        func_to_call = function_map.get(function_name)
        if func_to_call:
            if verbose:
                print(f"Calling function: {function_name}({function_args})")
            else:
                print(f" - Calling function: {function_name}")
            result = func_to_call(**full_args)
            # Now you can return the proper types.Content response with the result!
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": result},
                    )
                ],
            )
        else:
            # Handle the unknown function case
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )

    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name if 'function_name' in locals() else "unknown",
                    response={"error": f"Error executing function call: {e}"},
                )
            ],
        )