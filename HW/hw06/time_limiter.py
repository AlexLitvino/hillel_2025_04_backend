import time
import threading

def excepthook(args):
    if args.exc_type is TimeoutError:
        raise TimeoutError('Inside excepthook')

threading.excepthook = excepthook


class TimeLimiter:

    def __init__(self, timeout: float):
        self.timeout = timeout

    def __enter__(self):
        self.run = True
        def _time_checker(start_time: float, timeout: float):
            while self.run:
                if time.perf_counter() - start_time > timeout:
                    raise TimeoutError
                else:
                    time.sleep(1)

        start_time = time.perf_counter()
        self.thread = threading.Thread(target=_time_checker, args=(start_time, self.timeout))
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.run = False
        self.thread.join()


def n_seconds_duration(duration: int):
    print('Function started')
    time.sleep(duration)
    print('Function stopped')


if __name__ == '__main__':
    try:
        with TimeLimiter(2):
            n_seconds_duration(3)
    except TimeoutError:
        print('Caught')  # Doesn't work
