import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    abspath = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(abspath, file_path))
     
    valid__target_path = os.path.commonpath([abspath, target_path]) == abspath

    if not valid__target_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_path,  "r") as f:
            file_content = f.read(MAX_CHARS)
            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as err:
        return "Error: {err}"
    
    return file_content
