"""
Main entry point for the superintelligence system (plugin/registry version).
Orchestrates the flow: sense → learn → replicate → api → autonomy.
"""
from .registry import get_plugins

def run_superintelligence():
    print("--- Superintelligence Pipeline Start ---")
    # Sensory input (multimodal)
    sensory_data = None
    for sense_func in get_plugins("sense"):
        sensory_data = sense_func()
        print("[Sense] Sensory data:", sensory_data)
    # Learning (DGM, etc.)
    for learn_func in get_plugins("learn"):
        learn_func(sensory_data)
        print("[Learn] Learning step complete.")
    # Self-replication
    for replicate_func in get_plugins("replicate"):
        replicate_func()
        print("[Replicate] Replication step complete.")
    # API access
    for api_func in get_plugins("api"):
        api_func()
        print("[API] API access step complete.")
    # Autonomy (AutoGPT, etc.)
    for autonomy_func in get_plugins("autonomy"):
        autonomy_func()
        print("[Autonomy] Autonomy step complete.")
    print("--- Pipeline Complete ---")

if __name__ == "__main__":
    run_superintelligence()
