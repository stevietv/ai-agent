import os

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
