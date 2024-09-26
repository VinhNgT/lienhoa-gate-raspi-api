from concurrent.futures import ThreadPoolExecutor

from app.exceptions import app_exceptions


class RequestQueue:
    def __init__(self, max_size: int):
        self._thread_executor = ThreadPoolExecutor(max_workers=1)

        self.max_size = max_size
        self._current_size = 0

    def submit(self, fn, /, *args, **kwargs):
        if self._current_size >= self.max_size:
            raise app_exceptions.TooManyRequestsException()

        self._current_size += 1
        future = self._thread_executor.submit(fn, *args, **kwargs)

        def decrease_size(_):
            self._current_size -= 1

        future.add_done_callback(decrease_size)

        return future

    def shutdown(self):
        self._thread_executor.shutdown(cancel_futures=True)

    def __len__(self):
        return self._current_size
