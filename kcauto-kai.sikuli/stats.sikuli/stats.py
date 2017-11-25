from util import Util


class Stats(object):
    def __init__(self, config):
        """Initializes the Stats module.

        Args:
            config (Config): kcauto-kai Config instance
        """
        self.reset_stats()
        self.config = config

    def reset_stats(self):
        """Resets all stats to 0
        """
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
        self.buckets_used = 0
        self.quests_checked = 0
        self.quests_started = 0
        self.quests_finished = 0
        self.recoveries = 0

    def print_stats(self):
        """Prints a summary of all the stats to console.
        """
        if self.config.expeditions['enabled']:
            Util.log_success(
                "Expeditions sent: {} / received: {}".format(
                    self.expeditions_sent, self.expeditions_received))
        else:
            Util.log_success(
                "Expeditions received: {}".format(self.expeditions_received))

        if self.config.pvp['enabled']:
            Util.log_success("PvPs done: {}".format(self.pvp_done))

        if self.config.combat['enabled']:
            Util.log_success("Combat done: {} / attempted: {}".format(
                self.combat_done, self.combat_attempted))

        if self.config.quests['enabled']:
            Util.log_success(
                "Quests started: {} / finished: {}".format(
                    self.quests_started, self.quests_finished))

        Util.log_success("Resupplies: {} || Repairs: {} || Buckets: {}".format(
            self.resupplies_done, self.repairs_done, self.buckets_used))

        Util.log_success("Recoveries done: {}".format(self.recoveries))

    def increment(self, stat):
        """UNUSED. Used to increment specific stats based on their attribute
        name. It is preferable to use the individual increment methods below.

        Args:
            stat (str): attribute name to increment
        """
        try:
            setattr(self, stat, getattr(self, stat) + 1)
        except AttributeError:
            Util.log_error("Invalid stat '{}'".format(stat))

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

    def increment_quests_checked(self):
        self.quests_checked += 1

    def increment_quests_started(self):
        self.quests_started += 1

    def increment_quests_finished(self):
        self.quests_finished += 1

    def increment_recoveries(self):
        self.recoveries += 1
