from datetime import datetime, timedelta
from random import randint
from util import Util


class Scheduler(object):
    def __init__(self, config):
        self.config = config
        self.next_scheduled_sleep_time = {
            'kca': None,
            'expedition': None,
            'combat': None
        }
        self.sleep_wake_time = {
            'kca': None,
            'expedition': None,
            'combat': None
        }
        self.reset_scheduled_sleep_all()

    def conduct_module_sleep(self, module):
        if not self.config.scheduled_sleep['{}_sleep_enabled'.format(module)]:
            return False

        return self.set_and_check_timers(
            'kca',
            self.config.scheduled_sleep['{}_sleep_start_time'.format(module)],
            self.config.scheduled_sleep['{}_sleep_length'.format(module)])

    def set_and_check_timers(self, module, start_time, sleep_length):
        cur_time = datetime.now()

        # if a scheduled sleep time is not set, set it
        if not self.next_scheduled_sleep_time[module]:
            self.next_scheduled_sleep_time[module] = datetime.now().replace(
                hour=int(start_time[:2]),
                minute=int(start_time[2:]),
                second=0, microsecond=0)
            if cur_time >= self.next_scheduled_sleep_time[module]:
                # specified time has already passed today, set to next day
                self.next_scheduled_sleep_time[module] = (
                    self.next_scheduled_sleep_time[module] + timedelta(days=1))

        # if the current time is before the wake time, stay asleep
        if cur_time < self.sleep_wake_time[module]:
            return True

        # if the current time is past the schedule sleep time, go to sleep
        if cur_time >= self.next_scheduled_sleep_time[module]:
            Util.log_warning(
                "Scheduled Sleep beginning. Resuming in ~{} hours.".format(
                    sleep_length))
            # set the wake time when going to sleep so the previous conditional
            # is triggered
            self.sleep_wake_time[module] = cur_time + timedelta(
                hours=int(sleep_length),
                minutes=int(sleep_length % 1 * 60) + randint(1, 15))
            # set the next scheduled sleep time as well
            self.next_scheduled_sleep_time[module] = (
                self.next_scheduled_sleep_time[module] + timedelta(days=1))
            return True
        return False

    def reset_scheduled_sleep(self, module):
        """Method to reset the scheduled sleep attributes of a specific module.
        """
        self.next_scheduled_sleep_time[module] = None
        self.sleep_wake_time[module] = datetime.now()

    def reset_scheduled_sleep_all(self):
        for module in self.next_scheduled_sleep_time:
            self.reset_scheduled_sleep(module)
