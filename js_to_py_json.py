def js_json_path_to_python(js_path):
    # Split the path by '.' to get individual components
    components = js_path.split('.')
    python_path = ""

    for component in components:
        # Check if the component has array access, indicated by []
        if '[' in component and ']' in component:
            # Split component into key and index
            key, index = component[:-1].split('[')
            # Append the key and index access to the python path
            python_path += f"['{key}'][{index}]"
        else:
            # Append the key access to the python path
            python_path += f"['{component}']"

    return python_path

# Example usage:
js_path = "data[0].relationships['customers-also-bought-apps'].data[0].attributes.privacy.privacyTypes[0].dataCategories"
python_path = js_json_path_to_python(js_path)
print(python_path)
