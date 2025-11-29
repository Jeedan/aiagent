import os
from google.genai import types
from functions.is_permitted_directory import is_permitted_directory


def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
       
        if not is_permitted_directory(working_directory, full_path):
             return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # ensure the directory exists
        # if not create it
        dir_name = os.path.dirname(full_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        # create the file
        # overwrite if it does exist
        # create if it does not
        with open(full_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"


schema_write_file = types.FunctionDeclaration(
    name ="write_file",
    description="Creates file with specified content in designated directory, overwrites it if it exists.",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties ={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)