from .parser.parser import add_custom_componentsB

def Title(children, browser, *args, **kwargs):
    browser.setWindowTitle(children)

components = {
    "Title": Title
}

# The default value of components in renderer.py is {}. Means that no component is added.
# But we are still returning components. This means that it's the way of importing this object
def add_custom_components(custom_components):
    global components
    components.update(custom_components)
    unparsed_components = {}
    for key in custom_components.keys():
        unparsed_components[f"/{key}"] = key
    add_custom_componentsB(unparsed_components)

    return components