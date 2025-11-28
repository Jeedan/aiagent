import os

# checks if we are in the permitted working directory
def is_permitted_directory(working_directory, full_path):
    absolute_path = os.path.abspath(full_path)
    abs_working_directory =  os.path.abspath(working_directory)

    return absolute_path.startswith(abs_working_directory)