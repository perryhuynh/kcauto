from abc import ABC


class ConfigBase(ABC):
    _config = {}

    def __init__(self, config):
        self._config = config

    def __eq__(self, other):
        for prop, value in vars(self).iteritems():
            if value != getattr(other, prop, None):
                return False
        return True

    def __ne__(self, other):
        for prop, value in vars(self).iteritems():
            if value != getattr(other, prop, None):
                return True
        return False
