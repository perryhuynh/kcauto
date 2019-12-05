import api.api_core as api
import config.config_core as cfg
import util.kca as kca_u
from combat.lbas_group import LBASGroup
from util.logger import Log
from kca_enums.kcsapi_paths import KCSAPIEnum
from kca_enums.lbas_fatigue import LBASFatigueEnum
from kca_enums.lbas_groups import LBASGroupEnum
from kca_enums.lbas_state import LBASStateEnum


class LBASCore(object):
    groups = {}

    def __init__(self):
        self.enabled = (
            True
            if len(cfg.config.combat.lbas_groups) > 0
            else False)
        for group in LBASGroupEnum:
            self.groups[group.value] = LBASGroup(int(group.value))

    def update_lbas_groups(self, data):
        Log.log_debug("Updating LBAS group data from API.")
        for group in LBASGroupEnum:
            self.groups[group.value].api_enabled = False

        sortie_world = cfg.config.combat.sortie_map.world
        for group in data:
            if sortie_world == 'E' and group['api_area_id'] < 40:
                continue
            elif sortie_world == '6' and group['api_area_id'] != 6:
                continue

            group_id = group['api_rid']
            group_instance = self.groups[group_id]
            group_instance.api_enabled = True
            group_instance.config_enabled = (
                True
                if LBASGroupEnum(group_id) in cfg.config.combat.lbas_groups
                else False)
            group_instance.state = LBASStateEnum(group['api_action_kind'])
            planes = []
            for plane in group['api_plane_info']:
                if plane['api_state'] == 0:
                    continue
                planes.append({
                    'fatigue': LBASFatigueEnum(plane['api_cond']),
                    'count': plane['api_count'],
                    'count_max': plane['api_max_count']
                })
            group_instance.planes = planes

    def manage_lbas(self):
        if not self.enabled:
            return False

        resupply_groups = self._groups_to_resupply
        switch_state_groups = self._groups_to_switch_state
        rest_groups = self._groups_to_rest
        if resupply_groups or switch_state_groups:
            Log.log_msg("Managing LBAS groups.")
            self._open_lbas_panel()
            for group in LBASGroupEnum:
                group_id = group.value
                group_instance = self.groups[group_id]
                if not group_instance.is_active:
                    continue

                if group_id != 1:
                    kca_u.kca.click_existing(
                        'upper_right', f'combat|lbas_group_tab_{group_id}.png')
                    kca_u.kca.sleep(1)
                if group_id in resupply_groups:
                    self._resupply(group_id)
                if group_id in switch_state_groups:
                    self._set_to_desired_state(
                        group_instance.state,
                        group_instance.desired_group_state)
            kca_u.kca.sleep(0.5)
            kca_u.kca.click_existing('lower_left', 'combat|c_world_1.png')
            kca_u.kca.sleep(1)

        if rest_groups:
            return self._time_to_rest

    def assign_lbas(self, map_data):
        if not self.enabled:
            return False

        Log.log_msg("Assigning LBAS groups.")
        kca_u.kca.r['lbas'].hover()
        for group in self.assignable_lbas_groups:
            nodes = cfg.config.combat.nodes_for_lbas_group(group.group_id)
            Log.log_msg(
                f"Assigning group {group.group_id} to nodes {nodes[0].value} "
                f"and {nodes[1].value}.")
            for node in nodes:
                node_instance = map_data.nodes[node.value]
                panel = kca_u.kca.wait(
                    'kc', 'combat|lbas_panel_side.png', wait=90)
                panel_pos = 'r' if panel.x - kca_u.kca.game_x > 600 else 'l'
                if (
                        (panel_pos == 'l' and node_instance.x < 420)
                        or (panel_pos == 'r' and node_instance.x > 780)):
                    kca_u.kca.hover(panel)
                node_instance.select()
                kca_u.kca.sleep()
            kca_u.kca.r['lbas'].hover()
            kca_u.kca.click_existing('upper', 'combat|lbas_assign_confirm.png')
            kca_u.kca.r['lbas'].hover()
            kca_u.kca.sleep(1)

    def _lbas_panel_check_cond(self):
        return (
            True
            if (
                kca_u.kca.exists('upper_right', 'combat|lbas_group_tab_1.png')
                or kca_u.kca.exists(
                    'upper_right', 'combat|lbas_group_tab_1_only.png'))
            else False)

    def _open_lbas_panel(self):
        if cfg.config.combat.sortie_map.world == 'E':
            kca_u.kca.click_existing(
                'lower_left', 'combat|lbas_resupply_menu_button_event.png')
            kca_u.kca.sleep()
            kca_u.kca.while_wrapper(self._lbas_panel_check_cond, timeout=10)
        else:
            kca_u.kca.click_existing(
                'upper_right', 'combat|lbas_resupply_menu_button.png')
            kca_u.kca.sleep()
            kca_u.kca.wait('upper_right', 'combat|lbas_group_tab_1.png')
        kca_u.kca.sleep()

    def _lbas_panel_resupply_cond(self):
        return (
            True
            if not kca_u.kca.exists('upper_right', 'combat|lbas_resupply.png')
            else False)

    def _lbas_panel_resupply_func(self):
        kca_u.kca.click_existing(
            'upper_right', 'combat|lbas_resupply.png', cached=True)
        kca_u.kca.sleep(0.1)

    def _resupply(self, group_id):
        Log.log_msg(f"Resupplying LBAS group {group_id}.")
        kca_u.kca.while_wrapper(
            self._lbas_panel_resupply_cond, self._lbas_panel_resupply_func,
            timeout=10)

        kca_u.kca.wait_vanish(
            'lower_right', 'combat|lbas_resupply_in_progress.png')
        kca_u.kca.sleep()

    def _set_to_desired_state(self, start, stop):
        if start is stop:
            return
        Log.log_msg(
            f"Switching LBAS state from {start.display_name} to "
            f"{stop.display_name}.")
        state_order = list(LBASStateEnum)
        idx = state_order.index(start)
        relative_order = state_order[idx:] + state_order[:idx]
        for idx, state in enumerate(relative_order):
            if state is stop:
                break
            Log.log_debug(
                f"Switching LBAS state from {state.display_name} to "
                f"{relative_order[idx + 1].display_name}.")
            cur_name = state.name.lower()
            next_name = relative_order[idx + 1].name.lower()
            kca_u.kca.click_existing(
                'upper_right', f'combat|lbas_group_mode_{cur_name}.png')
            kca_u.kca.r['top'].hover()
            kca_u.kca.wait(
                'upper_right', f'combat|lbas_group_mode_{next_name}.png')
            kca_u.kca.sleep(0.5)
        api.api.update_from_api({KCSAPIEnum.SORTIE_ASSIGN_LBAS})

    @property
    def assignable_lbas_groups(self):
        groups = []
        for group in LBASGroupEnum:
            group_instance = self.groups[group.value]
            group_node_size = len(
                cfg.config.combat.nodes_for_lbas_group(group.value))
            if (
                    group_instance.api_enabled
                    and group_instance.config_enabled
                    and group_node_size == 2):
                groups.append(group_instance)
        return groups

    @property
    def _groups_to_resupply(self):
        groups = []
        for group_id in self.groups:
            group = self.groups[group_id]
            if group.needs_resupply:
                groups.append(group_id)
        return groups

    @property
    def _groups_to_switch_state(self):
        groups = []
        for group_id in self.groups:
            group = self.groups[group_id]
            if group.state is not group.desired_group_state:
                groups.append(group_id)
        return groups

    @property
    def _groups_to_rest(self):
        groups = []
        for group_id in self.groups:
            group = self.groups[group_id]
            if group.needs_rest:
                groups.append(group_id)
        return groups

    @property
    def _time_to_rest(self):
        highest_fatigue = LBASFatigueEnum.NO_FATIGUE
        for group_id in self.groups:
            group = self.groups[group_id]
            if group.needs_rest:
                if group.highest_fatigue > highest_fatigue:
                    highest_fatigue = group.highest_fatigue

        if highest_fatigue is LBASFatigueEnum.MEDIUM_FATIGUE:
            return 9
        if highest_fatigue is LBASFatigueEnum.HEAVY_FATIGUE:
            return 15
        return False


lbas = LBASCore()
