# Guided Project on Boot.Dev
We created a small LLM that will fix bugs, or read and print the contents of files or run and print the results of said python files to the user. 
We used the free tier Gemini API

from the course itself:
# What Does the Agent Do?
This a CLI tool that:
1. Accepts a coding task (e.g., "strings aren't splitting in my app, pweeze fix 🥺👉🏽👈🏽")
  - Chooses from a set of predefined functions to work on the task, for example:
  - Scan the files in a directory
  - Read a file's contents
  - Overwrite a file's contents
  - Execute the Python interpreter on a file
2. Repeats step 2 until the task is complete (or it fails miserably, which is possible)
For example, I have a buggy calculator app, so I used my agent to fix the code:
```python
> uv run main.py "fix my calculator app, it's not starting correctly"
# Calling function: get_files_info
# Calling function: get_file_content
# Calling function: write_file
# Calling function: run_python_file
# Calling function: write_file
# Calling function: run_python_file
# Final response:
# Great! The calculator app now seems to be working correctly. The output shows the expression and the result in a formatted way.
```
