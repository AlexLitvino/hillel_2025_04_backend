### 1. Write a Timer Context Manager

Write a context manager called `TimerContext` that measures and logs the execution time of its block.

```python
import time
import logging

class TimerContext:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start
        logging.info(f"Elapsed: {elapsed:.2f} seconds")

logging.basicConfig(level=logging.INFO)

with TimerContext():
    time.sleep(2)
```

Test it with various code blocks.

---

### 2. Temporary Configuration Context Manager

Create a context manager `Configuration` that applies changes to a global configuration temporarily and restores the original after the context.

Requirements:

- Accepts updates as a dictionary.
- Restores original configuration even if an error occurs.
- Optionally accepts a validator function.

Example skeleton:

```python
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
```

Test with valid and invalid updates.


Comments:
Great job overall
- TimeLimiter issues:
  - Raises TimeoutError from a background thread, which cannot be caught in the main thread; as a result, the except TimeoutError does not work.
  - Uses threading.excepthook, but this does not propagate exceptions to the main thread context.
- Configuration context manager:
  - Saves a copy of GLOBAL_CONFIG in __enter__, but does not return self or any value (recommended for with statements).
  - Validator is called only on updates, not on the full configuration after merging updates, which could lead to invalid global states.
  - On invalid config, exception is raised before global update—this is correct.

