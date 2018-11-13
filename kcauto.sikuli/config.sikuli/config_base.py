from abc import ABCMeta, abstractmethod


class AbstractConfigModule:
    """Abstract base class for config reader modules.
    """
    __metaclass__ = ABCMeta

    def __init__(self, config_parser):
        self.config_parser = config_parser
        self.valid = False
        self.config = {'enabled': False}

    @abstractmethod
    def parse_cfg(self):
        pass

    @staticmethod
    def validate_cfg(config):
        pass

    @staticmethod
    def _getlist(config, section, option):
        """Method to split a comma-delimited string in the config to a list
        of strings.

        Args:
            config (ConfigParser): ConfigParser instance
            section (str): section in config file
            option (str): line item in config file

        Returns:
            list: list of split values
        """
        value = config.get(section, option).replace(' ', '').split(',')
        if '' in value:
            value.remove('')
        return value

    @staticmethod
    def try_cast_to_int(val):
        """Method that attempts to coerce the val to an int, returning the val
        as-is the cast fails.

        Args:
            val (str): string to attempt to cast to int

        Returns:
            int, str: int if the cast was successful; the original str
                representation otherwise
        """
        try:
            return int(val)
        except ValueError:
            return val
