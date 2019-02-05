import os
import importlib.util

def load():
    modulelist = []

    for plugin in [x for x in os.listdir('./plugins/') if os.path.isdir('./plugins/' + x)]:
        spec = importlib.util.spec_from_file_location(plugin, './plugins/' + plugin + '/__init__.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        modulelist.append(module)

    for module in modulelist:
        module.load()