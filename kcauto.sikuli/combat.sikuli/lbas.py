from sikuli import Region, Pattern
from threading import Thread
from kca_globals import Globals
from util import Util


class LBAS(object):
    # Must be relevant to:
    # http://kancolle.wikia.com/wiki/Land_Base_Aerial_Support#Options
    _LBAS_GROUP_MODES = ("standby", "sortie", "defense", "retreat", "rest")

    def __init__(self, config, regions, sortie_map_data):
        """Initializes the LBAS module for use in the Combat module.

        Args:
            config (Config): kcauto Config instance
            regions (dict): dict of pre-defined kcauto regions
            sortie_map_data (MapData): MapData instance from the Combat module
        """
        self.config = config
        self.regions = regions
        self.kc_region = regions['game']
        self.map = sortie_map_data
        self.fatigue = {}

        # lbas-related regions
        x = self.kc_region.x
        y = self.kc_region.y
        self.module_regions = {
            'check_lbas_fatigue': Region(x + 850, y + 350, 55, 330),
            'lbas_mode_switcher': Region(x + 1135, y + 200, 55, 80)
        }

    def assign_groups(self):
        """Method for assigning sortied LBAS groups to their respective nodes
        on the sortie map.
        """
        Util.wait_until_appears(self.regions["upper"], "lbas_panel_ready.png")
        Util.log_msg("Assign LBAS groups to nodes.")
        for key in (1, 2, 3):
            lbas_group_nodes = "lbas_group_{}_nodes".format(key)
            if not self.config.combat[lbas_group_nodes]:
                # if no lbas nodes are specified for this group, skip it
                continue
            Util.log_msg("Assigning nodes for LBAS group #{}.".format(
                lbas_group_nodes[11]))
            nodes = self.config.combat[lbas_group_nodes]
            for node in nodes:
                node_obj = self.map.nodes[node]
                lbas_sidebar_pos = "left"
                lbas_panel_side = Util.wait_until_appears(
                    self.kc_region, "lbas_panel_side.png")
                if lbas_panel_side.x > 600:
                    lbas_sidebar_pos = "right"
                if ((lbas_sidebar_pos == 'left' and
                     node_obj.coords[0] < 420) or
                        (lbas_sidebar_pos == 'right' and
                         node_obj.coords[0] > 780)):
                    self.kc_region.hover('lbas_panel_side.png')
                node_obj.click_node(self.kc_region)
                Util.rejigger_mouse(self.regions, 'lbas')
                Util.kc_sleep()
            self.regions['upper'].click('lbas_assign_confirm.png')
            Util.rejigger_mouse(self.regions, 'lbas')
            Util.kc_sleep(1)

    def resupply_groups(self, check_fatigue):
        """Method for resupplying the LBAS groups. If check_fatigue is set to
        True, this method will also resolve the LBAS fatigue, set their LBAS
        mode to 'rest' to speed up morale recovery, and delay the sortie if
        necessary.

        Args:
            check_fatigue (bool): whether or not LBAS fatigue should be handled

        Returns:
            bool: True if LBAS groups are ready to be sortied, False otherwise
            int: number of minutes to delay the sortie by
        """
        # reset temporary fatigue tracker
        fatigue = {
            'high': False,
            'medium': False
        }
        Util.log_msg("Begin resupplying LBAS groups.")
        if self.config.combat['map'][0] == 'E':
            resupply_menu_button = 'lbas_resupply_menu_button_event.png'
            resupply_menu_button_faded = (
                'lbas_resupply_menu_button_faded_event.png')
            resupply_menu_button_region = self.regions['lower_left']
        else:
            resupply_menu_button = 'lbas_resupply_menu_button.png'
            resupply_menu_button_faded = (
                'lbas_resupply_menu_button_faded.png')
            resupply_menu_button_region = self.regions['top_submenu']

        Util.wait_and_click_and_wait(
            resupply_menu_button_region,
            resupply_menu_button,
            resupply_menu_button_region,
            Pattern(resupply_menu_button_faded).exact())
        Util.kc_sleep(3)
        for group in self.config.combat['lbas_groups']:
            Util.log_msg("Checking LBAS group #{} state.".format(group))
            if group != 1:
                self.regions['right'].click('lbas_group_tab_{}.png'.format(
                    str(group)))
                Util.kc_sleep()
            if Util.check_and_click(
                    self.regions['right'], 'lbas_resupply.png'):
                Util.log_msg("Resupplying LBAS group #{}.".format(group))
                self.regions['right'].waitVanish('lbas_resupply.png', 10)
            if check_fatigue:
                fatigue = self._check_and_manage_lbas_fatigue(fatigue, group)
            Util.kc_sleep(1)
        Util.kc_sleep(1)
        Util.wait_and_click_and_wait(
            resupply_menu_button_region,
            resupply_menu_button_faded,
            resupply_menu_button_region,
            Pattern(resupply_menu_button).exact())
        Util.kc_sleep(1)
        if fatigue['high']:
            return False, 18
        if fatigue['medium']:
            return False, 12
        return True, 0

    def _check_and_manage_lbas_fatigue(self, fatigue, group):
        """Checks LBAS group fatigue and manages its LBAS mode appropriately.

        Args:
            fatigue (dict): fatigue counter
            group (int): LBAS group ID

        Returns:
            dict: updated fatigue counter
        """
        group_fatigue = self._check_fatigue()
        self.print_fatigue_states(group)
        if group_fatigue['high'] or group_fatigue['medium']:
            Util.log_warning(
                "LBAS Group #{} is fatigued, sortie cancelled.".format(group))
            self._switch_lbas_mode('rest')
            fatigue['high'] = (
                group_fatigue['high']
                if group_fatigue['high'] else fatigue['high'])
            fatigue['medium'] = (
                group_fatigue['medium']
                if group_fatigue['medium'] else fatigue['medium'])
        else:
            Util.log_msg("LBAS Group #{} has good morale.".format(group))
            lbas_group_nodes_key = 'lbas_group_{}_nodes'.format(group)
            # put LBAS group into air defense mode if it is active but no nodes
            # are assigned to it
            group_sortie_mode = (
                'sortie'
                if self.config.combat[lbas_group_nodes_key] else 'defense')
            Util.log_msg("Assigning LBAS Group #{} to {} mode.".format(
                group, group_sortie_mode))
            self._switch_lbas_mode(group_sortie_mode)
        return fatigue

    def _switch_lbas_mode(self, target_mode):
        """Switches the lbas group mode to the specified final mode.

        Args:
            target_mode (str): the mode to switch the LBAS group to
        """
        if target_mode not in self._LBAS_GROUP_MODES:
            raise ValueError("No such LBAS Group mode: \"{}\".".format(
                target_mode))
        Util.rejigger_mouse(self.regions, "top")
        idx = 0
        for idx, available_mode in enumerate(self._LBAS_GROUP_MODES):
            if Util.region_contains(
                    self.module_regions["lbas_mode_switcher"],
                    "lbas_group_mode_{}.png".format(available_mode)):
                break
        expected_modes = self._LBAS_GROUP_MODES[
                         idx:] + self._LBAS_GROUP_MODES[:idx]
        for idx, current_mode in enumerate(expected_modes):
            Util.log_msg(
                "Current LBAS Group mode: \"{}\".".format(current_mode))
            if current_mode == target_mode:
                break
            Util.check_and_click(self.module_regions["lbas_mode_switcher"],
                                 "lbas_group_mode_{}.png".format(current_mode))
            Util.rejigger_mouse(self.regions, "top")
            try:
                next_mode = expected_modes[idx + 1]
            except IndexError:
                next_mode = expected_modes[0]
            Util.wait_until_appears(self.module_regions["lbas_mode_switcher"],
                                    "lbas_group_mode_{}.png".format(next_mode))
        Util.log_msg("LBAS Group switched to {} mode.".format(target_mode))

    def _check_fatigue(self):
        """Method to multithread detection of LBAS group fatigue states.

        Returns:
            dict: updated fatigue counter dict
        """
        # reset fatigue
        thread_check_low_fatigue = Thread(
            target=self._check_fatigue_func, args=('medium', ))
        thread_check_high_fatigue = Thread(
            target=self._check_fatigue_func, args=('high', ))
        Util.multithreader([
            thread_check_low_fatigue, thread_check_high_fatigue])
        return self.fatigue

    def _check_fatigue_func(self, mode):
        """Child multithreaded method for fatigue states.

        Args:
            mode (str): which fatigue state to check for
        """
        self.fatigue[mode] = (
            True
            if (self.module_regions['check_lbas_fatigue'].exists(
                Pattern('ship_state_fatigue_{}.png'.format(mode)).similar(
                    Globals.FATIGUE_SIMILARITY)))
            else False)

    def print_fatigue_states(self, group):
        """Method to report the LBAS Group's fatigue state in a more
        human-readable format
        """
        fatigue = 'Rested'
        if self.fatigue['high']:
            fatigue = 'High'
        elif self.fatigue['medium']:
            fatigue = 'Medium'
        Util.log_msg(
            "LBAS Group #{} fatigue state: \"{}\"".format(group, fatigue))
