from datetime import datetime

import args.args_core as arg
import config.config_core as cfg
import fleet.fleet_core as flt
import util.click_tracker as clt
from stats.combat import CombatStats
from stats.expedition import ExpeditionStats
from stats.pvp import PvPStats
from stats.quest import QuestStats
from stats.rsc import ResourceStats
from stats.recovery import RecoveryStats
from stats.resupply import ResupplyStats
from stats.repair import RepairStats
from stats.ships_switcher import ShipSwitcherStats
from util.kc_time import KCTime
from util.logger import Log


class Stats(object):
    print_loop_end_stats = True
    start_time = None
    loop_count = None
    combat = None
    expedition = None
    pvp = None
    ship_switcher = None
    resupply = None
    repair = None
    quest = None
    recovery = None
    rsc = None
    max_equip_count = 0
    current_equip_count = 0

    def __init__(self):
        self.start_time = datetime.now()
        self.loop_count = 0
        self.combat = CombatStats(self.start_time)
        self.expedition = ExpeditionStats(self.start_time)
        self.pvp = PvPStats(self.start_time)
        self.ship_switcher = ShipSwitcherStats(self.start_time)
        self.resupply = ResupplyStats(self.start_time)
        self.repair = RepairStats(self.start_time)
        self.quest = QuestStats(self.start_time)
        self.recovery = RecoveryStats(self.start_time)
        self.rsc = ResourceStats(self.start_time)
        Log.log_debug("Stats module initialized.")

    def set_print_loop_end_stats(self, value=True):
        self.print_loop_end_stats = value

    def print_stats(self):
        Log.log_success(
            "kcauto has been running for "
            f"{KCTime.timedelta_to_str(datetime.now() - self.start_time)}"
            f" (loop {self.loop_count}).")
        if cfg.config.combat.enabled:
            Log.log_success(self.combat)
        if cfg.config.pvp.enabled:
            Log.log_success(self.pvp)
        if cfg.config.expedition.enabled:
            Log.log_success(self.expedition)

        if cfg.config.combat.enabled:
            for fleet in flt.fleets.combat_fleets:
                Log.log_success(fleet)
        if cfg.config.expedition.enabled:
            for fleet in flt.fleets.expedition_fleets:
                Log.log_success(fleet)

        if cfg.config.ship_switcher.enabled:
            Log.log_success(self.ship_switcher)

        if self.resupply.resupplies_done > 0:
            Log.log_success(self.resupply)

        if self.repair.repairs_done > 0:
            Log.log_success(self.repair)

        if cfg.config.quest.enabled:
            Log.log_success(self.quest)

        if cfg.config.scheduler.enabled:
            import scheduler.scheduler_core as sch
            Log.log_success("Active Scheduler rules:")
            for sleep_tuple in sch.scheduler.stop_timers:
                Log.log_success(
                    f"- {sleep_tuple[1]} at "
                    f"{KCTime.datetime_to_str(sleep_tuple[0])}")
            for wake_tuple in sch.scheduler.wake_timers:
                Log.log_success(
                    f"- {wake_tuple[1]} until "
                    f"{KCTime.datetime_to_str(wake_tuple[0])}")
            for run_tuple in sch.scheduler.run_thresholds:
                Log.log_success(f"- {run_tuple[1]}")
            for rule_tuple in sch.scheduler.misc_rules:
                Log.log_success(f"- {rule_tuple}")

        if self.recovery.recoveries_done > 0:
            Log.log_success(self.recovery)

        Log.log_success(self.rsc)

        if not arg.args.parsed_args.no_click_track:
            clt.click_tracker.export()

        self.print_loop_end_stats = False


stats = Stats()
