from datetime import datetime
from sys import exit

import combat.combat_core as com
import config.config_core as cfg
import expedition.expedition_core as exp
import pvp.pvp_core as pvp
import ships.ships_core as shp
from kca_enums.scheduler_slots import (
    SchedulerSlot0Enum, SchedulerSlot2Enum, SchedulerSlot3Enum)
from scheduler.schedule_rule import ScheduleRule
from util.kc_time import KCTime
from util.logger import Log


class SchedulerCore(object):
    rules = []
    stop_timers = []
    wake_timers = []
    run_thresholds = []
    misc_rules = []
    kca_active = True

    def __init__(self):
        Log.log_debug("Initializing scheduler core.")
        self.update_from_config()

    def update_from_config(self):
        self.rules = []
        self.stop_timers = []
        self.wake_timers = []
        self.run_thresholds = []
        self.misc_rules = []
        self._intake_rules(cfg.config.scheduler.rules)
        self._set_initial_timers_and_thresholds()
        self._set_misc_rules()

    def _intake_rules(self, rules):
        for rule in rules:
            self.rules.append(ScheduleRule(rule))

    def _set_initial_timers_and_thresholds(self):
        for rule in self.rules:
            if rule.next_action_time:
                self.stop_timers.append((rule.next_action_time, rule))
            elif rule.condition_runs:
                import stats.stats_core as sts
                if rule.condition_type is SchedulerSlot0Enum.SORTIES_RUN:
                    run = sts.stats.combat.combat_sorties
                elif rule.condition_type is SchedulerSlot0Enum.EXPEDITIONS_RUN:
                    run = sts.stats.expedition.expeditions_received
                elif rule.condition_type is SchedulerSlot0Enum.PVP_RUN:
                    run = sts.stats.pvp.pvp_done
                run += rule.condition_runs
                self.run_thresholds.append((run, rule))

    def _set_misc_rules(self):
        for rule in self.rules:
            if rule.condition_type in (
                    SchedulerSlot0Enum.RESCUE, SchedulerSlot0Enum.DOCKS_FULL,
                    SchedulerSlot0Enum.CLEAR_STOP):
                self.misc_rules.append(rule)

    def check_and_process_rules(self):
        self._check_and_process_stop_timers()
        self._check_and_process_thresholds()
        self._check_and_process_misc_rules()
        self._check_and_process_wake_timers()

    def _check_and_process_stop_timers(self):
        new_stop_timers = []
        for timer_tuple in self.stop_timers:
            time = timer_tuple[0]
            rule = timer_tuple[1]
            if datetime.now() > time:
                if rule.action is SchedulerSlot2Enum.STOP:
                    if rule.condition_type is SchedulerSlot0Enum.TIME:
                        Log.log_msg(
                            f"Stopping {rule.action_module.display_name} "
                            f" module at local time "
                            f"~{rule.condition_time[0]:02}:"
                            f"{rule.condition_time[1]:02}.")
                    elif rule.condition_type is SchedulerSlot0Enum.TIME_RUN:
                        Log.log_msg(
                            f"Stopping {rule.action_module.display_name} "
                            f" module after running for "
                            f"~{rule.condition_time[0]:02}:"
                            f"{rule.condition_time[1]:02}.")
                if rule.action is SchedulerSlot2Enum.SLEEP:
                    wake_time = rule.next_wake_time
                    if rule.condition_type is SchedulerSlot0Enum.TIME:
                        Log.log_msg(
                            f"Sleeping {rule.action_module.display_name} "
                            f"module at local time "
                            f"~{rule.condition_time[0]:02}:"
                            f"{rule.condition_time[1]:02} for "
                            f"~{rule.action_length[0]:02}:"
                            f"{rule.action_length[1]:02}. Waking at "
                            f"{KCTime.datetime_to_str(wake_time)}.")
                    elif rule.condition_type is SchedulerSlot0Enum.TIME_RUN:
                        Log.log_msg(
                            f"Sleeping {rule.action_module.display_name} "
                            f"module after running for "
                            f"~{rule.condition_time[0]:02}:"
                            f"{rule.condition_time[1]:02} for "
                            f"~{rule.action_length[0]:02}:"
                            f"{rule.action_length[1]:02}. Waking at "
                            f"{KCTime.datetime_to_str(wake_time)}.")
                    self.wake_timers.append((wake_time, rule))
                self._set_module_enabled_state(rule, False)
            else:
                new_stop_timers.append(timer_tuple)
        self.stop_timers = new_stop_timers

    def _check_and_process_thresholds(self):
        new_run_thresholds = []
        for threshold_tuple in self.run_thresholds:
            import stats.stats_core as sts
            threshold = threshold_tuple[0]
            rule = threshold_tuple[1]
            if (
                    (rule.condition_type is SchedulerSlot0Enum.SORTIES_RUN
                        and sts.stats.combat.combat_sorties >= threshold)
                    or (rule.condition_type
                        is SchedulerSlot0Enum.EXPEDITIONS_RUN
                        and sts.stats.expedition.expeditions_received
                        >= threshold)
                    or (rule.condition_type is SchedulerSlot0Enum.PVP_RUN
                        and sts.stats.pvp.pvp_done >= threshold)):
                self._set_module_enabled_state(rule, False)
            else:
                new_run_thresholds.append(threshold_tuple)
        self.run_thresholds = new_run_thresholds

    def _check_and_process_misc_rules(self):
        for rule in self.misc_rules:
            if rule.condition_type is SchedulerSlot0Enum.RESCUE:
                for ship in com.combat.rescued_ships:
                    if ship.sortno == rule.condition_rescue:
                        Log.log_success(
                            f"Ship {ship.name} (#{ship.sortno}) rescued. "
                            "Executing scheduler rule.")
                        self._set_module_enabled_state(rule, False)
                        break
            elif rule.condition_type is SchedulerSlot0Enum.DOCKS_FULL:
                if shp.ships.current_ship_count == shp.ships.max_ship_count:
                    Log.log_success("Port is full. Executing Scheduler rule.")
                    self._set_module_enabled_state(rule, False)
            elif rule.condition_type is SchedulerSlot0Enum.CLEAR_STOP:
                if com.combat.map_cleared:
                    Log.log_success(
                        "Sortie map cleared. Executing Scheduler rule.")
                    self._set_module_enabled_state(rule, False)

    def _check_and_process_wake_timers(self):
        new_wake_timers = []
        for timer_tuple in self.wake_timers:
            time = timer_tuple[0]
            rule = timer_tuple[1]
            if datetime.now() > time:
                if rule.action is SchedulerSlot2Enum.SLEEP:
                    if rule.condition_type is SchedulerSlot0Enum.TIME:
                        Log.log_msg(
                            f"Waking {rule.action_module.display_name} module "
                            f"after sleeping for ~{rule.action_length[0]:02}:"
                            f"{rule.action_length[1]:02}.")
                    elif rule.condition_type is SchedulerSlot0Enum.TIME_RUN:
                        Log.log_msg(
                            f"Waking {rule.action_module.display_name} module "
                            f"after sleeping for ~{rule.action_length[0]:02}:"
                            f"{rule.action_length[1]:02}.")
                    self.stop_timers.append((rule.next_action_time, rule))
                self._set_module_enabled_state(rule, True)
            else:
                new_wake_timers.append(timer_tuple)
        self.wake_timers = new_wake_timers

    def _set_module_enabled_state(self, rule, state):
        module = rule.action_module
        if module is SchedulerSlot3Enum.COMBAT_MODULE:
            com.combat.enabled = state
        elif module is SchedulerSlot3Enum.EXPEDITION_MODULE:
            exp.expedition.enabled = state
        elif module is SchedulerSlot3Enum.PVP_MODULE:
            pvp.pvp.enabled = state
        elif module is SchedulerSlot3Enum.KCAUTO:
            if rule.action is SchedulerSlot2Enum.STOP:
                Log.log_success("Stopping kcauto based on scheduler rule.")
                exit(0)
            elif rule.action is SchedulerSlot2Enum.SLEEP:
                if state is True:
                    Log.log_success("Waking kcauto.")
                self.kca_active = state


scheduler = SchedulerCore()
