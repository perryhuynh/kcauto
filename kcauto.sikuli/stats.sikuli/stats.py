from datetime import datetime
from util import Util


class Stats(object):
    def __init__(self, config):
        """Initializes the Stats module.

        Args:
            config (Config): kcauto Config instance
        """
        self.reset_stats()
        self.config = config

    def reset_stats(self):
        """Resets all stats to 0
        """
        self.start_time = datetime.now()
        self.cycles_completed = 0
        self.expeditions_attempted = 0
        self.expeditions_sent = 0
        self.expeditions_received = 0
        self.pvp_attempted = 0
        self.pvp_done = 0
        self.combat_attempted = 0
        self.combat_done = 0
        self.resupplies_done = 0
        self.repairs_done = 0
        self.ships_switched = 0
        self.buckets_used = 0
        self.quests_checked = 0
        self.quests_started = 0
        self.quests_finished = 0
        self.recoveries = 0

    def _pretty_timedelta(self, delta):
        """Generate a human-readable time delta representation of how long the
        script has been running. Prettify code taken from:
        https://stackoverflow.com/q/538666

        Args:
            delta (timedelta): timedelta representation of current time minus
                the script start time

        Returns:
            str: human-readable representation of timedelta
        """

        pretty_string = "{} days ".format(delta.days) if delta.days else ""
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        pretty_string += "{} hours {} minutes".format(
            hours, minutes, seconds)
        return pretty_string

    def _pretty_perhour(self, count, hours):
        """Generate a sensible count and count-per-hour string representation,
        returning just the count if the hours count is below 1 or count is 0.

        Args:
            count (int): total count
            hours (float): total hours to calculate count-per-hour with

        Returns:
            str: count and human-readable representation of count-per-hour if
                hours < 1 or count is 0
        """
        if hours < 1 or count == 0:
            return count
        return "{} ({:0.2f}/hr)".format(count, count / hours)

    def print_stats(self):
        """Prints a summary of all the stats to console.
        """
        delta = datetime.now() - self.start_time
        hours = delta.total_seconds() / 3600

        if self.config.expeditions['enabled']:
            Util.log_success(
                "Expeditions sent: {} / received: {}".format(
                    self._pretty_perhour(self.expeditions_sent, hours),
                    self._pretty_perhour(self.expeditions_received, hours)))
        else:
            Util.log_success(
                "Expeditions received: {}".format(self.expeditions_received))

        if self.config.pvp['enabled']:
            Util.log_success("PvPs done: {}".format(
                self._pretty_perhour(self.pvp_done, hours)))

        if self.config.combat['enabled']:
            Util.log_success("Combat done: {} / attempted: {}".format(
                self._pretty_perhour(self.combat_done, hours),
                self._pretty_perhour(self.combat_attempted, hours)))

        if self.config.ship_switcher['enabled']:
            Util.log_success("Ships switched: {}".format(
                self._pretty_perhour(self.ships_switched, hours)))

        if self.config.quests['enabled']:
            Util.log_success(
                "Quests started: {} / finished: {}".format(
                    self._pretty_perhour(self.quests_started, hours),
                    self._pretty_perhour(self.quests_finished, hours)))

        Util.log_success("Resupplies: {} || Repairs: {} || Buckets: {}".format(
            self._pretty_perhour(self.resupplies_done, hours),
            self._pretty_perhour(self.repairs_done, hours),
            self._pretty_perhour(self.buckets_used, hours)))

        Util.log_success("Recoveries done: {}".format(self.recoveries))

        Util.log_success(
            "kcauto has been running for {} (started on {})".format(
                self._pretty_timedelta(delta),
                self.start_time.strftime('%Y-%m-%d %H:%M:%S')))

    def increment_cycles_completed(self):
        self.cycles_completed += 1

    def increment_expeditions_attempted(self):
        self.expeditions_attempted += 1

    def increment_expeditions_sent(self):
        self.expeditions_sent += 1

    def increment_expeditions_received(self):
        self.expeditions_received += 1

    def increment_pvp_attempted(self):
        self.pvp_attempted += 1

    def increment_pvp_done(self):
        self.pvp_done += 1

    def increment_combat_attempted(self):
        self.combat_attempted += 1

    def increment_combat_done(self):
        self.combat_done += 1

    def increment_resupplies_done(self):
        self.resupplies_done += 1

    def increment_repairs_done(self):
        self.repairs_done += 1

    def increment_buckets_used(self):
        self.buckets_used += 1

    def increment_ships_switched(self):
        self.ships_switched += 1

    def increment_quests_checked(self):
        self.quests_checked += 1

    def increment_quests_started(self):
        self.quests_started += 1

    def increment_quests_finished(self):
        self.quests_finished += 1

    def increment_recoveries(self):
        self.recoveries += 1
