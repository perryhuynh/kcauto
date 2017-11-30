# config module
import ConfigParser
import os
import sys
import re
from sikuli import getBundlePath
from copy import deepcopy
from util import Util


class Config(object):
    """Config module that reads and validates the config to be passed to
    kcauto-kai

    Attributes:
        basic_recovery (bool): indicates whether or not basic recovery is on
            (UNUSED)
        changed (bool): indicates whether or not the config has changed from
            the previously stored config
        combat (dict): dict of combat-related config settings
        config_file (str): name of config file
        expeditions (dict): dict of expedition-related config settings
        expeditions_all (list): list of all expeditions to be passed in to the
            expedition module
        initialized (bool): indicates whether or not kcauto-kai has been
            initialized with the current config
        jst_offset (int): hours offset from JST
        ok (bool): indicates whether or not the recently passed in config
            passes validation or not
        program (str): name of window Kantai Collection is running in
        pvp (dict): dict of pvp-related config settings
        quests (dict): dict of quest-related config settings
        recovery_method (str): specifies the recovery method to be attempted
            by kcauto-kai (UNUSED)
        scheduled_sleep (dict): dict of scheduled sleep-related config settings
    """

    ok = False
    initialized = False
    changed = False
    program = ''
    recovery_method = ''
    basic_recovery = False
    jst_offset = 0

    scheduled_sleep = {'enabled': False}
    expeditions = {'enabled': False}
    pvp = {'enabled': False}
    combat = {'enabled': False}
    quests = {'enabled': False}

    def __init__(self, config_file):
        """Initializes the config file by changing the working directory to the
        root kcauto-kai folder and reading the passed in config file.

        Args:
            config_file (str): name of config file
        """
        Util.log_msg("Initializing config module")
        os.chdir(getBundlePath())
        os.chdir('..')
        self.config_file = config_file
        self.read()

    def read(self):
        """Method that backs up the previous config, reads in the specified
        config file and validates it.
        """
        backup_config = deepcopy(self.__dict__)

        if not self.initialized:
            Util.log_msg('Reading config')

        config = ConfigParser.ConfigParser()
        config.read(self.config_file)

        self._read_general(config)

        if config.getboolean('ScheduledSleep', 'Enabled'):
            self._read_scheduled_sleep(config)
        else:
            self.scheduled_sleep = {'enabled': False}

        if config.getboolean('Expeditions', 'Enabled'):
            self._read_expeditions(config)
        else:
            self.expeditions = {'enabled': False}

        if config.getboolean('PvP', 'Enabled'):
            self._read_pvp(config)
        else:
            self.pvp = {'enabled': False}

        if config.getboolean('Combat', 'Enabled'):
            self._read_combat(config)
        else:
            self.combat = {'enabled': False}

        if config.getboolean('Quests', 'Enabled'):
            self._read_quests(config)
        else:
            self.quests = {'enabled': False}

        self.validate()

        if (self.ok and not self.initialized):
            Util.log_msg('Starting kancolle-auto!')
            self.initialized = True
            self.changed = True
        elif (not self.ok and not self.initialized):
            Util.log_error('Invalid config. Please check your config file.')
            sys.exit(1)
        elif (not self.ok and self.initialized):
            Util.warning(
                'Config change detected, but with problems. Rolling back '
                'config.')
            self._rollback_config(backup_config)
        elif (self.ok and self.initialized):
            if backup_config != self.__dict__:
                Util.log_warning('Config change detected. Hot-reloading.')
                self.changed = True

    def validate(self):
        """Method to validate the passed in config file
        """
        if not self.initialized:
            Util.log_msg("Validating config")
        self.ok = True

        if self.expeditions['enabled']:
            valid_expeditions = range(1, 41) + [9998, 9999]
            for expedition in self.expeditions_all:
                if expedition not in valid_expeditions:
                    Util.log_error(
                        "Invalid Expedition: '{}'.".format(expedition))
                    self.ok = False

        if self.combat['enabled']:
            # validate the combat engine
            if self.combat['engine'] not in ('legacy', 'live'):
                Util.log_error("Invalid Combat Engine: '{}'.".format(
                    self.combat['engine']))
                self.ok = False
            # validate the fleet mode
            if self.combat['fleet_mode'] not in (
                    'ctf', 'stf', 'transport', 'striking', ''):
                Util.log_error("Invalid Combat FleetMode: '{}'.".format(
                    self.combat['fleet_mode']))
                self.ok = False
            # validate the node selects
            if self.combat['raw_node_selects']:
                node_selects = {}
                for raw_node_select in self.combat['raw_node_selects']:
                    nsm = re.search('([A-Z0-9]+)>([A-Z0-9]+)', raw_node_select)
                    if nsm:
                        node_selects[nsm.group(1)] = nsm.group(2)
                    else:
                        Util.log_error("Invalid Node Select: '{}'".format(
                            raw_node_select))
                        self.ok = False
                if self.ok and node_selects:
                    self.combat['node_selects'] = node_selects
                del self.combat['raw_node_selects']
            # validate the formations
            if self.combat['raw_formations']:
                formations = {}
                valid_formations = (
                    'combinedfleet_1', 'combinedfleet_2', 'combinedfleet_3',
                    'combinedfleet_4', 'line_ahead', 'double_line', 'diamond',
                    'echelon', 'line_abreast', 'vanguard')
                for raw_formation in self.combat['raw_formations']:
                    fm = re.search('([A-Z0-9]+):({})'.format(
                        '|'.join(valid_formations)), raw_formation)
                    if fm:
                        fm_node = (
                            int(fm.group(1)) if fm.group(1).isdigit()
                            else fm.group(1))
                        formations[fm_node] = fm.group(2)
                    else:
                        Util.log_error("Invalid Formation: '{}'".format(
                            raw_formation))
                        self.ok = False
                if self.ok and formations:
                    self.combat['formations'] = formations
                del self.combat['raw_formations']
            # validate the night battles
            if self.combat['raw_night_battles']:
                night_battles = {}
                for raw_night_battle in self.combat['raw_night_battles']:
                    nbm = re.search(
                        '([A-Z0-9]+)>(True|False)', raw_night_battle)
                    if nbm:
                        nbm_node = (
                            int(nbm.group(1)) if nbm.group(1).isdigit()
                            else nbm.group(1))
                        night_battles[nbm_node] = (
                            True if nbm.group(2) is 'True' else False)
                    else:
                        Util.log_error("Invalid Night Battle: '{}'".format(
                            raw_night_battle))
                        self.ok = False
                if self.ok and night_battles:
                    self.combat['night_battles'] = night_battles
                del self.combat['raw_night_battles']
            # validate the misc options
            for option in self.combat['misc_options']:
                if option not in (
                        'CheckFatigue', 'ReserveDocks', 'PortCheck',
                        'MedalStop'):
                    Util.log_error(
                        "Invalid Combat MiscOption: '{}'.".format(option))
                    self.ok = False

        # TODO: Add additional checks to make sure that expeditions to fleet 2
        # and 3 were not assigned if combined fleets or striking fleet modes
        # were assigned

    def _read_general(self, config):
        """Method to parse the General settings of the passed in config.

        Args:
            config (ConfigParser): ConfigParser instance
        """
        self.program = config.get('General', 'Program')
        self.jst_offset = config.getint('General', 'JSTOffset')

    def _read_scheduled_sleep(self, config):
        """Method to parse the Scheduled Sleep settings of the passed in
        config.

        Args:
            config (ConfigParser): ConfigParser instance
        """
        self.scheduled_sleep['enabled'] = True
        self.scheduled_sleep['start_time'] = "{:04d}".format(
            config.getint('ScheduledSleep', 'StartTime'))
        self.scheduled_sleep['sleep_length'] = config.getfloat(
            'ScheduledSleep', 'SleepLength')

    def _read_expeditions(self, config):
        """Method to parse the Expedition settings of the passed in config.

        Args:
            config (ConfigParser): ConfigParser instance
        """
        self.expeditions['enabled'] = True
        self.expeditions_all = []
        if config.get('Expeditions', 'Fleet2'):
            self.expeditions['fleet2'] = map(
                int, self._getlist(config, 'Expeditions', 'Fleet2'))
            self.expeditions_all.extend(self.expeditions['fleet2'])
        else:
            self.expeditions.pop('fleet2', None)
        if config.get('Expeditions', 'Fleet3'):
            self.expeditions['fleet3'] = map(
                int, self._getlist(config, 'Expeditions', 'Fleet3'))
            self.expeditions_all.extend(self.expeditions['fleet3'])
        else:
            self.expeditions.pop('fleet3', None)
        if config.get('Expeditions', 'Fleet4'):
            self.expeditions['fleet4'] = map(
                int, self._getlist(config, 'Expeditions', 'Fleet4'))
            self.expeditions_all.extend(self.expeditions['fleet4'])
        else:
            self.expeditions.pop('fleet4', None)

    def _read_pvp(self, config):
        """Method to parse the Ovo settings of the passed in config.

        Args:
            config (ConfigParser): ConfigParser instance
        """
        self.pvp['enabled'] = True

    def _read_combat(self, config):
        """Method to parse the Combat settings of the passed in config.

        Args:
            config (ConfigParser): ConfigParser instance
        """
        self.combat['enabled'] = True
        self.combat['engine'] = config.get('Combat', 'Engine')
        self.combat['fleet_mode'] = config.get('Combat', 'FleetMode')
        self.combat['combined_fleet'] = (
            True if self.combat['fleet_mode'] in ['ctf', 'stf', 'transport']
            else False)
        self.combat['map'] = config.get('Combat', 'Map')
        combat_nodes = config.get('Combat', 'CombatNodes')
        self.combat['combat_nodes'] = int(combat_nodes) if combat_nodes else 99
        self.combat['raw_node_selects'] = (
            self._getlist(config, 'Combat', 'NodeSelects'))
        self.combat['raw_formations'] = (
            self._getlist(config, 'Combat', 'Formations'))
        self.combat['raw_night_battles'] = (
            self._getlist(config, 'Combat', 'NightBattles'))
        self.combat['retreat_limit'] = config.get('Combat', 'RetreatLimit')
        self.combat['repair_limit'] = config.get('Combat', 'RepairLimit')
        self.combat['repair_time_limit'] = config.getint(
            'Combat', 'RepairTimeLimit')
        self.combat['misc_options'] = self._getlist(
            config, 'Combat', 'MiscOptions')
        if config.get('Combat', 'LBASGroups'):
            self.combat['lbas_enabled'] = True
            self.combat['lbas_groups'] = map(
                int, self._getlist(config, 'Combat', 'LBASGroups'))
            self.combat['lbas_group_1_nodes'] = self._getlist(
                config, 'Combat', 'LBASGroup1Nodes')
            self.combat['lbas_group_2_nodes'] = self._getlist(
                config, 'Combat', 'LBASGroup2Nodes')
            self.combat['lbas_group_3_nodes'] = self._getlist(
                config, 'Combat', 'LBASGroup3Nodes')
        else:
            self.combat['lbas_enabled'] = False

    def _read_quests(self, config):
        """Method to parse the Quest settings of the passed in config.

        Args:
            config (ConfigParser): ConfigParser instance
        """
        self.quests['enabled'] = True

    def _rollback_config(self, config):
        """Method to roll back the config to the passed in config's.

        Args:
            config (dict): previously backed up config
        """
        for key in config:
            setattr(self, key, config['key'])

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
