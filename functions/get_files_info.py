import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    print(f"Getting files info for directory: {full_path}")
    
    error_string_prefix = "Error:"
    error_string = f"{error_string_prefix}"
    final_string = f"- README.md: file_size=1032 bytes, is_dir=False\n- src: file_size=128 bytes, is_dir=True\n- package.json: file_size=1234 bytes, is_dir=False"
    return final_string    