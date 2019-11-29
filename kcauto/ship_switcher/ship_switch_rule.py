import operator

import fleet.fleet_core as flt
import repair.repair_core as rep
from kca_enums.damage_states import DamageStateEnum
from kca_enums.ship_switcher_slots import (
    ShipSwitcherConditionSlot0Enum, ShipSwitcherCriteriaSlot0Enum,
    ShipSwitcherOperatorEnum, ShipSwitcherCriteriaSlot8Enum,
    ShipSwitcherCriteriaSlot9Enum)
from kca_enums.ship_types import ShipTypeEnum
from util.logger import Log


class ShipSwitchRule(object):
    slot_id = None
    conditions = []
    criteria = []

    def __init__(self, slot_id, rule_string):
        self.slot_id = slot_id
        split_rule = rule_string.split('|')
        conditions = split_rule[0]
        criteria = split_rule[1]

        split_conditions = conditions.split(',')
        for condition in split_conditions:
            split_cond = condition.split(':')
            split_cond[0] = ShipSwitcherConditionSlot0Enum(split_cond[0])
            if split_cond[1]:
                split_cond[1] = ShipSwitcherOperatorEnum(split_cond[1])
            if split_cond[0] is ShipSwitcherConditionSlot0Enum.LEVEL:
                split_cond[2] = int(split_cond[2])
            elif split_cond[0] is ShipSwitcherConditionSlot0Enum.DAMAGE:
                split_cond[2] = DamageStateEnum(int(split_cond[2]))
            elif split_cond[0] is ShipSwitcherConditionSlot0Enum.MORALE:
                split_cond[2] = int(split_cond[2])
            self.conditions.append(split_cond)

        split_criteria = criteria.split(',')
        for criterion in split_criteria:
            split_crit = criterion.split(':')
            split_crit[0] = ShipSwitcherCriteriaSlot0Enum(split_crit[0])
            if split_crit[0] is ShipSwitcherCriteriaSlot0Enum.SHIP:
                split_crit[1] = int(split_crit[1])
            elif split_crit[0] is ShipSwitcherCriteriaSlot0Enum.CLASS:
                split_crit[1] = ShipTypeEnum(int(split_crit[1]))
            if split_crit[2]:
                split_crit[2] = ShipSwitcherOperatorEnum(split_crit[2])
            if split_crit[3]:
                split_crit[3] = int(split_crit[3])
            if split_crit[4]:
                split_crit[4] = ShipSwitcherOperatorEnum(split_crit[4])
            if split_crit[5]:
                split_crit[5] = DamageStateEnum(int(split_crit[5]))
            if split_crit[6]:
                split_crit[6] = ShipSwitcherOperatorEnum(split_crit[6])
            if split_crit[7]:
                split_crit[7] = int(split_crit[7])
            if split_crit[8]:
                split_crit[8] = ShipSwitcherCriteriaSlot8Enum(split_crit[8])
            if split_crit[9]:
                split_crit[9] = ShipSwitcherCriteriaSlot9Enum(split_crit[9])
            self.criteria.append(split_crit)

    @property
    def ship_in_slot(self):
        if len(flt.fleets.fleets[1].ship_data) < self.slot_id:
            raise ValueError(
                f"Slot {self.slot_id} is empty in first fleet. Please "
                "pre-fill slots with Ship Switcher rules.")
        return flt.fleets.fleets[1].ship_data[self.slot_id - 1]

    def need_to_switch(self):
        slot_ship = self.ship_in_slot

        for condition in self.conditions:
            op = self._get_operator(condition[1])

            if condition[0] is ShipSwitcherConditionSlot0Enum.LEVEL:
                if op(slot_ship.level, condition[2]):
                    Log.log_debug(
                        f"{slot_ship.name} in Slot {self.slot_id} has met "
                        "level threshold to be switched out.")
                    return True
            elif condition[0] is ShipSwitcherConditionSlot0Enum.DAMAGE:
                if op(slot_ship.damage, condition[2]):
                    Log.log_debug(
                        f"{slot_ship.name} in Slot {self.slot_id} has met "
                        "damage threshold to be switched out.")
                    return True
            elif condition[0] is ShipSwitcherConditionSlot0Enum.MORALE:
                if op(slot_ship.morale, condition[2]):
                    Log.log_debug(
                        f"{slot_ship.name} in Slot {self.slot_id} has met "
                        "morale threshold to be switched out.")
                    return True
        return False

    def ship_meets_criteria(self, ship):
        if ship.local_id in flt.fleets.ships_in_fleets:
            return False
        if ship.local_id in rep.repair.ships_under_repair:
            return False
        for criterion in self.criteria:
            if criterion[0] is ShipSwitcherCriteriaSlot0Enum.SHIP:
                if not ship.sortno == criterion[1]:
                    continue
            elif criterion[0] is ShipSwitcherCriteriaSlot0Enum.CLASS:
                if not ship.ship_type == criterion[1]:
                    continue
            if criterion[2] and criterion[3]:
                op = self._get_operator(criterion[2])
                if not op(ship.level, criterion[3]):
                    continue
            if criterion[4] and criterion[5]:
                op = self._get_operator(criterion[4])
                if not op(ship.damage, criterion[5]):
                    continue
            if criterion[6] and criterion[7]:
                op = self._get_operator(criterion[6])
                if not op(ship.morale, criterion[7]):
                    continue
            if criterion[8]:
                if (
                        criterion[8] is ShipSwitcherCriteriaSlot8Enum.LOCKED
                        and not ship.locked):
                    continue
                elif (
                        criterion[8] is ShipSwitcherCriteriaSlot8Enum.LOCKED
                        and ship.locked):
                    continue
            if criterion[9]:
                if (
                        criterion[9] is ShipSwitcherCriteriaSlot9Enum.RINGED
                        and not ship.ringed):
                    continue
                elif (
                        criterion[9]
                        is ShipSwitcherCriteriaSlot9Enum.NOT_RINGED
                        and ship.ringed):
                    continue
            Log.log_msg(f"{ship.name} meets switch-in criteria.")
            return True
        return False

    def _get_operator(self, op_string):
        if op_string is ShipSwitcherOperatorEnum.LT:
            return operator.lt
        elif op_string is ShipSwitcherOperatorEnum.GT:
            return operator.gt
        elif op_string is ShipSwitcherOperatorEnum.LE:
            return operator.le
        elif op_string is ShipSwitcherOperatorEnum.GE:
            return operator.ge
        elif op_string is ShipSwitcherOperatorEnum.EQ:
            return operator.eq
        elif op_string is ShipSwitcherOperatorEnum.NE:
            return operator.ne
