import config.config_core as cfg
import expedition.expedition_core as exp
from stats.stats_base import StatsBase
from util.logger import Log


class ExpeditionStats(StatsBase):
    expeditions_sent = 0
    expeditions_received = 0

    def __init__(self, start_time):
        super().__init__(start_time)
        Log.log_debug("Expedition Stats module initialized.")

    @property
    def expeditions_sent_ph(self):
        return self.expeditions_sent / self.hours_run

    @property
    def expeditions_received_ph(self):
        return self.expeditions_received / self.hours_run

    def __str__(self):
        return_string = ""

        if cfg.config.expedition.enabled:
            if not exp.expedition.enabled:
                return_string = "Expedition module is disabled. / "
            return_string += (
                f"{self.expeditions_sent} Expeditions sent "
                f"({self.expeditions_sent_ph:.2f}/hr) / "
                f"{self.expeditions_received} Expeditions received "
                f"({self.expeditions_received_ph:.2f}/hr)")

        return return_string
