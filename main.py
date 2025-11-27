import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.environ.get('GEMINI_API_KEY')

client = genai.Client(api_key=api_key)

# the prompt we send to the ai model
user_prompt = ""


def contains_verbose_flag(args):
    for arg in args:
        if "--verbose" in arg:
            return True
    return False

def get_user_prompt(index, length=1):
    return sys.argv[index] if len(sys.argv) > length  else ""


def generate_gemini_response(prompt, verbose=False):
    # early return case
    if prompt == "":
        print("""Please provide a prompt.\nExample: uv run main.py "What is star wars about?" """)
        sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)
    
    if verbose:
        tokens_in_prompt = response.usage_metadata.prompt_token_count
        tokens_remaining = response.usage_metadata.candidates_token_count
        # print the response as well as the tokens 
        print(response.text)
        print(f"""User prompt: {prompt}\nPrompt tokens: {tokens_in_prompt}\nResponse tokens: {tokens_remaining}""")
    else:
        print(response.text)
          

def main():
    print("Hello from aiagent!\n")
   
    has_verbose_flag = contains_verbose_flag(sys.argv[1:])

    if has_verbose_flag:
        user_prompt = "".join(sys.argv[1:]).replace("--verbose", " ").strip()
    else:
        user_prompt = get_user_prompt(1)

    generate_gemini_response(user_prompt, has_verbose_flag)
    



if __name__ == "__main__":
    main()
