from config_base import AbstractConfigModule
from util import Util


class ConfigPvP(AbstractConfigModule):
    def parse_cfg(self):
        """Method to parse the PvP settings of the passed-in config.
        """
        cp = self.config_parser

        if not cp.getboolean('PvP', 'Enabled'):
            self.config.clear()
            self.config['enabled'] = False
            return self.config

        self.config['enabled'] = True
        self.config['fleet'] = (
            cp.getint('PvP', 'Fleet')
            if cp.get('PvP', 'Fleet')
            else None)

        return self.config

    @staticmethod
    def validate_cfg(config):
        """Method to validate the PvP settings.
        """
        valid = True
        pvp_cfg = config['pvp']

        if not pvp_cfg['enabled']:
            if len(pvp_cfg) != 1:
                valid = False
            return valid

        # validate fleet preset
        if pvp_cfg['fleet'] and not 0 < pvp_cfg['fleet'] < 13:
            Util.log_error(
                "Invalid fleet preset ID for PvP: '{}'".format(
                    pvp_cfg['fleet']))
            valid = False

        return valid
