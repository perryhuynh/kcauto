from config_base import AbstractConfigModule


class ConfigScheduledSleep(AbstractConfigModule):
    config = {}

    def parse_cfg(self):
        """Method to parse the ScheduledSleep settings of the passed-in config.
        """
        cp = self.config_parser

        for module in ('script', 'expedition', 'combat'):
            module_title = module.title()
            self.config['{}_sleep_enabled'.format(module)] = (
                cp.getboolean(
                    'ScheduledSleep', '{}SleepEnabled'.format(module_title)))
            self.config['{}_sleep_start_time'.format(module)] = (
                "{:04d}".format(cp.getint(
                    'ScheduledSleep', '{}SleepStartTime'.format(
                        module_title))))
            self.config['{}_sleep_length'.format(module)] = (
                cp.getfloat(
                    'ScheduledSleep', '{}SleepLength'.format(module_title)))

        return self.config

    @staticmethod
    def validate_cfg(config):
        """Method to validate the ScheduledSleep settings.
        """
        return True
