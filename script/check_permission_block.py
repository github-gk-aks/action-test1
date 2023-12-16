import os
from ruamel.yaml import YAML
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
        # Add a blank line and insert 'permissions' block after 'on' block
        content['permissions'] = 'write-all'

    # Insert a blank line after 'on' block
        with open(file_path, 'w') as f:
            yaml.dump(content, f)

        insert_blank_line(content, 'permissions', 'on', yaml)
        insert_blank_line(content, 'jobs', 'permissions', yaml)

def insert_blank_line(data, key, anchor, yaml):
    if anchor in data and key in data:
        index = list(data.keys()).index(anchor) + 1
        # Insert a blank line after the specified key only if it's not the last key
        if index < len(data) and key in data.ca.items:
            indent = data.ca.items[key][0].start_mark.column
            data.yaml_set_comment_before_after_key(key, before='\n', indent=indent)
            data.insert(index, key, data[key])
    elif key not in data:
        # Insert a new key with a blank line after the anchor
        index = list(data.keys()).index(anchor) + 1
        data.insert(index, key, "")


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
