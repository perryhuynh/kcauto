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
        scheduled_sleep (dict): dict of scheduled sleep-related config settings
        scheduled_stop (dict): dict of scheduled stop-related config settings
    """

    ok = False
    initialized = False
    changed = False
    program = ''
    jst_offset = 0
    pause = False

    scheduled_sleep = {}
    scheduled_stop = {}
    expeditions = {'enabled': False}
    pvp = {'enabled': False}
    combat = {'enabled': False}
    ship_switcher = {'enabled': False}
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
        self._read_scheduled_sleep(config)
        self._read_scheduled_stop(config)

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

        if (config.getboolean('ShipSwitcher', 'Enabled') and
                self.combat['enabled']):
            self._read_ship_switcher(config)
        else:
            self.ship_switcher = {'enabled': False}

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

        if self.scheduled_stop:
            for module in ('expedition', 'combat'):
                stop_key = '{}_stop_mode'.format(module)
                if self.scheduled_stop[stop_key] not in (
                        '', 'script', 'module'):
                    Util.log_error(
                        "Invalid Stop Mode for {}: '{}'".format(
                            module.title(), self.scheduled_stop[stop_key]))
                    self.ok = False

        if self.expeditions['enabled']:
            valid_expeditions = range(1, 41) + [
                'A1', 'A2', 'A3', 'B1', 9998, 9999]
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
            # validate fleet modes and possible expedition fleet collisions
            if (self.combat['fleet_mode'] in ('ctf', 'stf', 'transport')
                    and self.expeditions['enabled']):
                if 'fleet2' in self.expeditions:
                    Util.log_error(
                        "Expedition(s) defined for Fleet 2 while Combat Fleet "
                        "Mode is defined as Combined Fleet.")
                    self.ok = False
            if (self.combat['fleet_mode'] == 'striking'
                    and self.expeditions['enabled']):
                if 'fleet3' in self.expeditions:
                    Util.log_error(
                        "Expedition(s) defined for Fleet 3 while Combat Fleet "
                        "Mode is defined as Striking Fleet.")
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
            # validate the night battles
            if self.combat['raw_night_battles']:
                night_battles = {}
                for raw_night_battle in self.combat['raw_night_battles']:
                    nbm = re.search(
                        '([A-Z0-9]+):(True|False)', raw_night_battle)
                    if nbm:
                        nbm_node = (
                            int(nbm.group(1)) if nbm.group(1).isdigit()
                            else nbm.group(1))
                        night_battles[nbm_node] = (
                            True if nbm.group(2) == 'True' else False)
                    else:
                        Util.log_error("Invalid Night Battle: '{}'".format(
                            raw_night_battle))
                        self.ok = False
                if self.ok and night_battles:
                    self.combat['night_battles'] = night_battles
            # validate lbas setup
            if self.combat['lbas_enabled']:
                for group in (1, 2, 3):
                    if self.combat['lbas_group_{}_nodes'.format(group)]:
                        if group not in self.combat['lbas_groups']:
                            Util.log_error(
                                "LBAS Group {} has nodes assigned to it but "
                                "is not active. Either clear the nodes or "
                                "activate the LBAS Group".format(group))
                            self.ok = False
                        elif (len(self.combat['lbas_group_{}_nodes'.format(
                                group)]) != 2):
                            Util.log_error(
                                "LBAS Group {} does not have 2 nodes assigned "
                                " to it".format(group))
                            self.ok = False
            # validate the misc options
            for option in self.combat['misc_options']:
                if option not in (
                        'CheckFatigue', 'ReserveDocks', 'PortCheck',
                        'ClearStop'):
                    Util.log_error(
                        "Invalid Combat MiscOption: '{}'.".format(option))
                    self.ok = False
        if self.ship_switcher['enabled']:
            if self.combat['fleet_mode'] != '':
                Util.log_error(
                    "Ship Switcher can only be used with standard fleets")
                self.ok = False
            for slot in range(0, 6):
                if slot not in self.ship_switcher:
                    continue
                criteria = self.ship_switcher[slot]['criteria']
                for c in criteria:
                    if c not in ('damage', 'fatigue', 'sparkle'):
                        Util.log_error(
                            "Invalid switch criteria for slot {}: '{}'".format(
                                slot, c))
                        self.ok = False
                if self.ship_switcher[slot]['mode'] == 'position':
                    for ship in self.ship_switcher[slot]['ships']:
                        if len(ship) != 3:
                            Util.log_error(
                                "Invalid # of arguments for ship in slot {}"
                                .format(slot))
                            self.ok = False
                if self.ship_switcher[slot]['mode'] == 'class':
                    for ship in self.ship_switcher[slot]['ships']:
                        if len(ship) < 2:
                            Util.log_error(
                                "Invalid # of arguments for ship in slot {}"
                                .format(slot))
                            self.ok = False

    def _read_general(self, config):
        """Method to parse the General settings of the passed in config.

        Args:
            config (ConfigParser): ConfigParser instance
        """
        self.program = config.get('General', 'Program')
        self.jst_offset = config.getint('General', 'JSTOffset')
        self.pause = config.getboolean('General', 'Pause')

    def _read_scheduled_sleep(self, config):
        """Method to parse the Scheduled Sleep settings of the passed in
        config.

        Args:
            config (ConfigParser): ConfigParser instance
        """
        for module in ('script', 'expedition', 'combat'):
            module_title = module.title()
            self.scheduled_sleep['{}_sleep_enabled'.format(module)] = (
                config.getboolean(
                    'ScheduledSleep', '{}SleepEnabled'.format(module_title)))
            self.scheduled_sleep['{}_sleep_start_time'.format(module)] = (
                "{:04d}".format(config.getint(
                    'ScheduledSleep', '{}SleepStartTime'.format(
                        module_title))))
            self.scheduled_sleep['{}_sleep_length'.format(module)] = (
                config.getfloat(
                    'ScheduledSleep', '{}SleepLength'.format(module_title)))

    def _read_scheduled_stop(self, config):
        """Method to parse the Scheduled Stop settings of the passed in
        config.

        Args:
            config (ConfigParser): ConfigParser instance
        """
        for module in ('script', 'expedition', 'combat'):
            module_title = module.title()
            self.scheduled_stop['{}_stop_enabled'.format(module)] = (
                config.getboolean(
                    'ScheduledStop', '{}StopEnabled'.format(module_title)))
            try:
                self.scheduled_stop['{}_stop_count'.format(module)] = (
                    config.getint(
                        'ScheduledStop', '{}StopCount'.format(module_title)))
            except ValueError:
                self.scheduled_stop['{}_stop_count'.format(module)] = None
            try:
                self.scheduled_stop['{}_stop_time'.format(module)] = (
                    "{:04d}".format(config.getint(
                        'ScheduledStop', '{}StopTime'.format(
                            module_title))))
            except ValueError:
                self.scheduled_stop['{}_stop_time'.format(module)] = None
            if module in ('expedition', 'combat'):
                self.scheduled_stop['{}_stop_mode'.format(module)] = (
                    config.get(
                        'ScheduledStop', '{}StopMode'.format(module_title)))

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
        """Method to parse the PvP settings of the passed in config.

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
        self.combat['striking_fleet'] = (
            True if self.combat['fleet_mode'] == 'striking' else False)
        self.combat['map'] = config.get('Combat', 'Map')
        combat_nodes = config.get('Combat', 'CombatNodes')
        self.combat['combat_nodes'] = int(combat_nodes) if combat_nodes else 99
        self.combat['node_selects'] = {}
        self.combat['raw_node_selects'] = (
            self._getlist(config, 'Combat', 'NodeSelects'))
        self.combat['formations'] = {}
        self.combat['raw_formations'] = (
            self._getlist(config, 'Combat', 'Formations'))
        self.combat['night_battles'] = {}
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

    def _read_ship_switcher(self, config):
        """Method to parse the ShipSwitcher settings of the passed in config.
        Only run if Combat is also enabled.

        Args:
            config (ConfigParser): ConfigParser instance
        """

        def _create_ship_switcher_dict(slot, criteria, ships):
            slot_dict = {
                'slot': slot,
                'criteria': criteria,
                'mode': None,
                'ships': []
            }

            for ship in ships:
                ship_dict = {}
                ship_split = ship.split(':')
                if ship_split[0] in ('C', 'S'):
                    # class or shipname mode
                    ship_dict['sort_order'] = 'class'
                    if ship_split[0] == 'C':
                        slot_dict['mode'] = (
                            'class' if slot_dict['mode'] is None else
                            slot_dict['mode'])
                        ship_dict['class'] = ship_split[1].lower()
                    elif ship_split[0] == 'S':
                        slot_dict['mode'] = (
                            'ship' if slot_dict['mode'] is None else
                            slot_dict['mode'])
                        ship_dict['ship'] = ship_split[1].lower()
                    if ship_split[2] != '_':
                        ship_dict['level'] = ship_split[2]
                    if ship_split[3] != '_':
                        ship_dict['locked'] = (
                            True if ship_split[3] == 'L' else False)
                    if ship_split[4] != '_':
                        ship_dict['ringed'] = (
                            True if ship_split[4] == 'R' else False)
                elif ship_split[0] in ('P'):
                    # class in position mode
                    slot_dict['mode'] = (
                        'position' if slot_dict['mode'] is None else
                        slot_dict['mode'])
                    if ship_split[1] == 'N':
                        ship_dict['sort_order'] = 'new'
                    elif ship_split[1] == 'C':
                        ship_dict['sort_order'] = 'class'
                    elif ship_split[1] == 'L':
                        ship_dict['sort_order'] = 'level'
                    if ship_split[2] == 'E':
                        ship_dict['offset_ref'] = 'end'
                    elif ship_split[2] == 'S':
                        ship_dict['offset_ref'] = 'start'
                    ship_dict['offset'] = int(ship_split[3])
                slot_dict['ships'].append(ship_dict)
            return slot_dict

        self.ship_switcher['enabled'] = True
        for slot in range(0, 6):
            criteria = self._getlist(
                config, 'ShipSwitcher', 'Slot{}Criteria'.format(slot + 1))
            ships = self._getlist(
                config, 'ShipSwitcher', 'Slot{}Ships'.format(slot + 1))
            if criteria and ships:
                self.ship_switcher[slot] = _create_ship_switcher_dict(
                    slot, criteria, ships)

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
