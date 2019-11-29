from config.config_base import ConfigBase


class ConfigQuest(ConfigBase):
    _enabled = False
    _quests = False

    def __init__(self, config):
        super().__init__(config)
        self.enabled = config['quest.enabled']
        self.quests = config['quest.quests']

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if type(value) is not bool:
            raise ValueError(
                "Specified value for quests enabled is not a boolean.")
        self._enabled = value

    @property
    def quests(self):
        return self._quests

    @quests.setter
    def quests(self, value):
        self._quests = value
