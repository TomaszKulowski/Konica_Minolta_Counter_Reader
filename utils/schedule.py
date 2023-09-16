"""
This Python script provides a utility class, 'Schedule,' for scheduling recurring events based on
specified time intervals. It allows users to check and manage scheduled events based on daily, monthly,
or yearly intervals.
"""

from datetime import datetime

from dateutil.relativedelta import relativedelta


class Schedule:
    """
    A utility class for scheduling recurring events based on specified time intervals.

    Attributes:
        periods_of_time (list): A list of valid time intervals for scheduling ('day', 'month', 'year').
        next_call (str): The next scheduled event time in the format of the specified time interval.
        interval (int): The time interval in units of the specified time interval ('day', 'month', 'year').

    Methods:
        get_call_every():
            Get the currently set time interval for scheduling.

        call_every(call_every: str):
            Set the time interval for scheduling ('day', 'month', or 'year').

        check_time() -> bool:
            Check if it's time for the next scheduled event based on the set time interval and interval value.
    """
    def __init__(self, interval: int, next_call: str):
        """
        Initialize the Schedule object with the specified interval and next scheduled event time.

        Args:
            interval (int): The time interval in units of the specified time interval ('day', 'month', 'year').
            next_call (str): The next scheduled event time in the format of the specified time interval.
        """
        self.periods_of_time = ['day', 'month', 'year']
        self.next_call = next_call
        self.interval = interval
        self._call_every = None

    def get_call_every(self) -> str:
        """
        Get the currently set time interval for scheduling.

        Returns:
            str: The time interval for scheduling ('day', 'month', or 'year').
        """
        return self._call_every

    def call_every(self, call_every: str):
        """
        Set the time interval for scheduling ('day', 'month', or 'year').

        Args:
            call_every (str): The time interval for scheduling ('day', 'month', or 'year').

        Raises:
            ValueError: If the provided time interval is not in the list of valid intervals.
        """
        if call_every not in self.periods_of_time:
            raise ValueError
        self._call_every = call_every

    def check_time(self) -> bool:
        """
        Check if it's time for the next scheduled event based on the set time interval and interval value.

        Returns:
            bool: True if it's time for the next scheduled event, False otherwise.
        """
        current_time = getattr(datetime.now(), self.get_call_every())
        if self.next_call == current_time:
            relative = relativedelta()
            relative.day = 0
            relative.month = 0
            relative.year = 0

            relative_attr = getattr(relative, self.get_call_every())
            self.next_call = relative_attr + current_time + self.interval
            return True

        return False
