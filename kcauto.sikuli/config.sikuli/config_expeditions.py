from config_base import AbstractConfigModule
from util import Util


class ConfigExpeditions(AbstractConfigModule):
    def parse_cfg(self):
        """Method to parse the Expedition settings of the passed-in config.
        """
        cp = self.config_parser

        if not cp.getboolean('Expeditions', 'Enabled'):
            self.config.clear()
            self.config['enabled'] = False
            return self.config

        self.config['enabled'] = True
        self.config['expeditions_all'] = []
        if cp.get('Expeditions', 'Fleet2'):
            self.config['fleet2'] = map(
                self.try_cast_to_int,
                self._getlist(cp, 'Expeditions', 'Fleet2'))
            self.config['expeditions_all'].extend(self.config['fleet2'])
        else:
            self.config.pop('fleet2', None)
        if cp.get('Expeditions', 'Fleet3'):
            self.config['fleet3'] = map(
                self.try_cast_to_int,
                self._getlist(cp, 'Expeditions', 'Fleet3'))
            self.config['expeditions_all'].extend(self.config['fleet3'])
        else:
            self.config.pop('fleet3', None)
        if cp.get('Expeditions', 'Fleet4'):
            self.config['fleet4'] = map(
                self.try_cast_to_int,
                self._getlist(cp, 'Expeditions', 'Fleet4'))
            self.config['expeditions_all'].extend(self.config['fleet4'])
        else:
            self.config.pop('fleet4', None)

        return self.config

    @staticmethod
    def validate_cfg(config):
        """Method to validate the Expedition settings.
        """
        valid = True
        expeditions_cfg = config['expeditions']

        if not expeditions_cfg['enabled']:
            if len(expeditions_cfg) != 1:
                valid = False
            return valid

        # validate expeditions
        valid_expeditions = range(1, 42) + [
            'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'S1', 'S2']
        for expedition in expeditions_cfg['expeditions_all']:
            if expedition not in valid_expeditions:
                Util.log_error(
                    "Invalid Expedition: '{}'.".format(expedition))
                valid = False

        return valid
