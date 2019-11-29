from stats.stats_base import StatsBase
from util.logger import Log


class ShipSwitcherStats(StatsBase):
    ships_switched = 0

    def __init__(self, start_time):
        super().__init__(start_time)
        Log.log_debug("Ship Switcher Stats module initialized.")

    @property
    def ships_switched_ph(self):
        return self.ships_switched / self.hours_run

    def __str__(self):
        return (
            f"{self.ships_switched} ships switched "
            f"({self.ships_switched_ph:.2f}/hr)")
