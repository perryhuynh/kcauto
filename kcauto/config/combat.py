from config.config_base import ConfigBase
from constants import MAX_FLEET_PRESETS
from kca_enums.damage_states import DamageStateEnum
from kca_enums.fleet_modes import FleetModeEnum, CombinedFleetModeEnum
from kca_enums.formations import FormationEnum
from kca_enums.lbas_groups import LBASGroupEnum
from kca_enums.maps import MapEnum
from kca_enums.nodes import NodeEnum, NamedNodeEnum


class ConfigCombat(ConfigBase):
    _enabled = False
    _fleet_presets = []
    _sortie_map = None
    _fleet_mode = None
    _retreat_points = []
    _node_selects = {}
    _node_formations = {}
    _node_night_battles = {}
    _push_nodes = []
    _retreat_limit = None
    _repair_limit = None
    _repair_timelimit_hours = None
    _repair_timelimit_minutes = None
    _lbas_groups = []
    _lbas_group_1_nodes = []
    _lbas_group_2_nodes = []
    _lbas_group_3_nodes = []
    _check_fatigue = False
    _check_lbas_fatigue = False
    _reserve_repair_dock = False
    _port_check = False
    _clear_stop = False

    def __init__(self, config):
        super().__init__(config)
        self.enabled = config['combat.enabled']
        self.fleet_presets = config['combat.fleet_presets']
        self.sortie_map = config['combat.sortie_map']
        self.fleet_mode = config['combat.fleet_mode']
        self.retreat_points = config['combat.retreat_points']
        self.node_selects = config['combat.node_selects']
        self.node_formations = config['combat.node_formations']
        self.node_night_battles = config['combat.node_night_battles']
        self.push_nodes = config['combat.push_nodes']
        self.retreat_limit = config['combat.retreat_limit']
        self.repair_limit = config['combat.repair_limit']
        self.repair_timelimit_hours = config['combat.repair_timelimit_hours']
        self.repair_timelimit_minutes = config[
            'combat.repair_timelimit_minutes']
        self.lbas_groups = config['combat.lbas_groups']
        self.lbas_group_1_nodes = config['combat.lbas_group_1_nodes']
        self.lbas_group_2_nodes = config['combat.lbas_group_2_nodes']
        self.lbas_group_3_nodes = config['combat.lbas_group_3_nodes']
        self.check_fatigue = config['combat.check_fatigue']
        self.check_lbas_fatigue = config['combat.check_lbas_fatigue']
        self.reserve_repair_dock = config['combat.reserve_repair_dock']
        self.port_check = config['combat.port_check']
        self.clear_stop = config['combat.clear_stop']

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if type(value) is not bool:
            raise ValueError(
                "Specified value for pvp enabled is not a boolean.")
        self._enabled = value

    @property
    def fleet_presets(self):
        return self._fleet_presets

    @fleet_presets.setter
    def fleet_presets(self, value):
        for preset_id in value:
            if not 0 < preset_id <= MAX_FLEET_PRESETS:
                raise ValueError("Invalid value specified for fleet preset")
        self._fleet_presets = value

    @property
    def sortie_map(self):
        return self._sortie_map

    @sortie_map.setter
    def sortie_map(self, value):
        if not MapEnum.contains_value(value):
            raise ValueError("Invalid map specified")
        self._sortie_map = MapEnum(value)

    @property
    def fleet_mode(self):
        return self._fleet_mode

    @fleet_mode.setter
    def fleet_mode(self, value):
        if not FleetModeEnum.contains_value(value):
            raise ValueError("Invalid fleet mode specified.")
        fleet_mode = FleetModeEnum(value)
        if (
                fleet_mode is not FleetModeEnum.STANDARD
                and len(self.fleet_presets) > 0):
            raise ValueError(
                "Fleet mode must be standard for use with fleet presets.")
        if (
                self._config['combat.enabled']
                and self._config['pvp.enabled']
                and CombinedFleetModeEnum.contains_value(value)):
            raise ValueError(
                "Combat fleet cannot be combined when PvP is enabled")
        if (
                self._config['combat.enabled']
                and CombinedFleetModeEnum.contains_value(value)
                and self._config['expedition.enabled']
                and len(self._config['expedition.fleet_2']) > 0):
            raise ValueError(
                "Combat fleet cannot be combined if expedition 2 fleets are "
                "defined")
        self._fleet_mode = fleet_mode

    @property
    def retreat_points(self):
        return self._retreat_points

    @retreat_points.setter
    def retreat_points(self, value):
        for node in value:
            if not NodeEnum.contains_value(node):
                raise ValueError("Invalid node specified")
        self._retreat_points = [NodeEnum(node) for node in value]

    @property
    def node_selects(self):
        return self._node_selects

    @node_selects.setter
    def node_selects(self, value):
        node_selects = {}
        for select in value:
            split = select.split('>')
            if len(split) != 2:
                raise ValueError("Node select in wrong format.")
            if (
                    not NamedNodeEnum.contains_value(split[0])
                    or not NamedNodeEnum.contains_value(split[1])):
                raise ValueError("Bad node specified in node select.")
            node_selects[split[0]] = NodeEnum(split[1])
        self._node_selects = node_selects

    @property
    def node_formations(self):
        return self._node_formations

    @node_formations.setter
    def node_formations(self, value):
        node_formations = {}
        for formation in value:
            split = formation.split(':')
            split[0] = int(split[0]) if split[0].isdigit() else split[0]
            if len(split) != 2:
                raise ValueError("Node formation in wrong format.")
            if not NodeEnum.contains_value(split[0]):
                raise ValueError("Bad node specified in node formation.")
            if not FormationEnum.contains_value(split[1]):
                raise ValueError("Bad formation specified in node formation.")
            node_formations[split[0]] = FormationEnum(split[1])
        self._node_formations = node_formations

    @property
    def node_night_battles(self):
        return self._node_night_battles

    @node_night_battles.setter
    def node_night_battles(self, value):
        node_night_battles = {}
        for nb in value:
            split = nb.split(':')
            split[0] = int(split[0]) if split[0].isdigit() else split[0]
            if len(split) != 2:
                raise ValueError("Node night battle in wrong format.")
            if not NodeEnum.contains_value(split[0]):
                raise ValueError("Bad node specified in node nb.")
            if split[1] not in ('True', 'False'):
                raise ValueError("Bad bool specified for node nb.")
            node_night_battles[split[0]] = split[1] == 'True'
        self._node_night_battles = node_night_battles

    @property
    def push_nodes(self):
        return self._push_nodes

    @push_nodes.setter
    def push_nodes(self, value):
        for node in value:
            if not NamedNodeEnum.contains_value(node):
                raise ValueError("Invalid node specified for push nodes.")
        self._push_nodes = [NodeEnum(node) for node in value]

    @property
    def retreat_limit(self):
        return self._retreat_limit

    @retreat_limit.setter
    def retreat_limit(self, value):
        if not DamageStateEnum.contains_value(value):
            raise ValueError("Invalid damage state specified")
        self._retreat_limit = DamageStateEnum(value)

    @property
    def repair_limit(self):
        return self._repair_limit

    @repair_limit.setter
    def repair_limit(self, value):
        if not DamageStateEnum.contains_value(value):
            raise ValueError("Invalid damage state specified")
        self._repair_limit = DamageStateEnum(value)

    @property
    def repair_timelimit_hours(self):
        return self._repair_timelimit_hours

    @repair_timelimit_hours.setter
    def repair_timelimit_hours(self, value):
        if type(value) is not int:
            raise ValueError("Invalid time limit hour specified.")
        self._repair_timelimit_hours = value

    @property
    def repair_timelimit_minutes(self):
        return self._repair_timelimit_minutes

    @repair_timelimit_minutes.setter
    def repair_timelimit_minutes(self, value):
        if type(value) is not int:
            raise ValueError("Invalid time limit hour specified.")
        if not 0 <= value <= 59:
            raise ValueError("Invalid minute specified.")
        self._repair_timelimit_minutes = value

    @property
    def lbas_groups(self):
        return self._lbas_groups

    @lbas_groups.setter
    def lbas_groups(self, value):
        for group in value:
            if not LBASGroupEnum.contains_value(group):
                raise ValueError("Invalid lbas group specified")
        self._lbas_groups = [LBASGroupEnum(group) for group in value]

    @property
    def lbas_group_1_nodes(self):
        return self._lbas_group_1_nodes

    @lbas_group_1_nodes.setter
    def lbas_group_1_nodes(self, value):
        if (
                LBASGroupEnum.G01.value in self.lbas_groups
                and len(value) not in (0, 2)):
            raise ValueError("0 or 2 nodes not specified for LBAS 1")
        for node in value:
            if not NamedNodeEnum.contains_value(node):
                raise ValueError("Invalid node specified for LBAS 1")
        self._lbas_group_1_nodes = [NodeEnum(node) for node in value]

    @property
    def lbas_group_2_nodes(self):
        return self._lbas_group_2_nodes

    @lbas_group_2_nodes.setter
    def lbas_group_2_nodes(self, value):
        if (
                LBASGroupEnum.G02.value in self.lbas_groups
                and len(value) not in (0, 2)):
            raise ValueError("0 or 2 nodes not specified for LBAS 2")
        for node in value:
            if not NamedNodeEnum.contains_value(node):
                raise ValueError("Invalid node specified for LBAS 2")
        self._lbas_group_2_nodes = [NodeEnum(node) for node in value]

    @property
    def lbas_group_3_nodes(self):
        return self._lbas_group_3_nodes

    @lbas_group_3_nodes.setter
    def lbas_group_3_nodes(self, value):
        if (
                LBASGroupEnum.G03.value in self.lbas_groups
                and len(value) not in (0, 2)):
            raise ValueError("0 or 2 nodes not specified for LBAS 3")
        for node in value:
            if not NamedNodeEnum.contains_value(node):
                raise ValueError("Invalid node specified for LBAS 3")
        self._lbas_group_3_nodes = [NodeEnum(node) for node in value]

    @property
    def check_fatigue(self):
        return self._check_fatigue

    @check_fatigue.setter
    def check_fatigue(self, value):
        if type(value) is not bool:
            raise ValueError("Check Fatigue is not a bool.")
        self._check_fatigue = value

    @property
    def check_lbas_fatigue(self):
        return self._check_lbas_fatigue

    @check_lbas_fatigue.setter
    def check_lbas_fatigue(self, value):
        if type(value) is not bool:
            raise ValueError("Check LBAS Fatigue is not a bool.")
        self._check_lbas_fatigue = value

    @property
    def reserve_repair_dock(self):
        return self._reserve_repair_dock

    @reserve_repair_dock.setter
    def reserve_repair_dock(self, value):
        if type(value) is not bool:
            raise ValueError("Reserve repair docks is not a bool.")
        self._reserve_repair_dock = value

    @property
    def port_check(self):
        return self._port_check

    @port_check.setter
    def port_check(self, value):
        if type(value) is not bool:
            raise ValueError("Port Check is not a bool.")
        self._port_check = value

    @property
    def clear_stop(self):
        return self._clear_stop

    @clear_stop.setter
    def clear_stop(self, value):
        if type(value) is not bool:
            raise ValueError("Clear Stop is not a bool.")
        self._clear_stop = value

    def nodes_for_lbas_group(self, group):
        if not LBASGroupEnum.contains_value(group):
            raise ValueError("Invalid group id specified")
        return getattr(self, f'lbas_group_{group}_nodes')
