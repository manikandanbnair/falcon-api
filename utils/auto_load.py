import pkgutil,importlib
def auto_load():
    package_name = 'rest'
    package = importlib.import_module(package_name)

    for loader,module_name,is_pkg in pkgutil.iter_modules(package.__path__):

        module = importlib.import_module(f"{package_name}.{module_name}")


