import config.config_core as cfg
import combat.combat_core as com
from stats.stats_base import StatsBase
from util.kc_time import KCTime
from util.logger import Log


class CombatStats(StatsBase):
    combat_sorties = 0
    nodes_fought = 0
    ships_rescued = 0
    event_resets = 0

    def __init__(self, start_time):
        super().__init__(start_time)
        Log.log_debug("Combat Stats module initialized.")

    @property
    def combat_sorties_ph(self):
        return self.combat_sorties / self.hours_run

    @property
    def nodes_fought_ph(self):
        return self.nodes_fought / self.hours_run

    @property
    def ships_rescued_ph(self):
        return self.ships_rescued / self.hours_run

    @property
    def event_resets_ph(self):
        return self.event_resets / self.hours_run

    def __str__(self):
        if cfg.config.combat.enabled:
            if com.combat.enabled:
                return_string = (
                    "Next sortie at "
                    f"{KCTime.datetime_to_str(com.combat.next_sortie_time)}")
            else:
                time_disabled = com.combat.time_disabled
                if time_disabled:
                    return_string = (
                        f"Combat module disabled as of "
                        f"{KCTime.datetime_to_str(time_disabled)}")

            return_string += (
                f" / {self.combat_sorties} sorties "
                f"({self.combat_sorties_ph:.2f}/hr) / "
                f"{self.nodes_fought} nodes fought "
                f"({self.nodes_fought_ph:.2f}/hr) / "
                f"{self.ships_rescued} ships rescued "
                f"({self.ships_rescued_ph:.2f}/hr)")
            if cfg.config.event_reset.enabled:
                return_string += (
                    f" / {self.event_resets} ({self.event_resets_ph:.2f}/hr)")
        else:
            return_string = "Combat module is disabled."

        return return_string
