import config.config_core as cfg
from stats.stats_base import StatsBase
from util.logger import Log


class RepairStats(StatsBase):
    repairs_done = 0
    buckets_used = 0
    passive_repairs_done = 0

    def __init__(self, start_time):
        super().__init__(start_time)
        Log.log_debug("Repair Stats module initialized.")

    @property
    def repairs_done_ph(self):
        return self.repairs_done / self.hours_run

    @property
    def buckets_used_ph(self):
        return self.buckets_used / self.hours_run

    @property
    def passive_repairs_done_ph(self):
        return self.passive_repairs_done / self.hours_run

    def __str__(self):
        return_string = (
            f"{self.repairs_done} repairs done "
            f"({self.repairs_done_ph:.2f}/hr) "
            f"/ {self.buckets_used} buckets used "
            f"({self.buckets_used_ph:.2f}/hr)")

        if cfg.config.passive_repair.enabled:
            return_string += (
                f" / {self.passive_repairs_done} passive repairs done "
                f"({self.passive_repairs_done_ph:.2f}/hr)")

        return return_string
