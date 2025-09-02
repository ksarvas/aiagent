import os
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

If you do not know what arguments to provide to a Python file, assume there are none and proceed by calling the function with an empty argument list. Do not ask the user for clarification.

If the user asks to fix a bug in a specific output, please first look into the associated python files and see if anything needs to be fixed in those files for the correct output. When doing this sort of thing, please look for the source of the incorrect behaviour rather than just changing the symptom. If the bug seems to be caused by a recent change, please consider reverting something that was changed incorrectly. Please look into fixing bugs at the source file and do not make your own main.py print the correct result as a forced fix.
"""
model_name = "gemini-2.0-flash-001"

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if len(sys.argv) > 1:
    user_prompt = sys.argv[1]
else:
    print("Error: No prompt provided. Please provide a prompt as a command line argument.")
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

client = genai.Client(api_key=api_key)

# Loop starts here
for i in range(20):  # or while loop with counter
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            )
        )

        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count

    except Exception as e:
        print(f"Error during content generation: {e}")
        sys.exit(1)

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if response.function_calls:
        # Process function calls first
        function_responses = []
        for function_call in response.function_calls:
            verbose = "--verbose" in sys.argv
            function_call_result = call_function(function_call, verbose=verbose)
            function_responses.append(function_call_result.parts[0])
        
            # Only print in verbose mode
            if verbose:
                if function_call_result.parts and hasattr(function_call_result.parts[0], "function_response"):
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                else:
                    raise Exception("No function response found!")
    
        messages.append(types.Content(role="user", parts=function_responses))
    elif response.text:
        # Only check for text if there are no function calls
        print(f"Final response:\n{response.text}")
        break
    else:
        # No function calls and no text - unexpected state
        print("Error: Response contained neither text nor function calls")
        break
    # Handle verbose printing outside of function call logic
    if "--verbose" in sys.argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

# Loop ends here