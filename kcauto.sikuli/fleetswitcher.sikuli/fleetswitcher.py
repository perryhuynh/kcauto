import sys
from sikuli import Region
from kca_globals import Globals
from nav import Nav
from util import Util


class FleetSwitcherModule(object):
    def __init__(self, config, stats, regions):
        """Initializes the FleetSwitcher module.

        Args:
            config (Config): kcauto Config instance
            stats (Stats): kcauto Stats instance
            regions (dict): dict of pre-defined kcauto regions
        """
        self.config = config
        self.stats = stats
        self.regions = regions
        self.kc_region = regions['game']
        self.current_fleet = None
        self.last_combat_fleet = None

    def goto_fleetcomp_presets(self):
        """Method to navigate to the fleet preset recall submenu of the fleet
        composition menu.
        """
        Nav.goto(self.regions, 'fleetcomp')
        Util.check_and_click(
            self.regions['lower_left'], 'fleetswitch_submenu.png')

    def switch_pvp_fleet(self):
        """Method to switch Fleet 1 to the specified PvP preset fleet, if
        necessary.

        Returns:
            bool: True if a switch was done or attempted, False otherwise
        """
        if (self.config.pvp['enabled'] and self.config.pvp['fleet']
                and self.config.pvp['fleet'] != self.current_fleet):
            self.goto_fleetcomp_presets()
            self._recall_preset(self.config.pvp['fleet'])
            return True
        return False

    def switch_combat_fleet(self):
        """Method to switch Fleet 1 to one of the specified combat preset
        fleet, if necessary.

        Returns:
            bool: True if a switch was done or attempted, False otherwise
        """
        if (self.config.combat['enabled']
                and len(self.config.combat['fleets']) > 0):
            if (not self.last_combat_fleet
                    or len(self.config.combat['fleets']) == 1):
                # first combat fleet switch or only one combat fleet specified
                next_combat_fleet = self.config.combat['fleets'][0]
            else:
                # specify next fleet preset from previously used fleet
                temp_index = self.config.combat['fleets'].index(
                    self.last_combat_fleet) + 1
                temp_index = (
                    0 if temp_index == len(self.config.combat['fleets'])
                    else temp_index)
                next_combat_fleet = self.config.combat['fleets'][temp_index]
            if next_combat_fleet != self.current_fleet:
                Util.log_msg("Fleet switch required.")
                self.goto_fleetcomp_presets()
                self._recall_preset(next_combat_fleet)
                self.last_combat_fleet = next_combat_fleet
                return True
        return False

    def _recall_preset(self, preset_id):
        """Method that encompasses the logic to switch the requested fleet by
        its preset_id (1-based); 1 would be the first preset visible in the
        preset recall screen (not to be confused with the preset save screen).
        Please note that failed switch attempts will stop the script.

        Args:
            preset_id (int): which nth preset to switch to (1-based)

        Returns:
            bool: True after successful preset recall
        """
        Util.log_msg("Switching to fleet preset {}.".format(preset_id))
        self._scroll_preset_list(preset_id)
        preset_region = self._generate_preset_list_region(preset_id)
        if not Util.check_and_click(preset_region, 'fleetswitch_button.png'):
            Util.log_error(
                "Could not find fleet preset {}. Please check your config and "
                "fleet prests.".format(preset_id))
            sys.exit(1)
        Util.rejigger_mouse(self.regions, 'top')
        Util.kc_sleep()
        if self.regions['lower_left'].exists('fleetswitch_submenu_exit.png'):
            # still on the fleet preset page, implying that the switch failed
            # due to ships being in other fleets
            Util.log_error(
                "Could not switch in fleet preset {} due to ships being "
                "assigned in other fleets. Please check your config and fleet "
                "presets.".format(preset_id))
            sys.exit(1)
        # successful switch
        self.stats.increment_fleets_switched()
        self.current_fleet = preset_id
        return True

    def _scroll_preset_list(self, preset_id):
        """If necessary, scrolls the preset list to display the desired preset.

        Args:
            preset_id (int): which nth preset to switch to (1-based)
        """
        if preset_id > 5:
            # only scroll if the desired preset is greater than the 5th preset
            scroll_count = preset_id - 5
            for n in range(scroll_count):
                if Util.check_and_click(
                        self.regions['lower_left'], 'scroll_next.png',
                        Globals.EXPAND['scroll_next']):
                    Util.kc_sleep(0.4, 0.2)
                else:
                    Util.log_error(
                        "Could not navigate to fleet preset {}. Please check "
                        "your config and fleet presets.".format(preset_id))
                    sys.exit(1)

    def _generate_preset_list_region(self, preset_id):
        """Method that generates the region to search for the fleet preset
        recall button.

        Args:
            preset_id (int): which nth preset to switch to (1-based)

        Returns:
            Region: Sikuli region to search the fleet preset recall button in
        """
        # preset_id is 1-based, offset is 0-based
        offset = 4 if preset_id > 5 else preset_id - 1
        return Region(
            self.kc_region.x + 415,
            self.kc_region.y + 280 + (offset * 76), 60, 40)
