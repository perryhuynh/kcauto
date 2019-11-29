import config.config_core as cfg
from kca_enums.lbas_fatigue import LBASFatigueEnum
from kca_enums.lbas_groups import LBASGroupEnum
from kca_enums.lbas_state import LBASStateEnum


class LBASGroup(object):
    group_id = None
    config_enabled = False
    api_enabled = False
    state = None
    planes = []

    def __init__(self, group_id):
        self.group_id = group_id

    @property
    def is_active(self):
        return self.api_enabled and self.config_enabled

    @property
    def needs_resupply(self):
        if not self.is_active:
            return False
        for plane in self.planes:
            if plane['count'] < plane['count_max']:
                return True
        return False

    @property
    def needs_rest(self):
        if not self.is_active or not cfg.config.combat.check_lbas_fatigue:
            return False
        if self.highest_fatigue > LBASFatigueEnum.NO_FATIGUE:
            return True
        return False

    @property
    def highest_fatigue(self):
        highest_fatigue = LBASFatigueEnum.NO_FATIGUE
        for plane in self.planes:
            if plane['fatigue'] > highest_fatigue:
                highest_fatigue = plane['fatigue']
        return highest_fatigue

    @property
    def desired_group_state(self):
        if not self.is_active:
            return self.state
        if self.needs_rest:
            return LBASStateEnum.REST

        group_node_size = len(
            cfg.config.combat.nodes_for_lbas_group(self.group_id))
        if LBASGroupEnum(self.group_id) in cfg.config.combat.lbas_groups:
            if group_node_size == 2:
                return LBASStateEnum.SORTIE
            elif group_node_size == 0:
                return LBASStateEnum.AIR_DEFENSE
        return LBASStateEnum.STANDBY
