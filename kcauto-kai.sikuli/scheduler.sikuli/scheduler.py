from datetime import datetime, timedelta
from random import randint
from util import Util


class Scheduler(object):
    def __init__(self, config, stats):
        self.config = config
        self.stats = stats
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
        """Method that holds the primary sleep logic for a given module,
        including setting the sleep start and wake times.

        Args:
            module (str): 'kca', 'expedition', or 'combat'

        Returns:
            bool: True if the module should be asleep; False otherwise
        """
        if not self.config.scheduled_sleep['{}_sleep_enabled'.format(module)]:
            # if scheduled sleep for a particular module is not enabled, just
            # return False
            return False

        start_time = self.config.scheduled_sleep[
            '{}_sleep_start_time'.format(module)]
        sleep_length = self.config.scheduled_sleep[
            '{}_sleep_length'.format(module)]
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
            if module == 'kca':
                Util.log_warning(
                    "Beginning scheduled sleep. Resuming in ~{} hours.".format(
                        sleep_length))
            else:
                Util.log_warning(
                    "Beginning scheduled sleep for {} module. "
                    "Resuming in ~{} hours.".format(module, sleep_length))
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

    def _reset_scheduled_sleep(self, module):
        """Method to reset the scheduled sleep attributes of a specific module.
        """
        self.next_scheduled_sleep_time[module] = None
        self.sleep_wake_time[module] = datetime.now()

    def reset_scheduled_sleep_all(self):
        """Method to reset the scheduled sleep attributes of all modules, using
        the _reset_scheduled_sleep private method.
        """
        for module in self.next_scheduled_sleep_time:
            self._reset_scheduled_sleep(module)
