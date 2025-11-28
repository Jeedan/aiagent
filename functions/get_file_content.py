import os
from functions.config import MAX_CHARS
from functions.is_permitted_directory import is_permitted_directory

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)

        # # make sure we are in the permitted working directory
        if not is_permitted_directory(working_directory, full_path):
            return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

        # check if the file exists and is a regular file
        if not os.path.isfile(full_path):
            return (f'Error: File not found or is not a regular file: "{file_path}"')
        
        # read the file contents
        # truncate if too long and return with appended message
        # otherwise just return the file contents as a string
        with open(full_path, 'r') as f:
            file_content_string = f.read()  
            if len(file_content_string) > MAX_CHARS:
                return f'{file_content_string[:MAX_CHARS]}..."{file_path}" truncated at 10000 characters' 
            
            return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"