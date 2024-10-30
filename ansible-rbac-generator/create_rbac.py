import yaml
# resource_mappings = {  # Define resource_mappings dictionary outside the function
#     "low": ["deployments", "pods", "statefulsets", "service", "Events"],
#     "medium": ["deployments", "pods", "statefulsets", "service", "Events", "ConfigMaps"],
#     "high": ["*"]
# }

# def role_def(namespace: str,name: str, apigroups: str, resources: str, verbs: str):
#     verb_mappings = {
#         "read": ["get", "list", "watch"],
#         "write": ["get", "list", "watch", "create", "update", "delete"],
#         "admin": ["*"]  # Grant all verbs for "admin"
#     }

#     resource_mappings = {
#         "low": ["deployments", "pods", "statefulsets", "service", "Events"],
#         "medium": ["deployments", "pods", "statefulsets", "service", "Events","ConfigMaps"],
#         "high": ["*"]  # Grant access to all resources for "high"
#     }

#     desired_verbs = verb_mappings.get(verbs, [])  # Use default empty list for invalid verbs
#     desired_resources = resource_mappings.get(resources, [])  # Use default empty list for invalid resources


#     role_data = f"""
#     apiVersion: rbac.authorization.k8s.io/v1
#     kind: Role
#     metadata:
#       namespace: {namespace}
#       name: {name}
#     rules:
#     - apiGroups: {apigroups.split(',')}
#       resources: {desired_resources}
#       verbs: {desired_verbs}
#     """

#     role_info = yaml.safe_load(role_data)
#     role_verbs = []
#     for verbs in desired_verbs:
#         role_verbs.append(verbs)
        


# # Example usage
# role_yaml = role_def("mmdreza", "mmdreza-api", "", "high", "admin")
# print(yaml.dump(role_yaml, default_flow_style=False))
def role_def(namespace: str, name: str, apigroups: str, resources: str, verbs: str):
    
    verb_mappings = {
        "read": ["get",  "list", "watch"],
        "write": ["get", "list", "watch", "create", "update", "delete"],
        "admin": ["*"]  # Grant all verbs for "admin"
    }
    
    resource_mappings = {
        "low": ["deployments", "pods", "statefulsets", "service", "Events"],
        "medium": ["deployments", "pods", "statefulsets", "service", "Events", "ConfigMaps","Secrets"],
        "high": ["*"]
    }
    apigroups_mapping = {
        "low":["core"],
        "medium":["core","app"],
        "high": [
                "core",
                "apps",
                "batch",
                "networking.k8s.io",
                "storage.k8s.io",
                "rbac.authorization.k8s.io",
                "autoscaling",
                "admissionregistration.k8s.io",
                "policy",
                "scheduling.k8s.io",
                "coordination.k8s.io",
                "flowcontrol.apiserver.k8s.io",
                "certificates.k8s.io",
                "apiextensions.k8s.io",
                "node.k8s.io",
                "authentication.k8s.io",
                "authorization.k8s.io",
                "snapshot.storage.k8s.io"] 
                }
    desired_verbs = verb_mappings.get(verbs)  # Use default empty list for invalid verbs
    desired_resources = resource_mappings.get(resources)  # Use default empty list for invalid resources
    desired_apigroups = apigroups_mapping.get(apigroups)  # Use default empty list for invalid resources

    role_data = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "Role",
        "metadata": {
            "namespace": namespace,
            "name": name
        },
        "rules": [
            {
                "apiGroups": desired_apigroups,
                "resources": desired_resources,
                "verbs": desired_verbs
            }
        ]
    }
    return yaml.dump(role_data, default_flow_style=False)
#role_def(namespace: str, name: str, apigroups: str, resources: str, verbs: str)
role_yaml = role_def("mmdreza", "mmdreza-api", "high", "low", "read")
print(role_yaml)
