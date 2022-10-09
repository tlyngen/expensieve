import logging
import functools
from time import perf_counter


def timer(func):
    @functools.wraps(func)
    def timer_wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        elapsed_ms = (end_time - start_time) * 1000
        logger.info(f"{func.__qualname__!r} completed in {elapsed_ms:.3f} ms")
        return value
    return timer_wrapper
