import os

def get_files_info(working_directory, directory="."):
    final_string = "" 
    try:
        full_path = os.path.join(working_directory, directory)
        absolute_path = os.path.abspath(full_path)

        abs_working_directory =  os.path.abspath(working_directory)

        #print(f"AbsoulteWorking directory: '{abs_working_directory}'")
        #print(f"Absolute Path: '{absolute_path}'")
        
        if not absolute_path.startswith(abs_working_directory):
            raise Exception(f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory")
        
        isDir = os.path.isdir(full_path)

        if not isDir:
            raise Exception(f'Error: "{directory}" is not a directory')
        
        wd = os.listdir(full_path)

        # get info for each file
        for file in wd:
            file_size = os.path.getsize(os.path.join(full_path, file))
            file_information = f"- {file}: file_size={file_size} bytes, is_dir={os.path.isdir(os.path.join(full_path, file))}\n"
            final_string += file_information
        return final_string    
    
    except Exception as e:
        return f"Error: {str(e)}"