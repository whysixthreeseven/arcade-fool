# External libraries:
from datetime import datetime


def timestamp():
    """
    Returns the current date and time in a string format.
    
    Return
    --------
    timestamp: `str`
        The current date and time in a string format: `"2026-10-19 14:36:00"`.
    """

    # Getting time value and formatting:
    dt_now: datetime = datetime.now()
    dt_format: str = r"%Y-%m-%d %H:%M:%S"
    dt_timestamp: str = dt_now.strftime(dt_format)

    # Returning:
    return dt_timestamp

