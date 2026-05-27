import os
import glob
import importlib

def register_all(app, url_prefix="/api"):
    folder = os.path.dirname(__file__)
    files  = glob.glob(folder + "/*.py")
    for f in files:
        module_name = os.path.basename(f)[:-3]
        if module_name.startswith("_"):
            continue
        module = importlib.import_module(f"app.controllers.{module_name}")
        if hasattr(module, "ctrl"):
            name   = module.ctrl.blueprint.name
            prefix = f"{url_prefix}/{name}"
            app.register_blueprint(module.ctrl.blueprint, url_prefix=prefix)
            print(f"[OK] Blueprint '{name}' enregistré sur {prefix}")