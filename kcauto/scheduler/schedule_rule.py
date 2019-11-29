from datetime import datetime, timedelta
from random import randint

from kca_enums.scheduler_slots import (
    SchedulerSlot0Enum, SchedulerSlot2Enum, SchedulerSlot3Enum)


class ScheduleRule(object):
    condition_type = None
    condition_time = None
    condition_runs = None
    condition_rescue = None
    action = None
    action_module = None
    action_length = None

    def __init__(self, rule_string):
        split_rule = rule_string.split(':')
        self.condition_type = SchedulerSlot0Enum(split_rule[0])
        if self.condition_type in (
                SchedulerSlot0Enum.TIME, SchedulerSlot0Enum.TIME_RUN):
            self.condition_time = (
                int(split_rule[1][0:2]), int(split_rule[1][2:4]))
        elif self.condition_type in (
                SchedulerSlot0Enum.SORTIES_RUN,
                SchedulerSlot0Enum.EXPEDITIONS_RUN,
                SchedulerSlot0Enum.PVP_RUN):
            self.condition_runs = int(split_rule[1])
        elif self.condition_type is SchedulerSlot0Enum.RESCUE:
            self.condition_rescue = int(split_rule[1])
        elif self.condition_type in (
                SchedulerSlot0Enum.DOCKS_FULL, SchedulerSlot0Enum.CLEAR_STOP):
            pass
        self.action = SchedulerSlot2Enum(split_rule[2])
        self.action_module = SchedulerSlot3Enum(split_rule[3])
        if self.action == SchedulerSlot2Enum.SLEEP:
            self.action_length = (
                int(split_rule[4][0:2]), int(split_rule[4][2:4]))

    @property
    def next_action_time(self):
        dt = None
        if self.condition_type is SchedulerSlot0Enum.TIME:
            dt = datetime.now().replace(
                hour=self.condition_time[0],
                minute=self.condition_time[1]
            ) + timedelta(minutes=randint(0, 15))
            if dt < datetime.now():
                dt += timedelta(days=1)
        elif self.condition_type is SchedulerSlot0Enum.TIME_RUN:
            dt = datetime.now() + timedelta(
                hours=self.condition_time[0],
                minutes=self.condition_time[1] + randint(0, 15))
        return dt

    @property
    def next_wake_time(self):
        dt = None
        if self.action_length:
            dt = datetime.now() + timedelta(
                hours=self.action_length[0],
                minutes=self.action_length[1] + randint(0, 15))
        return dt

    def __str__(self):
        ret_string = (
            f"{self.action.display_name} {self.action_module.display_name}")
        if self.action is SchedulerSlot2Enum.SLEEP:
            ret_string += (
                f" for ~{self.action_length[0]:02}:{self.action_length[1]:02}")

        if self.condition_type in (
                SchedulerSlot0Enum.SORTIES_RUN,
                SchedulerSlot0Enum.EXPEDITIONS_RUN,
                SchedulerSlot0Enum.PVP_RUN):
            ret_string += (
                f" after {self.condition_runs} "
                f"{self.condition_type.display_name}")
        elif self.condition_type is SchedulerSlot0Enum.RESCUE:
            import ships.ships_core as shp
            ship = shp.ships.get_ship_from_sortno(self.condition_rescue)
            ret_string += f" after rescuing {ship.name} (#{ship.sortno})"
        elif self.condition_type is SchedulerSlot0Enum.DOCKS_FULL:
            ret_string += f" after port is full"
        elif self.condition_type is SchedulerSlot0Enum.CLEAR_STOP:
            ret_string += f" after clearing map"

        ret_string += "."

        return ret_string
