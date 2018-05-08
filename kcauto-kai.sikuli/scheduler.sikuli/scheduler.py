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
            'script': None,
            'expedition': None,
            'combat': None
        }
        self.sleep_wake_time = {
            'script': None,
            'expedition': None,
            'combat': None
        }
        self.stop_times = {
            'script': None,
            'expedition': None,
            'combat': None
        }
        self.stop_count_marker = {
            'expedition': None,
            'combat': None
        }
        self.reset_scheduler()

    def conduct_module_sleep(self, module):
        """Method that holds the primary sleep logic for a given module,
        including setting the sleep start and wake times.

        Args:
            module (str): 'script', 'expedition', or 'combat'

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
            if module == 'script':
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

    def _reset_scheduled_sleep(self):
        """Method to reset the scheduled sleep attributes of all modules.
        """
        for module in self.next_scheduled_sleep_time:
            self.next_scheduled_sleep_time[module] = None
            self.sleep_wake_time[module] = datetime.now()

    def conduct_scheduled_stops(self):
        """Method to conduct scheduled stop of scripts and modules as defined
        by the config.
        """
        # script stop section; only stops script
        if self.config.scheduled_stop['script_stop_enabled']:
            if self.config.scheduled_stop['script_stop_count']:
                delta = datetime.now() - self.stats.start_time // 3600
                if delta >= self.config.scheduled_stop['script_stop_count']:
                    Util.log_success(
                        "Ran the designated number of hours. Stopping script.")
                    self.stats.print_stats()
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
                    self.stats.print_stats()
                    sys.exit(0)

        # expedition stop section
        if self.expedition and self.expedition.enabled:
            self._conduct_module_stop(
                self.expedition, 'expedition', self.stats.expeditions_sent)

        # combat stop section
        if self.combat and self.combat.enabled:
            self._conduct_module_stop(
                self.combat, 'combat', self.stats.combat_done)

    def _conduct_module_stop(self, module, mname, done_count):
        """Logic that encompasses for checking and conducting scheduled stop.

        Args:
            module (CombatModule or ExpeditionModule): module instances
            mname (str): string name of module
            done_count (int): count of combat or expeditions completed or sent
        """
        # local variables
        log_display = 'combat sortie' if mname == 'combat' else mname
        stop_mode = '{}_stop_mode'.format(mname)
        stop_count = '{}_stop_count'.format(mname)
        stop_time = '{}_stop_time'.format(mname)

        if self.config.scheduled_stop['{}_stop_enabled'.format(mname)]:
            if self.config.scheduled_stop[stop_count]:
                if (done_count >= self.stop_count_marker[mname] +
                        self.config.scheduled_stop[stop_count]):
                    if self.config.scheduled_stop[stop_mode] == 'script':
                        Util.log_success(
                            "Ran the designated number of {}s. Stopping "
                            "script.".format(log_display))
                        self.stats.print_stats()
                        sys.exit(0)
                    elif self.config.scheduled_stop[stop_mode] == 'module':
                        Util.log_success(
                            "Ran the designated number of {}s. Stopping {} "
                            "module.".format(log_display, mname))
                        module.disable_module()
            if self.config.scheduled_stop[stop_time]:
                # set the script stop time if it is notbeing tracked
                # internally
                if not self.stop_times[mname]:
                    self.stop_times[mname] = (
                        self._get_next_timer_datetime(
                            self.config.scheduled_stop[stop_time]))
                if datetime.now() > self.stop_times[mname]:
                    if self.config.scheduled_stop[stop_mode] == 'script':
                        Util.log_success(
                            "Ran {}s until the designated time. Stopping "
                            "script.".format(log_display))
                        self.stats.print_stats()
                        sys.exit(0)
                    elif self.config.scheduled_stop[stop_mode] == 'module':
                        Util.log_success(
                            "Ran {}s until the designated time. Stopping {} "
                            "module.".format(log_display, mname))
                        module.disable_module()

    def _reset_scheduled_stop(self):
        """Method to reset the scheduled stop attributes of all modules.
        """
        for module in self.stop_times:
            self.stop_times[module] = None
        # manually set the expedition and comabt done markers; scheduled stop
        # will use this as the start value
        self.stop_count_marker['expedition'] = self.stats.expeditions_sent
        self.stop_count_marker['combat'] = self.stats.combat_done

    def reset_scheduler(self):
        """Method to reset the scheduled sleep and scheduled stop attributes of
        all modules.
        """
        self._reset_scheduled_sleep()
        self._reset_scheduled_stop()

    def _get_next_timer_datetime(self, timer):
        """Method to generate a datetime object based on the passed in timer.
        If the generated datetime is in the past, this method automatically
        rolls it over to the next day to ensure it is in the future.

        Args:
            timer (str): timer in 'hhmm' format

        Returns:
            datetime: future datetime object based on timer
        """
        temp_datetime = datetime.now().replace(
            hour=int(timer[:2]),
            minute=int(timer[2:]),
            second=0, microsecond=0)
        if datetime.now() >= temp_datetime:
            # specified time has already passed today, set to next day
            temp_datetime = temp_datetime + timedelta(days=1)
        return temp_datetime
