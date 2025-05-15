GLOBAL_CONFIG = {"feature_a": True, "max_retries": 3}

class Configuration:
    def __init__(self, updates, validator=None):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

def validate_config(config):
    # Ensure max_retries >= 0
    return config.get("max_retries", 0) >= 0

"""
- Accepts updates as a dictionary.
- Restores original configuration even if an error occurs.
- Optionally accepts a validator function.
"""