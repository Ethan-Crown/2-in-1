"""
Evolving actions: code and data feedback loops (Darwinian evolution).
Simulates feedback for demo purposes.
"""

import importlib

# Configuration: which evolution modules to try (in order)
EVOLUTION_CONFIG = [
    "dgm.DGM_outer",  # Example: DGM evolution module
    # Add more evolution modules as needed
]

def evolve_actions(agent_output, run_data=None, evolution_config=EVOLUTION_CONFIG):
    """
    Attempts to use evolution logic from configured modules.
    Falls back to error message if no evolution is available.
    """
    for module_path in evolution_config:
        try:
            evolution_module = importlib.import_module(module_path)
            if hasattr(evolution_module, "evolve_actions"):
                # Pass run_data if supported, else just agent_output
                try:
                    return evolution_module.evolve_actions(agent_output, run_data=run_data)
                except TypeError:
                    return evolution_module.evolve_actions(agent_output)
        except Exception as e:
            print(f"[Evolution] Could not use evolution module {module_path}: {e}")
    # Fallback: no evolution available
    print("[Evolution] No evolution module available.")
    return {"feedback": "error", "rating": "error", "memory_summary": "error", "meta_reason": "error", "multi_agent_results": "error"}
