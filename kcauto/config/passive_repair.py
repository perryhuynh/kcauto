from config.config_base import ConfigBase
from kca_enums.damage_states import DamageStateEnum


class ConfigPassiveRepair(ConfigBase):
    _enabled = False
    _repair_threshold = 0
    _slots_to_reserve = 0

    def __init__(self, config):
        super().__init__(config)
        self.enabled = config['passive_repair.enabled']
        self.repair_threshold = config['passive_repair.repair_threshold']
        self.slots_to_reserve = config['passive_repair.slots_to_reserve']

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if type(value) is not bool:
            raise ValueError(
                "Specified value for repair passive enabled is not a boolean.")
        self._enabled = value

    @property
    def repair_threshold(self):
        return self._repair_threshold

    @repair_threshold.setter
    def repair_threshold(self, value):
        if not DamageStateEnum.contains_value(value):
            raise ValueError("Invalid Dmaage State")
        self._repair_threshold = DamageStateEnum(value)

    @property
    def slots_to_reserve(self):
        return self._slots_to_reserve

    @slots_to_reserve.setter
    def slots_to_reserve(self, value):
        if not 0 <= value <= 3:
            raise ValueError("Invalid number of slots to reserve")
        self._slots_to_reserve = value
