from config_base import AbstractConfigModule
from util import Util


class ConfigScheduledStop(AbstractConfigModule):
    config = {}

    def parse_cfg(self):
        """Method to parse the ScheduledStop settings of the passed-in config.
        """
        cp = self.config_parser

        for module in ('script', 'expedition', 'combat'):
            module_title = module.title()
            self.config['{}_stop_enabled'.format(module)] = (
                cp.getboolean(
                    'ScheduledStop', '{}StopEnabled'.format(module_title)))
            try:
                self.config['{}_stop_count'.format(module)] = (
                    cp.getint(
                        'ScheduledStop', '{}StopCount'.format(module_title)))
            except ValueError:
                self.config['{}_stop_count'.format(module)] = None
            try:
                self.config['{}_stop_time'.format(module)] = (
                    "{:04d}".format(cp.getint(
                        'ScheduledStop', '{}StopTime'.format(
                            module_title))))
            except ValueError:
                self.config['{}_stop_time'.format(module)] = None
            if module in ('expedition', 'combat'):
                self.config['{}_stop_mode'.format(module)] = (
                    cp.get(
                        'ScheduledStop', '{}StopMode'.format(module_title)))

        return self.config

    @staticmethod
    def validate_cfg(config):
        """Method to validate the ScheduledStop settings.
        """
        valid = True
        scheduled_stop_cfg = config['scheduled_stop']

        # validate stop modes
        for module in ('expedition', 'combat'):
            stop_key = '{}_stop_mode'.format(module)
            if scheduled_stop_cfg[stop_key] not in (
                    '', 'script', 'module'):
                Util.log_error(
                    "Invalid Stop Mode for {}: '{}'".format(
                        module.title(), scheduled_stop_cfg[stop_key]))
                valid = False

        return valid
