import os 
import subprocess
import sys
from google.genai import types
from functions.is_permitted_directory import is_permitted_directory

def run_python_file(working_directory, file_path, args=[]):
    try:
 
        full_path = os.path.join(working_directory, file_path)

        if not is_permitted_directory(working_directory, full_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'
        
        if not full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        completed_process = subprocess.run([sys.executable, file_path, *args], cwd=working_directory, capture_output=True, text=True, timeout=30)
        
     
        cleaned_stdout = completed_process.stdout.strip()
        cleaned_stderr = completed_process.stderr.strip()
        if cleaned_stdout == "" and cleaned_stderr == "":
            return f"No output produced."
         
        result = f"STDOUT: {cleaned_stdout}\nSTDERR: {cleaned_stderr}"
        
         
        if completed_process.returncode != 0:
            return result + f"\nProcess exited with code {completed_process.returncode}"
        
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file = types.FunctionDeclaration(
    name ="run_python_file",
    description="Runs a Python file in the designated directory if it exists. Then outputs the STDOUT and STDERR of the execution.",
    parameters = types.Schema(
        type=types.Type.OBJECT, 
        properties ={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The list of arguments to pass to the Python file during execution.",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
        required=["file_path"]
    ),
)