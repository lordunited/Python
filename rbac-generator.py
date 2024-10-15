import yaml

# Define your expanded input data
data = {
    'namespace': 'your-namespace',
    'service_accounts': [
        {
            'name': 'pod-reader-sa',
            'role_bindings': [
                {
                    'role': 'pod-reader',
                    'resources': ['pods'],
                    'verbs': ['get', 'list']
                }
            ]
        },
        {
            'name': 'service-manager-sa',
            'role_bindings': [
                {
                    'role': 'service-manager',
                    'resources': ['services'],
                    'verbs': ['create', 'delete', 'update']
                }
            ]
        },
        {
            'name': 'admin-sa',
            'role_bindings': [
                {
                    'role': 'admin',
                    'resources': ['deployments', 'replicasets'],
                    'verbs': ['*']
                }
            ]
        }
    ],
    'roles': [
        {
            'name': 'pod-reader',
            'resources': ['pods'],
            'verbs': ['get', 'list', 'watch']
        },
        {
            'name': 'service-manager',
            'resources': ['services'],
            'verbs': ['create', 'delete', 'update']
        },
        {
            'name': 'admin',
            'resources': ['deployments', 'replicasets'],
            'verbs': ['*']
        }
    ]
}

# Construct the RBAC YAML structure
rbac_yaml = []

# Generate Roles
for role in data['roles']:
    rbac_yaml.append({
        'apiVersion': 'rbac.authorization.k8s.io/v1',
        'kind': 'Role',
        'metadata': {
            'namespace': data['namespace'],
            'name': role['name']
        },
        'rules': [
            {
                'apiGroups': [''],
                'resources': role['resources'],
                'verbs': role['verbs']
            }
        ]
    })

# Generate RoleBindings for each ServiceAccount
for sa in data['service_accounts']:
    for binding in sa['role_bindings']:
        rbac_yaml.append({
            'apiVersion': 'rbac.authorization.k8s.io/v1',
            'kind': 'RoleBinding',
            'metadata': {
                'name': f"{binding['role']}-binding-{sa['name']}",
                'namespace': data['namespace']
            },
            'subjects': [
                {
                    'kind': 'ServiceAccount',
                    'name': sa['name'],
                    'namespace': data['namespace']
                }
            ],
            'roleRef': {
                'kind': 'Role',
                'name': binding['role'],
                'apiGroup': 'rbac.authorization.k8s.io'
            }
        })

# Convert to YAML format
yaml_output = yaml.dump_all(rbac_yaml, sort_keys=False)

# Write to a file
with open('complex_rbac_config.yaml', 'w') as f:
    f.write(yaml_output)

print("Complex RBAC configuration YAML generated as 'complex_rbac_config.yaml'")
