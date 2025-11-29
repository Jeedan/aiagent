import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
load_dotenv()

api_key = os.environ.get('GEMINI_API_KEY')

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

def contains_verbose_flag(args):
    for arg in args:
        if "--verbose" in arg:
            return True
    return False

def get_user_prompt(length=1, verbose_flag=False):
    
    if verbose_flag:
        return "".join(sys.argv[1:]).replace("--verbose", " ").strip()
    return sys.argv[1] if len(sys.argv) > length  else ""


def generate_gemini_response(user_prompt, system_prompt="", verbose=False):
    # early return case
    if user_prompt == "":
        print("""Please provide a prompt.\nExample: uv run main.py "What is star wars about?" """)
        sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    mode_name = 'gemini-2.0-flash-001'

    response = client.models.generate_content(model=mode_name, contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),)
    
    # check if we have any functions to call
    response_functions = response.function_calls
    if response_functions:
        for fc in response_functions:
            print(f"Calling function: {fc.name}({fc.args})")
    else:
        print(response.text)

    # print tokens 
    if verbose:
        tokens_in_prompt = response.usage_metadata.prompt_token_count
        tokens_remaining = response.usage_metadata.candidates_token_count
        # print the response as well as the tokens 
        print(f"""User prompt: {user_prompt}\nPrompt tokens: {tokens_in_prompt}\nResponse tokens: {tokens_remaining}""")
          

def main():
    print("Hello from aiagent!\n")
   
    # the prompt we send to the ai model
    user_prompt = ""
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    has_verbose_flag = contains_verbose_flag(sys.argv[1:])
    user_prompt = get_user_prompt(has_verbose_flag)
    
    generate_gemini_response(user_prompt, system_prompt, has_verbose_flag)
    



if __name__ == "__main__":
    main()
