from config.config_base import ConfigBase


class ConfigShipSwitcher(ConfigBase):
    _enabled = False
    _slots = {}

    def __init__(self, config):
        super().__init__(config)
        self.enabled = config['ship_switcher.enabled']
        self.slots = config['ship_switcher.slots']

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if type(value) is not bool:
            raise ValueError(
                "Specified value for ship switcher enabled is not a boolean.")
        self._enabled = value

    @property
    def slots(self):
        return self._slots

    @slots.setter
    def slots(self, value):
        slots = {}
        for slot_str in value:
            slots[int(slot_str)] = value[slot_str]
        # for rule in value:
        #     split_rule = rule.split(':')
        #     if len(split_rule) not in (4, 5):
        #         raise ValueError("Malformed Scheduler rule.")
        #     if split_rule[0] not in (
        #             'time', 'time_run', 'sorties', 'expeditions', 'pvp',
        #             'rescue', 'docks_full', 'clear_stop'):
        #         raise ValueError("Invalid rule conditional type.")
        #     if split_rule[2] not in ('stop', 'sleep'):
        #         raise ValueError("Invalid rule action.")
        #     if split_rule[3] not in ('combat', 'expedition', 'pvp', 'kca'):
        #         raise ValueError("Invalid rule action module.")
        self._slots = slots
