import config.config_core as cfg
import pvp.pvp_core as pvp
from stats.stats_base import StatsBase
from util.kc_time import KCTime
from util.logger import Log


class PvPStats(StatsBase):
    pvp_done = 0

    def __init__(self, start_time):
        super().__init__(start_time)
        Log.log_debug("PvP Stats module initialized.")

    @property
    def pvp_done_ph(self):
        return self.pvp_done / self.hours_run

    def __str__(self):
        if cfg.config.pvp.enabled:
            if pvp.pvp.enabled:
                return_string = (
                    "Next PvP at "
                    f"{KCTime.datetime_to_str(pvp.pvp.next_pvp_time)}")
            else:
                time_disabled = pvp.pvp.time_disabled
                if time_disabled:
                    return_string = (
                        f"PvP module disabled as of "
                        f"{KCTime.datetime_to_str(time_disabled)}")

            return_string += (
                f" / {self.pvp_done} PvPs done ({self.pvp_done_ph:.2f}/hr)")
        else:
            return_string = "PvP module is disabled."

        return return_string
