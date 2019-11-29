import config.config_core as cfg
from stats.stats_base import StatsBase
from util.logger import Log


class ResupplyStats(StatsBase):
    resupplies_done = 0
    provisional_resupplies_done = 0

    def __init__(self, start_time):
        super().__init__(start_time)
        Log.log_debug("Resupply Stats module initialized.")

    @property
    def resupplies_done_ph(self):
        return self.resupplies_done / self.hours_run

    @property
    def provisional_resupplies_done_ph(self):
        return self.provisional_resupplies_done / self.hours_run

    def __str__(self):
        return_string = (
            f"{self.resupplies_done} resupplies done "
            f"({self.resupplies_done_ph:.2f}/hr)")

        if cfg.config.expedition.enabled:
            return_string += (
                f" / {self.provisional_resupplies_done} provisional "
                "resupplies done "
                f"({self.provisional_resupplies_done_ph:.2f}/hr)")

        return return_string
