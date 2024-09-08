import logging
from typing import Callable
from utils.circular_queue import CircularQueue

error_queue_struct = CircularQueue(size=10)


def error_log(f: Callable[..., None]) -> Callable[..., None]:
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(e)
        return None

    return wrapper


def error_enqueue(f: Callable[..., None]) -> Callable[..., None]:

    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            error_queue_struct.enqueue((f, e))
        return None

    return wrapper


def error_queue_peek():
    return error_queue_struct.peek()


def error_queue_pop():
    return error_queue_struct.dequeue()