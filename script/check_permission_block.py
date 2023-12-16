import os
from ruamel.yaml import YAML, scalarstring
from glob import glob
from fnmatch import fnmatch

def check_permissions_block(file_path):
    with open(file_path, 'r') as f:
        yaml = YAML()
        content = yaml.load(f)

    permissions_found = 'N'

    if 'permissions' in content:
        print(f"Permissions block found at the top level in {file_path}")
        permissions_found = 'Y'
    else:
        print(f"Permission block not found at top level")

    if 'jobs' in content:
        for job_name, job_content in content['jobs'].items():
            if 'permissions' in job_content:
                print(f"Permissions block found in job '{job_name}' in {file_path}")
                permissions_found = 'Y'
            else:
                print(f"Permissions block not found in job '{job_name}' in {file_path}")
    
    if permissions_found == 'N':
        print(f"Permissions block not found in {file_path}")
        add_permissions_block(file_path)
 
def add_permissions_block(file_path):
    with open(file_path, 'r') as file:
        yaml = YAML()
        data = yaml.load(file)

    permissions_block = {
        'permissions': 'write-all'
    }

    # Check if 'on' block exists
    if 'on' in data:
        # Find the index of 'on' block
        on_index = list(data).index('on')

        # Check if 'on' is a dictionary or a list
        if isinstance(data['on'], dict):
            # Insert a blank line before 'on:' block
            data.yaml_add_eol_comment("\n", key='on', column=0)
            # Insert 'permissions' block after the blank line
            data.insert(on_index + 1, permissions_block)
        elif isinstance(data['on'], list):
            # Insert 'permissions' block after 'on:' block
            data.insert(on_index + 1, permissions_block)

        with open(file_path, 'w') as file:
            yaml.dump(data, file)

        print(f"Added 'permissions: write-all' after 'on:' block in {file_path}")
    else:
        print(f"'on:' block not found in {file_path}. Skipping...")

def process_workflow_files():
    # Get a list of all .yml files in the .github/workflows directory
    workflow_files = glob('.github/workflows/*.yml')

    # Patterns for files to be excluded
    exclude_patterns = ['token-permission.yml']

    for file_path in workflow_files:
        # Extracting only the file name from the full path
        file_name = os.path.basename(file_path)
        
        # Check if the file should be excluded
        if any(fnmatch(file_name, pattern) for pattern in exclude_patterns):
            print(f"Skipping {file_path}")
            continue

        check_permissions_block(file_path)

if __name__ == "__main__":
    process_workflow_files()
