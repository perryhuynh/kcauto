from config.config_base import ConfigBase
from kca_enums.event_difficulties import EventDifficultyEnum


class ConfigEventReset(ConfigBase):
    _enabled = None
    _frequency = None
    _reset_difficulty = None
    _farm_difficulty = None

    def __init__(self, config):
        super().__init__(config)
        self.enabled = config['event_reset.enabled']
        self.frequency = config['event_reset.frequency']
        self.reset_difficulty = config['event_reset.reset_difficulty']
        self.farm_difficulty = config['event_reset.farm_difficulty']

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if type(value) is not bool:
            raise ValueError(
                "Specified value for event reset enabled is not a boolean.")
        self._enabled = value

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        if type(value) is not int:
            raise ValueError("Frequency is not a number.")
        self._frequency = value

    @property
    def reset_difficulty(self):
        return self._reset_difficulty

    @reset_difficulty.setter
    def reset_difficulty(self, value):
        if not EventDifficultyEnum.contains_value(value):
            raise ValueError("Invalid difficulty specified")
        self._reset_difficulty = EventDifficultyEnum(value)

    @property
    def farm_difficulty(self):
        return self._farm_difficulty

    @farm_difficulty.setter
    def farm_difficulty(self, value):
        if not EventDifficultyEnum.contains_value(value):
            raise ValueError("Invalid difficulty specified")
        self._farm_difficulty = EventDifficultyEnum(value)
