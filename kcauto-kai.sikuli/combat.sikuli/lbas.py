from sikuli import Pattern
from threading import Thread
from globals import Globals
from util import Util


class LBAS(object):
    def __init__(self, config, regions, map):
        """Initializes the LBAS module for use in the Combat module.

        Args:
            config (Config): kcauto-kai Config instance
            regions (dict): dict of pre-defined kcauto-kai regions
            map (MapData): MapData instance from the Combat module
        """
        self.config = config
        self.regions = regions
        self.kc_region = regions['game']
        self.map = map
        self.fatigue = {}

    def assign_groups(self):
        """Method for assigning sortied LBAS groups to their respective nodes
        on the sortie map.
        """
        self.kc_region.wait('lbas_panel_ready.png', 10)
        Util.kc_sleep(1)
        Util.log_msg("Assign LBAS groups to nodes.")
        for lbas_group_nodes in (
                'lbas_group_1_nodes', 'lbas_group_2_nodes',
                'lbas_group_3_nodes'):
            if not self.config.combat[lbas_group_nodes]:
                # if no lbas nodes are specified for this group, skip it
                continue

            Util.log_msg(
                "Assigning nodes for LBAS group {}.".format(
                    lbas_group_nodes[11]))
            nodes = self.config.combat[lbas_group_nodes]
            for node in nodes:
                node_obj = self.map.nodes[node]
                lbas_sidebar_pos = 'left'
                lbas_sidebar = self.kc_region.find('lbas_panel_side.png')
                if lbas_sidebar.x > 400:
                    lbas_sidebar_pos = 'right'
                if ((lbas_sidebar_pos == 'left' and node_obj.coords[0] < 350)
                        or (lbas_sidebar_pos == 'right'
                            and node_obj.coords[0] > 450)):
                    self.kc_region.hover('lbas_panel_side.png')
                node_obj.click_node(self.kc_region)
                Util.rejigger_mouse(self.regions, 'lbas')
                Util.kc_sleep()
            Util.check_and_click(
                self.regions['upper'], 'lbas_assign_confirm.png')
            Util.rejigger_mouse(self.regions, 'lbas')

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
        Util.kc_sleep(1)
        for group in self.config.combat['lbas_groups']:
            Util.log_msg("Resupplying LBAS group {}.".format(group))
            if group != 1:
                self.regions['right'].click('lbas_group_tab_{}.png'.format(
                    str(group)))
            Util.check_and_click(self.regions['right'], 'lbas_resupply.png')
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
            return (False, 18)
        if fatigue['medium']:
            return (False, 12)
        return (True, 0)

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
            # lbas group is fatigued; put it in rest mode
            self._switch_lbas_mode('rest')
            fatigue['high'] = (
                group_fatigue['high']
                if group_fatigue['high'] else fatigue['high'])
            fatigue['medium'] = (
                group_fatigue['medium']
                if group_fatigue['medium'] else fatigue['medium'])
        else:
            lbas_group_nodes_key = 'lbas_group_{}_nodes'.format(group)
            # put LBAS group into air defense mode if it is active but no nodes
            # are assigned to it
            group_sortie_mode = (
                'sortie'
                if self.config.combat[lbas_group_nodes_key] else 'defense')
            self._switch_lbas_mode(group_sortie_mode)
        return fatigue

    def _switch_lbas_mode(self, final_mode):
        """Switches the lbas group mode to the specified final mode.

        Args:
            final_mode (str): the mode to switch the LBAS group to
        """
        Util.rejigger_mouse(self.regions, 'top')
        while not self.regions['lbas_mode_switcher'].exists(
                'lbas_group_mode_{}.png'.format(final_mode)):
            Util.click_screen(self.regions, 'lbas_mode_switch_button')
            Util.rejigger_mouse(self.regions, 'top')
            Util.kc_sleep(1)
        Util.log_msg("LBAS group switched to {} mode.".format(final_mode))

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
            if (self.regions['check_lbas_fatigue'].exists(
                Pattern('ship_state_fatigue_{}.png'.format(mode))
                .similar(Globals.FATIGUE_SIMILARITY)))
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
            "LBAS Group {} fatigue state: {}".format(group, fatigue))
