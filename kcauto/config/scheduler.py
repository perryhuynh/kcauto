from config.config_base import ConfigBase

from kca_enums.scheduler_slots import (
    SchedulerSlot0Enum, SchedulerSlot2Enum, SchedulerSlot3Enum)


class ConfigScheduler(ConfigBase):
    _rules = []

    def __init__(self, config):
        super().__init__(config)
        self.enabled = config['scheduler.enabled']
        self.rules = config['scheduler.rules']

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if type(value) is not bool:
            raise ValueError(
                "Specified value for scheduler enabled is not a boolean.")
        self._enabled = value

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, value):
        for rule in value:
            split_rule = rule.split(':')
            if len(split_rule) not in (4, 5):
                raise ValueError("Malformed Scheduler rule.")
            if not SchedulerSlot0Enum.contains_value(split_rule[0]):
                raise ValueError("Invalid rule conditional type.")
            if not SchedulerSlot2Enum.contains_value(split_rule[2]):
                raise ValueError("Invalid rule action.")
            if not SchedulerSlot3Enum.contains_value(split_rule[3]):
                raise ValueError("Invalid rule action module.")
        self._rules = value
