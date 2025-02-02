import os
import time
import random
from datetime import datetime, time as dt_time


class Scheduler:
    """
    A class to handle posting schedules and delays.
    """

    def __init__(self, schedule_config=None, delay_range=(5, 15)):
        """
        Initialize the Scheduler with configuration and delay range.

        Parameters:
        schedule_config (list): A list of tuples with time ranges [(start, end), ...]
        delay_range (tuple): A tuple defining the randomized delay range in seconds (min, max)
        """
        self.schedule = []
        self.delay_range = delay_range
        if schedule_config:
            for start_time, end_time in schedule_config:
                self.add_time_slot(start_time, end_time)

    def add_time_slot(self, start_time, end_time):
        """
        Add a time slot for posting.

        Parameters:
        start_time (str): Start time in "HH:MM" format
        end_time (str): End time in "HH:MM" format
        """
        self.schedule.append((self._parse_time(start_time), self._parse_time(end_time)))

    def is_within_schedule(self):
        """
        Check if the current time is within the allowed schedule.

        Returns:
        bool: True if within schedule, False otherwise
        """
        now = datetime.now().time()
        print(f"Time: {now} ")
        return any(start <= now <= end for start, end in self.schedule)

    def get_random_delay(self):
        """
        Get a random delay within the defined delay range.

        Returns:
        int: A random delay in seconds
        """
        return random.randint(*self.delay_range)

    @staticmethod
    def _parse_time(time_str):
        """
        Parse a time string into a datetime.time object.

        Parameters:
        time_str (str): Time string in "HH:MM" format.

        Returns:
        datetime.time: Parsed time object.
        """
        return datetime.strptime(time_str, "%H:%M").time()
