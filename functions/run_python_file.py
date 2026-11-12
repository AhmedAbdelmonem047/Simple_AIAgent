import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a python script at the specified file path with the given arguments if they were given",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to execute",
                },
                "args": {
                    "type": ["array", "null"],
                    "items": {"type": "string"},
                    "description": "the arguments that will be sent as parameters to the function if they were given",
                },
            },
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_dir]
        if args:    
            command.extend(args)
        process:subprocess.CompletedProcess = subprocess.run(command, capture_output=True, text=True, timeout= 30, cwd=working_dir_abs)
        output_list:list[str] = []
        if process.returncode != 0:
            output_list.append(f"Process exited with code {process.returncode}")
        if process.stdout == "" and process.stderr == "":
            output_list.append("No output produced")
        if process.stdout != "" :
            output_list.append(f"STDOUT: {process.stdout}")
        if process.stderr != "":
            output_list.append(f"STDERR: {process.stderr}")
        
        return "\n".join(output_list)
            
    except Exception as e:
        return f"Error: executing Python file: {e}"