import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    abspath = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(abspath, file_path))
     
    valid__target_path = os.path.commonpath([abspath, target_path]) == abspath

    if not valid__target_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_path]
    if args != None:
        command.extend(args)
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            cwd=os.path.dirname(target_path),
            timeout=30,
            text=True
        )

        responses = []

        if result.returncode != 0:
            responses.append(f"Process exited with code {result.returncode}")
        
        if result.stderr is None and result.stdout is None:
            responses.append("No output produced")
        
        if result.stdout:
            responses.append(f"STDOUT: {result.stdout}")
    
        if result.stderr:
            responses.append(f"STDERR: {result.stderr}")

    except Exception as err:
        return f"Error: executing Python file: {err}"

    return "\n".join(responses)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to be executed, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="a list of additional arguments to be passed to the file when executing",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="a single argument to be passed"
                    )
            ),
        },
        required=["file_path"],
    ),
)

