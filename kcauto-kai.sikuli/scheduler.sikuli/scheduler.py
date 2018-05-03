import sys
from datetime import datetime, timedelta
from random import randint
from util import Util


class Scheduler(object):
    def __init__(self, config, stats):
        self.config = config
        self.stats = stats
        self.expedition = None
        self.combat = None
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
        self.stop_times = {
            'script': None,
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
            self.next_scheduled_sleep_time[module] = (
                self._get_next_timer_datetime(start_time))

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

    def conduct_scheduled_stops(self):
        """Method to conduct scheduled stop of scripts and modules as defined
        by the config.
        """
        # TODO: code cleanup; check for enabled and existing expedition
        # and combat modules...
        # script stop section; only stops script
        if self.config.scheduled_stop['script_stop_enabled']:
            if self.config.scheduled_stop['script_stop_count']:
                delta = datetime.now() - self.stats.start_time // 3600
                if delta >= self.config.scheduled_stop['script_stop_count']:
                    Util.log_success(
                        "Ran the designated number of hours. Stopping script.")
                    sys.exit(0)
            if self.config.scheduled_stop['script_stop_time']:
                # set the script stop time if it is notbeing tracked internally
                if not self.stop_time['script']:
                    self.stop_time['script'] = (
                        self._get_next_timer_datetime(
                            self.config.scheduled_stop['script_stop_time']))
                if datetime.now() > self.stop_time['script']:
                    Util.log_success(
                        "Ran until the designated time. Stopping script.")
                    sys.exit(0)

        # expedition stop section
        if self.config.scheduled_stop['expedition_stop_enabled']:
            if self.config.scheduled_stop['expedition_stop_count']:
                if (self.config.scheduled_stop['expeditions_sent'] >=
                        self.config.scheduled_stop['expedition_stop_count']):
                    if (self.config.scheduled_stop['expedition_stop_mode'] ==
                            'script'):
                        Util.log_success(
                            "Ran the designated number of expeditions. "
                            "Stopping script.")
                        sys.exit(0)
                    elif (self.config.scheduled_stop['expedition_stop_mode'] ==
                            'module'):
                        Util.log_success(
                            "Ran the designated number of expeditions. "
                            "Stopping expedition module.")
                        self.expedition.disable_module()
            if self.config.scheduled_stop['expedition_stop_time']:
                # set the script stop time if it is notbeing tracked internally
                if not self.stop_time['expedition']:
                    self.stop_time['expedition'] = (
                        self._get_next_timer_datetime(
                            self.config.scheduled_stop['script_stop_time']))
                if datetime.now() > self.stop_time['expedition']:
                    if (self.config.scheduled_stop['expedition_stop_mode'] ==
                            'script'):
                        Util.log_success(
                            "Ran expeditions until the designated time. "
                            "Stopping script.")
                        sys.exit(0)
                    elif (self.config.scheduled_stop['expedition_stop_mode'] ==
                            'module'):
                        Util.log_success(
                            "Ran expeditions until the designated time. "
                            "Stopping expedition module.")
                        self.expedition.disable_module()

        # combat stop section
        if self.config.scheduled_stop['combat_stop_enabled']:
            if self.config.scheduled_stop['combat_stop_count']:
                if (self.config.scheduled_stop['combat_done'] >=
                        self.config.scheduled_stop['combat_stop_count']):
                    if (self.config.scheduled_stop['combat_stop_mode'] ==
                            'script'):
                        Util.log_success(
                            "Ran the designated number of combat sorties. "
                            "Stopping script.")
                        sys.exit(0)
                    elif (self.config.scheduled_stop['combat_stop_mode'] ==
                            'module'):
                        Util.log_success(
                            "Ran the designated number of combat sorties. "
                            "Stopping combat module.")
                        self.combat.disable_module()
            if self.config.scheduled_stop['combat_stop_time']:
                # set the script stop time if it is notbeing tracked internally
                if not self.stop_time['combat']:
                    self.stop_time['combat'] = (
                        self._get_next_timer_datetime(
                            self.config.scheduled_stop['combat_stop_time']))
                if datetime.now() > self.stop_time['combat']:
                    if (self.config.scheduled_stop['combat_stop_mode'] ==
                            'script'):
                        Util.log_success(
                            "Ran combat sorties until the designated time. "
                            "Stopping script.")
                        sys.exit(0)
                    elif (self.config.scheduled_stop['combat_stop_mode'] ==
                            'module'):
                        Util.log_success(
                            "Ran combat sorties until the designated time. "
                            "Stopping combat module.")
                        self.combat.disable_module()

    def _get_next_timer_datetime(self, timer):
        temp_datetime = datetime.now().replace(
            hour=int(timer[:2]),
            minute=int(timer[2:]),
            second=0, microsecond=0)
        if datetime.now() >= temp_datetime:
            # specified time has already passed today, set to next day
            temp_datetime = temp_datetime + timedelta(days=1)
        return temp_datetime
