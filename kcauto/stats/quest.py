import math

import config.config_core as cfg
import quest.quest_core as qst
from stats.stats_base import StatsBase
from util.kc_time import KCTime
from util.logger import Log


class QuestStats(StatsBase):
    times_checked = 0
    quests_activated = 0
    quests_deactivated = 0
    quests_turned_in = 0

    def __init__(self, start_time):
        super().__init__(start_time)
        Log.log_debug("Quest Stats module initialized.")

    @property
    def times_checked_ph(self):
        return self.times_checked / self.hours_run

    @property
    def quests_activated_ph(self):
        return self.quests_activated / self.hours_run

    @property
    def quests_deactivated_ph(self):
        return self.quests_deactivated / self.hours_run

    @property
    def quests_turned_in_ph(self):
        return self.quests_turned_in / self.hours_run

    def __str__(self):
        return_string = ""

        if cfg.config.quest.enabled:
            if qst.quest.enabled:
                intervals = qst.quest.soonest_check_intervals
                print_intervals = False
                for i in intervals:
                    if i < math.inf:
                        print_intervals = True
                        break
                if print_intervals:
                    return_string = "Next Quest check after "
                    interval_str_list = []
                    if intervals[0] < math.inf:
                        interval_str_list.append(f"Sortie#{intervals[0]}")
                    if intervals[1] < math.inf:
                        interval_str_list.append(f"PvP#{intervals[1]}")
                    if intervals[2] < math.inf:
                        interval_str_list.append(f"Expedition#{intervals[2]}")
                    return_string += "/".join(interval_str_list) + " / "
                return_string += (
                    "Quest reset at "
                    f"{KCTime.datetime_to_str(qst.quest.quest_reset_time)} ")
            else:
                return_string = "Quest module is disabled."
            return_string += (
                f" / checked {self.times_checked} times "
                f"({self.times_checked_ph:.2f}/hr) / "
                f"{self.quests_activated} Quests activated "
                f"({self.quests_activated_ph:.2f}/hr) / "
                f"{self.quests_deactivated} Quests deactivated "
                f"({self.quests_deactivated_ph:.2f}/hr) / "
                f"{self.quests_turned_in} Quests turned in "
                f"({self.quests_turned_in_ph:.2f}/hr)")

        return return_string
