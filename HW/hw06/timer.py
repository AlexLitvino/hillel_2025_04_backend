import time
import logging

class TimerContext:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        logging.info(f"Elapsed: {elapsed:.2f} seconds")

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    with TimerContext():
        time.sleep(2)

        with TimerContext():
            time.sleep(4)
