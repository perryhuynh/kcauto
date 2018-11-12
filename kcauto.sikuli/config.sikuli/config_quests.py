from config_base import AbstractConfigModule
from util import Util


class ConfigQuests(AbstractConfigModule):
    def parse_cfg(self):
        """Method to parse the Quest settings of the passed-in config.
        """
        cp = self.config_parser

        if not cp.getboolean('Quests', 'Enabled'):
            self.config.clear()
            self.config['enabled'] = False
            return self.config

        self.config['enabled'] = True
        self.config['quest_groups'] = self._getlist(
            cp, 'Quests', 'QuestGroups')

        return self.config

    @staticmethod
    def validate_cfg(config):
        """Method to validate the Quest settings.
        """
        valid = True
        quests_cfg = config['quests']

        if not quests_cfg['enabled']:
            if len(quests_cfg) != 1:
                valid = False
            return valid

        # validate that quest groups are specified
        if len(quests_cfg['quest_groups']) == 0:
            Util.log_error("No Quest Groups specified for Quest module")
            valid = False

        # validate quest groups
        for qg in quests_cfg['quest_groups']:
            if qg not in ('daily', 'weekly', 'monthly', 'others'):
                Util.log_error(
                    "Invalid Quest Group specified: '{}'".format(qg))
                valid = False

        return valid
