from stats.stats_base import StatsBase
from util.logger import Log


class RecoveryStats(StatsBase):
    recoveries_done = 0
    basic_recoveries_done = 0
    results_recoveries_done = 0
    catbomb_recoveries_done = 0
    catbomb_201_recoveries_done = 0
    catbomb_201_encountered = 0
    chrome_crash_t1_recoveries_done = 0
    chrome_crash_t2_recoveries_done = 0

    def __init__(self, start_time):
        super().__init__(start_time)
        Log.log_debug("Recovery Stats module initialized.")

    @property
    def recoveries_done_ph(self):
        return self.recoveries_done / self.hours_run

    @property
    def basic_recoveries_done_ph(self):
        return self.basic_recoveries_done / self.hours_run

    @property
    def results_recoveries_done_ph(self):
        return self.results_recoveries_done / self.hours_run

    @property
    def catbomb_recoveries_done_ph(self):
        return self.catbomb_recoveries_done / self.hours_run

    @property
    def catbomb_201_recoveries_done_ph(self):
        return self.catbomb_201_recoveries_done / self.hours_run

    @property
    def chrome_crash_t1_recoveries_done_ph(self):
        return self.chrome_crash_t1_recoveries_done / self.hours_run

    @property
    def chrome_crash_t2_recoveries_done_ph(self):
        return self.chrome_crash_t2_recoveries_done / self.hours_run

    def __str__(self):
        return_string = (
            f"{self.recoveries_done} Recoveries done "
            f"{self.recoveries_done_ph:.2f}/hr)")
        string_list = []
        if self.basic_recoveries_done:
            string_list.append(
                f"{self.basic_recoveries_done} Basic Recoveries "
                f"({self.basic_recoveries_done_ph:.2f}/hr)")
        if self.results_recoveries_done:
            string_list.append(
                f"{self.results_recoveries_done} Results Recoveries "
                f"({self.results_recoveries_done_ph:.2f}/hr)")
        if self.catbomb_recoveries_done:
            string_list.append(
                f"{self.catbomb_recoveries_done} Catbomb Recoveries "
                f"({self.catbomb_recoveries_done_ph:.2f}/hr)")
        if self.catbomb_201_recoveries_done:
            string_list.append(
                f"{self.catbomb_201_recoveries_done} 201 Recoveries "
                f"({self.catbomb_201_recoveries_done_ph:.2f}/hr)")
        if self.chrome_crash_t1_recoveries_done:
            string_list.append(
                f"{self.chrome_crash_t1_recoveries_done} "
                "Chrome Crash (Type 1) "
                f"({self.chrome_crash_t1_recoveries_done_ph:.2f}/hr)")
        if self.chrome_crash_t2_recoveries_done:
            string_list.append(
                f"{self.chrome_crash_t2_recoveries_done} "
                "Chrome Crash (Type 2) "
                f"({self.chrome_crash_t2_recoveries_done_ph:.2f}/hr)")

        return return_string + ' / ' + ' / '.join(string_list)
