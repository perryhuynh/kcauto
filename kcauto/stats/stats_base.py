from abc import ABC
from datetime import datetime


class StatsBase(ABC):
    start_time = None

    def __init__(self, start_time):
        self.start_time = start_time

    @property
    def hours_run(self):
        delta = datetime.now() - self.start_time
        hours = delta.total_seconds() / 3600
        if hours < 1:
            return 1
        return hours
