import pymel.core as pm
# Cleanup namespaces
    namespaces = pm.namespaceInfo(listOnlyNamespaces=True, recurse=True)
    namespaces.remove("UI")
    namespaces.remove("shared")

    for i in range(len(namespaces), 0, -1):
        pm.namespace(removeNamespace=namespaces[i - 1], mergeNamespaceWithRoot=True)