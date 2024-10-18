import functools
import logging
from src.base.models import BoxFailureResponseModel

LOGGER = logging.getLogger(__name__)

def exception_handler_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            LOGGER.error(f"Exception occurred in {func.__name__}: {str(e)}")
            # Return the failure response using BoxFailureResponseModel
            return BoxFailureResponseModel(success="false", message=f"An error occurred: {str(e)}", data=[]).dict()
    return wrapper