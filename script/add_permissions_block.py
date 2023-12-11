import os
from ruamel.yaml import YAML
from glob import glob
from fnmatch import fnmatch

def add_permissions_block(file_path):
    with open(file_path, 'r') as f:
        content = YAML().load(f)

    # Check if 'on' block exists and if 'permissions' block is not present in jobs
    if 'on' in content and ('jobs' not in content or 'permissions' not in content['jobs']):
        # Add a blank line for readability
        if 'jobs' in content and 'permissions' in content['jobs']:
            jobs = content['jobs']
            if isinstance(jobs, list):
                for job in jobs:
                    if 'permissions' not in job:
                        job.yaml_set_comment_before_after_key('permissions', before='\n')
                        job.insert(list(job).index('name') + 1, 'permissions', 'write-all')
            else:
                jobs.yaml_set_comment_before_after_key('permissions', before='\n')
                jobs.insert(list(jobs).index('name') + 1, 'permissions', 'write-all')
        else:
            content['permissions'] = 'write-all'

        with open(file_path, 'w') as f:
            YAML().dump(content, f, default_flow_style=False)

def process_workflow_files():
    # Get a list of all .yml files in the .github/workflows directory
    workflow_files = glob('.github/workflows/*.yml')

    # Patterns for files to be excluded
    exclude_patterns = ['token-permission.yml', 'add-license-file.yml']

    for file_path in workflow_files:
        # Check if the file should be excluded
        if any(fnmatch(file_path, pattern) for pattern in exclude_patterns):
            print(f"Skipping {file_path}")
            continue

        add_permissions_block(file_path)

if __name__ == "__main__":
    process_workflow_files()
