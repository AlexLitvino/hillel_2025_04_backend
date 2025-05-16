GLOBAL_CONFIG = {"feature_a": True, "max_retries": 3}

class Configuration:
    def __init__(self, updates, validator=None):
        self.updates = updates
        self.validator = validator

    def __enter__(self):
        self.global_config = GLOBAL_CONFIG.copy()
        if self.validator:
            if not self.validator(self.updates):
                raise Exception('Config for update is not valid')
        GLOBAL_CONFIG.update(self.updates)

    def __exit__(self, exc_type, exc_value, traceback):
        global GLOBAL_CONFIG
        GLOBAL_CONFIG = self.global_config

def validate_config(config):
    # Ensure max_retries >= 0
    return config.get("max_retries", 0) >= 0


if __name__ == '__main__':

    # No validation
    with Configuration({"feature_a": False, "feature_b": True}):
        print(GLOBAL_CONFIG)

    print(GLOBAL_CONFIG)
    print()

    # Successful validation
    with Configuration({"feature_a": False, "feature_c": True, "max_retries": 4}, validator=validate_config):
        print(GLOBAL_CONFIG)

    print(GLOBAL_CONFIG)
    print()

    # Unsuccessful validation
    try:
        with Configuration({"max_retries": -1}, validator=validate_config):
            print(GLOBAL_CONFIG)
    except Exception as e:
        print(e)

    print(GLOBAL_CONFIG)
