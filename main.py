import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.write_file import schema_write_file, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.get_file_content import schema_get_file_content, get_file_content

load_dotenv()

api_key = os.environ.get('GEMINI_API_KEY')

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
        schema_get_file_content,
    ]
)

def contains_verbose_flag(args):
    return "--verbose" in args

# def get_user_prompt(length=1, verbose_flag=False):
#     if verbose_flag:
#         return "".join(sys.argv[1:]).replace("--verbose", " ").strip()
#     return sys.argv[1] if len(sys.argv) > length  else ""

def get_user_prompt(verbose_flag=False):
    args = sys.argv[1:]
    if verbose_flag:
        args = [arg for arg in args if arg != "--verbose"]
        return "".join(args).strip()
    return sys.argv[1] if len(sys.argv) > 1  else ""

def print_token_metadata(response, user_prompt):
    tokens_in_prompt = response.usage_metadata.prompt_token_count
    tokens_remaining = response.usage_metadata.candidates_token_count
    # print the response as well as the tokens 
    print(f"""User prompt: {user_prompt}\nPrompt tokens: {tokens_in_prompt}\nResponse tokens: {tokens_remaining}""")

def call_function(function_call_part, verbose=False):
    
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    # working directory './calculator'
    print(f" - Calling function: {function_call_part.name}")
    
    function_names_dict = {
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
        "get_file_content": get_file_content,
    }

    function_name = function_call_part.name
    function_result = None
    if function_call_part.name in function_names_dict:
        function_result = function_names_dict[function_name](working_directory="./calculator", **function_call_part.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
 

def generate_gemini_response(user_prompt, system_prompt="", verbose=False):
    # early return case
    if user_prompt == "":
        print(
            'Please provide a prompt.\n'
            'Example: uv run main.py "What is star wars about?"'
        )
        sys.exit(1)

    messages = [
        types.Content(
            role="user",
            parts=[types.Part(text=user_prompt)],
        )
    ]

    mode_name = 'gemini-2.0-flash-001'

    response = client.models.generate_content(
        model=mode_name, 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        ),
    )
    
    # check if we have any functions to call
    response_functions = response.function_calls
    function_response_list = []

    if response_functions:
        for fc in response_functions:
            function_call_result = call_function(fc, verbose=verbose)
            if not function_call_result.parts[0].function_response:
                raise Exception("No function response received.")
            function_response_list.append(function_call_result)
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        print(response.text)

    # print tokens 
    if verbose:
        print_token_metadata(response, user_prompt)
      
          

def main():
    print("Hello from aiagent!\n")
   
    # the prompt we send to the ai model
    user_prompt = ""
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    has_verbose_flag = contains_verbose_flag(sys.argv[1:])
    user_prompt = get_user_prompt(verbose_flag=has_verbose_flag)
    
    generate_gemini_response(user_prompt, system_prompt, has_verbose_flag)
    



if __name__ == "__main__":
    main()
