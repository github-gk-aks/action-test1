import os
from ruamel.yaml import YAML
from glob import glob
from fnmatch import fnmatch

def check_permissions_block(file_path):
    with open(file_path, 'r') as f:
        yaml = YAML()
        try:
            content = yaml.load(f)
        except yaml.YAMLError as exc:
            print(f"Error in file {file_path}: {exc}")
            return

    try:
        if 'permissions' in content:
            print(f"Permissions block found at the top level in {file_path}")
    except KeyError:
        pass

    try:
        if 'jobs' in content:
            for job_name, job_content in content['jobs'].items():
                if 'permissions' in job_content:
                    print(f"Permissions block found in job '{job_name}' in {file_path}")
    except KeyError:
        pass

    if 'permissions' not in content and 'jobs' not in content:
        print(f"Permissions block not found in {file_path}")

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
