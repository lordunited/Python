
from ansible.module_utils.basic import AnsibleModule
import os

def run_module():
    # Define available arguments/parameters that a user can pass to the module
    module_args = {
        "user": {"type": "str", "required": True},
    }

    # Seed the result dict in the object
    result = {
        "changed": False,
        "exists": False,
    }

    # Instantiate AnsibleModule
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Retrieve the file path
    user_name = module.params["user"]
    
    # Check if the file exists


    # Exit with the result
    module.exit_json(**result)

def main():
    run_module()

if __name__ == "__main__":
    main()