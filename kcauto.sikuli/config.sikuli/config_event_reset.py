from config_base import AbstractConfigModule
from util import Util


class ConfigEventReset(AbstractConfigModule):
    def parse_cfg(self):
        """Method to parse the EventReset settings of the passed-in config.
        """
        cp = self.config_parser

        if not cp.getboolean('EventReset', 'Enabled'):
            self.config.clear()
            self.config['enabled'] = False
            return self.config

        self.config['enabled'] = True
        self.config['frequency'] = cp.getint('EventReset', 'Frequency')
        self.config['farm_difficulty'] = cp.get(
            'EventReset', 'FarmDifficulty')
        self.config['reset_difficulty'] = cp.get(
            'EventReset', 'ResetDifficulty')

        return self.config

    @staticmethod
    def validate_cfg(config):
        """Method to validate the EventReset settings.
        """
        valid = True
        event_reset_cfg = config['event_reset']
        combat_cfg = config['combat']

        if not event_reset_cfg['enabled']:
            if len(event_reset_cfg) != 1:
                valid = False
            return valid

        valid_difficulties = ('casual', 'easy', 'medium', 'hard')

        # validate combat being enabled
        if not combat_cfg['enabled']:
            Util.log_error(
                "Event Reset can only be used if Combat is enabled")
            valid = False

        # validate event map sortie
        if combat_cfg['map'][0] != 'E':
            Util.log_error(
                "Invalid map ({}) to use with Event Reset. Event Reset "
                "can only be used when sortieing to Event maps".format(
                    combat_cfg['map']))
            valid = False

        # validate farm difficulty
        if event_reset_cfg['farm_difficulty'] not in valid_difficulties:
            Util.log_error(
                "Invalid difficulty specified for Event Reset Farm "
                "Difficulty: '{}'.".format(
                    event_reset_cfg['farm_difficulty']))
            valid = False

        # validate reset difficulty
        if event_reset_cfg['reset_difficulty'] not in valid_difficulties:
            Util.log_error(
                "Invalid difficulty specified for Event Reset Reset "
                "Difficulty: '{}'.".format(
                    event_reset_cfg['reset_difficulty']))
            valid = False

        # validate that farm difficulty is not the reset difficulty
        if (event_reset_cfg['farm_difficulty']
                == event_reset_cfg['reset_difficulty']):
            Util.log_error(
                "Event Reset Farm and Reset difficulty cannot be "
                "identical.")
            valid = False

        return valid
