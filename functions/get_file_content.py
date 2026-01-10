import os
from config import MAX_CHARS
from google.genai import types

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and prints the content of the specificed file, truncated to MAX_CHARS (set to 10000)",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to be read, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"],
    ),
)