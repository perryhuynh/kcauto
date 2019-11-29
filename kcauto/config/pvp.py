from config.config_base import ConfigBase
from kca_enums.fleet_modes import CombinedFleetModeEnum
from constants import MAX_FLEET_PRESETS


class ConfigPvP(ConfigBase):
    _enabled = False
    _fleet_preset = None

    def __init__(self, config):
        super().__init__(config)
        self.enabled = config['pvp.enabled']
        self.fleet_preset = config['pvp.fleet_preset']

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if type(value) is not bool:
            raise ValueError(
                "Specified value for pvp enabled is not a boolean.")
        if (
                self._config['pvp.enabled']
                and self._config['combat.enabled']
                and CombinedFleetModeEnum.contains_value(
                    self._config['combat.fleet_mode'])):
            raise ValueError("Cannot enable PvP when combat fleet is combined")
        self._enabled = value

    @property
    def fleet_preset(self):
        return self._fleet_preset

    @fleet_preset.setter
    def fleet_preset(self, value):
        if not value:
            self._fleet_preset = None
        else:
            if not 0 < value <= MAX_FLEET_PRESETS:
                raise ValueError("Invalid value specified for fleet preset")
            self._fleet_preset = value
