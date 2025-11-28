from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

# Tests for get_files_info.py:
# print(f"Result for current directory:\n{get_files_info("calculator", ".")}")
# print(f"Result for 'pkg' directory:\n {get_files_info("calculator", "pkg")}")
# print(f"Result for '/bin' directory:\n {get_files_info("calculator", "/bin")}")
# print(f"Result for '../' directory:\n {get_files_info("calculator", "../")}")

# Tests for get_file_content.py:
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))
