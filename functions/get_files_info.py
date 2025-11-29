import os
from google.genai import types
from functions.is_permitted_directory import is_permitted_directory

def get_files_info(working_directory, directory="."):
    final_string = "" 
    try:
        full_path = os.path.join(working_directory, directory)
       
        if not is_permitted_directory(working_directory, full_path):
            return (f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory")
        
        isDir = os.path.isdir(full_path)

        if not isDir:
            return (f'Error: "{directory}" is not a directory')
        
        wd = os.listdir(full_path)

        # get info for each file
        for file in wd:
            file_size = os.path.getsize(os.path.join(full_path, file))
            file_information = f"- {file}: file_size={file_size} bytes, is_dir={os.path.isdir(os.path.join(full_path, file))}\n"
            final_string += file_information
        return final_string    
    
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name ="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties ={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)