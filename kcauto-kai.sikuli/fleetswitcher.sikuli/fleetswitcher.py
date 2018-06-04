from sikuli import Region, Pattern
from kca_globals import Globals
from nav import Nav
from util import Util


class FleetSwitcher(object):
    def __init__(self, config, stats, regions):
        """Initializes the FleetSwitcher module.

        Args:
            config (Config): kcauto-kai Config instance
            stats (Stats): kcauto-kai Stats instance
            regions (dict): dict of pre-defined kcauto-kai regions
        """
        self.config = config
        self.stats = stats
        self.regions = regions
        self.kc_region = regions['game']

    def goto_fleetcomp_presets(self):
        """Method to navigate to the fleet preset recall submenu of the fleet
        composition menu.
        """
        Nav.goto(self.regions, 'fleetcomp')
        self.regions['upper'].wait('shiplist_button.png', 10)
        Util.wait_and_click_and_wait(
            self.regions['lower_left'],
            Pattern('fleetswitch_submenu.png').exact(),
            self.regions['lower_left'],
            Pattern('fleetswitch_submenu_active.png').exact())

    def recall_preset(self, preset_id):
        """Method that encompasses the logic to switch the requested fleet by
        its preset_id (1-based); 1 would be the first preset visible in the
        preset recall screen (not to be confused with the preset save screen).

        Args:
            preset_id (int): which nth preset to switch to (1-based)

        Returns:
            bool: True after successful preset recall
        """
        self._scroll_preset_list(preset_id)
        preset_region = self._generate_preset_list_region(preset_id)
        Util.wait_and_click_and_wait(
            preset_region, 'fleetswitch_button.png',
            self.regions['upper'], 'shiplist_button.png')
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
                Util.check_and_click(
                    self.regions['lower_left'], 'scroll_next.png',
                    Globals.EXPAND['scroll_next'])
                Util.kc_sleep(0.4, 0.2)


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
        return Region(275, 185 + (offset * 52), 45, 29)
