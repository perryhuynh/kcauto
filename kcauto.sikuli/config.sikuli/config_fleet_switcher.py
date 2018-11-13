from config_base import AbstractConfigModule
from util import Util


class ConfigFleetSwitcher(AbstractConfigModule):
    def parse_cfg(self):
        """Method to parse the PvP settings of the passed-in config.
        """

        if not self.config['enabled']:
            self.config.clear()
            self.config['enabled'] = False
            return

    @staticmethod
    def validate_cfg(config):
        """Method to validate the FleetSwitcher settings.
        """
        valid = True
        combat_cfg = config['combat']

        # validate fleet switcher and combat fleet mode conflict
        if combat_cfg['enabled'] and combat_cfg['fleet_mode'] != '':
            Util.log_error(
                "Fleet Presets cannot be used when combat is enabled and not "
                "in Standard fleet mode")
            valid = False

        return valid
