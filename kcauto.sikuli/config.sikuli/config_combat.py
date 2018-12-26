import re
from config_base import AbstractConfigModule
from util import Util


class ConfigCombat(AbstractConfigModule):
    def parse_cfg(self):
        """Method to parse the Combat settings of the passed-in config.
        """
        cp = self.config_parser

        if not cp.getboolean('Combat', 'Enabled'):
            self.config.clear()
            self.config['enabled'] = False
            return self.config

        self.config['enabled'] = True
        self.config['engine'] = cp.get('Combat', 'Engine')
        if cp.get('Combat', 'Fleets'):
            self.config['fleets'] = map(
                int, self._getlist(cp, 'Combat', 'Fleets'))
        else:
            self.config['fleets'] = []
        self.config['map'] = cp.get('Combat', 'Map')
        self.config['fleet_mode'] = cp.get('Combat', 'FleetMode')
        self.config['combined_fleet'] = (
            True if self.config['fleet_mode'] in ['ctf', 'stf', 'transport']
            else False)
        self.config['striking_fleet'] = (
            True if self.config['fleet_mode'] == 'striking' else False)
        # defaults for retreat nodes and combat nodes
        self.config['retreat_nodes'] = []
        self.config['combat_nodes'] = 99
        # overwrite above if needed
        if cp.get('Combat', 'RetreatNodes'):
            temp_retreat_values = set(
                self._getlist(cp, 'Combat', 'RetreatNodes'))
            for val in temp_retreat_values:
                if val.isdigit():
                    self.config['combat_nodes'] = (
                        int(val) if int(val) < self.config['combat_nodes']
                        else self.config['combat_nodes'])
                else:
                    self.config['retreat_nodes'].append(val)
        self.config['node_selects'] = {}
        self.config['raw_node_selects'] = (
            self._getlist(cp, 'Combat', 'NodeSelects'))
        self.config['formations'] = {}
        self.config['raw_formations'] = (
            self._getlist(cp, 'Combat', 'Formations'))
        self.config['night_battles'] = {}
        self.config['raw_night_battles'] = (
            self._getlist(cp, 'Combat', 'NightBattles'))
        self.config['retreat_limit'] = cp.get('Combat', 'RetreatLimit')
        self.config['repair_limit'] = cp.get('Combat', 'RepairLimit')
        self.config['repair_time_limit'] = cp.getint(
            'Combat', 'RepairTimeLimit')
        self.config['misc_options'] = self._getlist(
            cp, 'Combat', 'MiscOptions')
        if cp.get('Combat', 'LBASGroups'):
            self.config['lbas_enabled'] = True
            self.config['lbas_groups'] = map(
                int, sorted(self._getlist(cp, 'Combat', 'LBASGroups')))
            self.config['lbas_group_1_nodes'] = self._getlist(
                cp, 'Combat', 'LBASGroup1Nodes')
            self.config['lbas_group_2_nodes'] = self._getlist(
                cp, 'Combat', 'LBASGroup2Nodes')
            self.config['lbas_group_3_nodes'] = self._getlist(
                cp, 'Combat', 'LBASGroup3Nodes')
        else:
            self.config['lbas_enabled'] = False

        return self.config

    @staticmethod
    def validate_cfg(config):
        """Method to validate the Combat settings.
        """
        valid = True
        combat_cfg = config['combat']
        expeditions_cfg = config['expeditions']

        if not combat_cfg['enabled']:
            if len(combat_cfg) != 1:
                valid = False
            return valid

        # validate the combat engine
        if combat_cfg['engine'] not in ('legacy', 'live'):
            Util.log_error("Invalid Combat Engine: '{}'.".format(
                combat_cfg['engine']))
            valid = False

        # validate fleet presets
        for preset in combat_cfg['fleets']:
            if not 0 < preset < 13:
                Util.log_error(
                    "Invalid fleet preset ID for combat: '{}'.".format(preset))
                valid = False

        # validate the fleet mode
        if combat_cfg['fleet_mode'] not in (
                'ctf', 'stf', 'transport', 'striking', ''):
            Util.log_error("Invalid Combat FleetMode: '{}'.".format(
                combat_cfg['fleet_mode']))
            valid = False

        # validate fleet modes and possible expedition fleet collisions
        if (combat_cfg['fleet_mode'] in ('ctf', 'stf', 'transport')
                and expeditions_cfg['enabled']):
            if 'fleet2' in expeditions_cfg:
                Util.log_error(
                    "Expedition(s) defined for Fleet 2 while Combat Fleet "
                    "Mode is defined as Combined Fleet.")
                valid = False
        if (combat_cfg['fleet_mode'] == 'striking'
                and expeditions_cfg['enabled']):
            if 'fleet3' in expeditions_cfg:
                Util.log_error(
                    "Expedition(s) defined for Fleet 3 while Combat Fleet "
                    "Mode is defined as Striking Fleet.")
                valid = False

        # validate the node selects
        if combat_cfg['raw_node_selects']:
            node_selects = {}
            for raw_node_select in combat_cfg['raw_node_selects']:
                nsm = re.search('([A-Z0-9]+)>([A-Z0-9]+)', raw_node_select)
                if nsm:
                    node_selects[nsm.group(1)] = nsm.group(2)
                else:
                    Util.log_error("Invalid Node Select: '{}'.".format(
                        raw_node_select))
                    valid = False
            if valid and node_selects:
                combat_cfg['node_selects'] = node_selects

        # validate the formations
        if combat_cfg['raw_formations']:
            formations = {}
            valid_formations = ((
                'combinedfleet_1', 'combinedfleet_2', 'combinedfleet_3',
                'combinedfleet_4'
            ) if combat_cfg['fleet_mode'] in ('ctf', 'stf') else (
                'line_ahead', 'double_line', 'diamond', 'echelon',
                'line_abreast', 'vanguard'))

            for raw_formation in combat_cfg['raw_formations']:
                fm = re.search('([A-Z0-9]+):({})'.format(
                    '|'.join(valid_formations)), raw_formation)
                if fm:
                    fm_node = (
                        int(fm.group(1)) if fm.group(1).isdigit()
                        else fm.group(1))
                    formations[fm_node] = fm.group(2)
                else:
                    Util.log_error(
                        "Invalid Formation for fleet mode '{}': '{}'.".format(
                            combat_cfg['fleet_mode'], raw_formation))
                    valid = False
            if valid and formations:
                combat_cfg['formations'] = formations

        # validate the night battles
        if combat_cfg['raw_night_battles']:
            night_battles = {}
            for raw_night_battle in combat_cfg['raw_night_battles']:
                nbm = re.search('([A-Z0-9]+):(True|False)', raw_night_battle)
                if nbm:
                    nbm_node = (
                        int(nbm.group(1)) if nbm.group(1).isdigit()
                        else nbm.group(1))
                    night_battles[nbm_node] = (
                        True if nbm.group(2) == 'True' else False)
                else:
                    Util.log_error("Invalid Night Battle: '{}'.".format(
                        raw_night_battle))
                    valid = False
            if valid and night_battles:
                combat_cfg['night_battles'] = night_battles

        # validate lbas setup
        if combat_cfg['lbas_enabled']:
            for group in (1, 2, 3):
                if combat_cfg['lbas_group_{}_nodes'.format(group)]:
                    if group not in combat_cfg['lbas_groups']:
                        Util.log_error(
                            "LBAS Group {} has nodes assigned to it but is "
                            "not active. Either clear the nodes or activate "
                            "the LBAS Group.".format(group))
                        valid = False
                    elif (len(combat_cfg['lbas_group_{}_nodes'.format(
                            group)]) != 2):
                        Util.log_error(
                            "LBAS Group {} does not have 2 nodes assigned to "
                            "it.".format(group))
                        valid = False

        # validate the misc options
        for option in combat_cfg['misc_options']:
            if option not in (
                    'CheckFatigue', 'ReserveDocks', 'PortCheck', 'ClearStop',
                    'LastNodePush'):
                Util.log_error(
                    "Invalid Combat MiscOption: '{}'.".format(option))
                valid = False

        return valid
