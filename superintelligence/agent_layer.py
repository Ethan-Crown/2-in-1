"""
Agent layer: decision-making using AutoGPT/Darwin-core logic.
Simulates agent decision for demo purposes.
"""

import importlib

# Configuration: which agent modules to try (in order)
AGENT_CONFIG = [
    "AutoGPT.agent",   # Example: AutoGPT agent module
    "dgm.coding_agent", # Example: DGM agent module
    # Add more agent modules as needed
]

def agent_decision(reasoned_data, memory=None, agent_config=AGENT_CONFIG):
    """
    Attempts to use agent logic from configured modules.
    Falls back to error message if no agent is available.
    """
    for module_path in agent_config:
        try:
            agent_module = importlib.import_module(module_path)
            if hasattr(agent_module, "agent_decision"):
                # Try to pass memory if supported
                try:
                    return agent_module.agent_decision(reasoned_data, memory=memory)
                except TypeError:
                    return agent_module.agent_decision(reasoned_data)
        except Exception as e:
            print(f"[Agent] Could not use agent module {module_path}: {e}")
    # Fallback: no agent available
    print("[Agent] No agent module available.")
    return {"action": "error: no agent available"}
