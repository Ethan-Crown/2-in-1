import importlib

# Configuration: which multi-agent modules to try (in order)
MULTI_AGENT_CONFIG = [
    "dgm.coding_agent_polyglot",  # Example: DGM multi-agent module
    # Add more multi-agent modules as needed
]

def multi_agent_reasoning(*args, multi_agent_config=MULTI_AGENT_CONFIG, **kwargs):
    """
    Attempts to use multi-agent logic from configured modules.
    Falls back to error message if no multi-agent is available.
    """
    for module_path in multi_agent_config:
        try:
            multi_agent_module = importlib.import_module(module_path)
            if hasattr(multi_agent_module, "multi_agent_reasoning"):
                return multi_agent_module.multi_agent_reasoning(*args, **kwargs)
        except Exception as e:
            print(f"[Multi-Agent] Could not use multi-agent module {module_path}: {e}")
    # Fallback: no multi-agent available
    print("[Multi-Agent] No multi-agent module available.")
    return {"result": "error"}