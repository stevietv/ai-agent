import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abspath = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(abspath, file_path))
     
    valid__target_path = os.path.commonpath([abspath, target_path]) == abspath

    if not valid__target_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    try:
        with open(target_path,  "w") as f:
            f.write(content)
    except Exception as err:
        return "Error: {err}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to the specificed file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to be written, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to the file",
            ),
        },
        required=["file_path","content"],
    ),
)