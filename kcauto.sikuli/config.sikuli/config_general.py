from config_base import AbstractConfigModule


class ConfigGeneral(AbstractConfigModule):
    config = {}

    def parse_cfg(self):
        """Method to parse the General settings of the passed-in config.
        """
        cp = self.config_parser

        self.config['program'] = cp.get('General', 'Program')
        self.config['jst_offset'] = cp.getint('General', 'JSTOffset')
        self.config['pause'] = cp.getboolean('General', 'Pause')

        return self.config

    @staticmethod
    def validate_cfg(config):
        """Method to validate the General settings.
        """
        return True
