import importlib

# Configuration: which memory modules to try (in order)
MEMORY_CONFIG = [
    "dgm.git_utils",  # Example: DGM memory/history module
    # Add more memory modules as needed
]

def save_run_history(run_data, memory_config=MEMORY_CONFIG):
    """
    Attempts to use memory logic from configured modules.
    Falls back to error message if no memory is available.
    """
    for module_path in memory_config:
        try:
            memory_module = importlib.import_module(module_path)
            if hasattr(memory_module, "save_run_history"):
                return memory_module.save_run_history(run_data)
        except Exception as e:
            print(f"[Memory] Could not use memory module {module_path}: {e}")
    print("[Memory] No memory module available.")
    return {"result": "error"}

def load_history(memory_config=MEMORY_CONFIG):
    """
    Attempts to use memory logic from configured modules.
    Falls back to error message if no memory is available.
    """
    for module_path in memory_config:
        try:
            memory_module = importlib.import_module(module_path)
            if hasattr(memory_module, "load_history"):
                return memory_module.load_history()
        except Exception as e:
            print(f"[Memory] Could not use memory module {module_path}: {e}")
    print("[Memory] No memory module available.")
    return {"history": "error"}