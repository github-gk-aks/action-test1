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
        on_block = data['on']

        # Check if 'on' block is a list
        if isinstance(on_block, list):
            # If 'on' is a list, add 'permissions' as a new item
            data.insert(data.ca.items['on'][0].end_mark.line, permissions_block, key='on')
        elif isinstance(on_block, dict):
            # If 'on' is a dictionary, add 'permissions' to it
            data.yaml_add_eol_comment("\n", key='on', column=0)
            data.insert(data.ca.items['on'][0].end_mark.line + 1, permissions_block, key='on')

        with open(file_path, 'w') as file:
            yaml.dump(data, file)
        
        print(f"Added 'permissions: write-all' in {file_path}")
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
