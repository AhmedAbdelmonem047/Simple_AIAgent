import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a file given the file's path and the content to be written",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file which will be written to",
                },
                "content": {
                    "type": "string",
                    "description": "The content that will be written inside the file",
                },
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        with open(target_dir, "w") as f:
             f.write(content)
    
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'