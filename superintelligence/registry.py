"""
Plugin registry for superintelligence capabilities.
"""
REGISTRY = {
    "learn": [],
    "sense": [],
    "replicate": [],
    "api": [],
    "autonomy": [],
}

def register(capability, func):
    REGISTRY[capability].append(func)

def get_plugins(capability):
    return REGISTRY.get(capability, [])
