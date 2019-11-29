from config.config_base import ConfigBase
from kca_enums.interaction_modes import InteractionModeEnum
from constants import (
    DEFAULT_CHROME_DEV_PORT, MIN_JST_OFFSET, MAX_JST_OFFSET, MIN_PORT,
    MAX_PORT)


class ConfigGeneral(ConfigBase):
    _jst_offset = 0
    _interaction_mode = None
    _chrome_dev_port = DEFAULT_CHROME_DEV_PORT
    _debug_mode = False

    def __init__(self, config):
        super().__init__(config)
        self.jst_offset = config['general.jst_offset']
        self.interaction_mode = config['general.interaction_mode']
        self.chrome_dev_port = config['general.chrome_dev_port']

    @property
    def jst_offset(self):
        return self._jst_offset

    @jst_offset.setter
    def jst_offset(self, value):
        if not MIN_JST_OFFSET <= value <= MAX_JST_OFFSET:
            raise ValueError("Invalid JST offset")
        self._jst_offset = value

    @property
    def interaction_mode(self):
        return self._interaction_mode

    @interaction_mode.setter
    def interaction_mode(self, value):
        if not InteractionModeEnum.contains_value(value):
            raise ValueError("Invalid Interaction Mode")
        self._interaction_mode = InteractionModeEnum(value)

    @property
    def is_direct_control(self):
        return self.interaction_mode is InteractionModeEnum.DIRECT_CONTROL

    @property
    def chrome_dev_port(self):
        return self._chrome_dev_port

    @chrome_dev_port.setter
    def chrome_dev_port(self, value):
        if value is None:
            self._chrome_dev_port = DEFAULT_CHROME_DEV_PORT
        elif type(value) is not int or not MIN_PORT <= value <= MAX_PORT:
            raise ValueError("Invalid Chrome Dev Port")
        self._chrome_dev_port = value
