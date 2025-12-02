import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import MAX_ITERATIONS
from functions.call_functions import call_function, available_functions
from prompts import system_prompt

load_dotenv()

api_key = os.environ.get('GEMINI_API_KEY')

client = genai.Client(api_key=api_key)

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
        

def generate_content(user_prompt, client, messages, verbose=False):
    mode_name = 'gemini-2.0-flash-001'#'gemini-2.5-flash'
    response = client.models.generate_content(
            model=mode_name, 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], 
                system_instruction=system_prompt
            ),
        )
    
    for candidate in response.candidates:
        messages.append(candidate.content)
    
    # check if we have any functions to call
    response_functions = response.function_calls
    function_response_list = []

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    
    if verbose:
        print_token_metadata(response, user_prompt)

    if response_functions:
        for fc in response_functions:
            function_call_result = call_function(fc, verbose=verbose)
            if not function_call_result.parts[0].function_response:
                raise Exception("No function response received.")
            function_response_list.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    

    if not response.function_calls and response.text != "":
        return response.text

    if function_response_list and len(function_response_list) > 0:
        messages.append(
            types.Content(role="user", parts=function_response_list))

    return None

def generate_gemini_response(user_prompt, verbose=False):
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

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERATIONS:
            break

        try:
            final_response = generate_content(user_prompt, client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error during content generation: {e}")
            break


    
# the app entry point      
def main():
    print("Hello from aiagent!\n")
   
    # the prompt we send to the ai model
    has_verbose_flag = contains_verbose_flag(sys.argv[1:])
    user_prompt = get_user_prompt(verbose_flag=has_verbose_flag)
    

    generate_gemini_response(user_prompt, has_verbose_flag)
 


if __name__ == "__main__":
    main()
