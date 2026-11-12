import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if working_dir_abs == target_dir:
        print("Result for current directory:")
    else:
        print(f"Result for '{directory}' directory:")

    if not os.path.isdir(target_dir):
      return f'Error: "{directory}" is not a directory'
  
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    directory_items:list[str] = [""]
    for item in os.listdir(target_dir):
        directory_items.append(f"{item}: file_size={os.path.getsize(os.path.join(target_dir, item))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, item))}\n")
    
    return "- ".join(directory_items)