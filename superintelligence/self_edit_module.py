import importlib

# Configuration: which self-edit modules to try (in order)
SELF_EDIT_CONFIG = [
    "dgm.self_improve_step",  # Example: DGM self-edit module
    # Add more self-edit modules as needed
]

def self_edit(*args, self_edit_config=SELF_EDIT_CONFIG, **kwargs):
    """
    Attempts to use self-edit logic from configured modules.
    Falls back to error message if no self-edit is available.
    """
    for module_path in self_edit_config:
        try:
            self_edit_module = importlib.import_module(module_path)
            if hasattr(self_edit_module, "self_edit"):
                return self_edit_module.self_edit(*args, **kwargs)
        except Exception as e:
            print(f"[Self-Edit] Could not use self-edit module {module_path}: {e}")
    # Fallback: no self-edit available
    print("[Self-Edit] No self-edit module available.")
    return {"result": "error"}