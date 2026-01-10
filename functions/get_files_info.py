import os

def get_files_info(working_directory, directory="."):
    abspath = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abspath, directory))
     
    valid__target_dir = os.path.commonpath([abspath, target_dir]) == abspath

    if not valid__target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abspath):
        return f'Error: "{directory}" is not a directory'
    
    response = []

    for file in os.listdir(target_dir):
        try:
            path = os.path.normpath(os.path.join(target_dir, file))
            file_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            response.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
        except Exception as err:
            return "Error: {err}"

    return "\n".join(response)
