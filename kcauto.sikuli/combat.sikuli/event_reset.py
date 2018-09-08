from sikuli import Region, Pattern
from kca_globals import Globals
from util import Util


class EventReset(object):
    def __init__(self, config, stats, regions, map_data):
        """Initializes the EventReset module for use in the Combat module.

        Args:
            config (Config): kcauto Config instance
            stats (Stats): kcauto Stats instance
            regions (dict): dict of pre-defined kcauto regions
            map_data (MapData): MapData instance of event map
        """
        self.config = config
        self.stats = stats
        self.regions = regions
        self.map = map_data
        self.kc_region = regions['game']

        # reset on first init
        self.next_reset_sortie = self.stats.combat_done

    def check_need_to_reset(self):
        """Method that checks the need to reset the event map's progress.

        Returns:
            bool: True if the progress needs to be reset, False otherwise
        """

        if self.stats.combat_done >= self.next_reset_sortie:
            Util.log_msg("Reset event map progress.")
            return True
        return False

    def reset_event_map_progress(self):
        """Method that resets the event map progress by switching to the
        Reset difficulty and then back to the Farm difficulty.
        """
        # dismiss first chalkboard on first pass
        Util.click_preset_region(self.regions, 'center')
        self._switch_difficulty(self.config.event_reset['reset_difficulty'])
        # re-initiate chalkboards to finalize reset
        Util.check_and_click(
            self.regions['lower_left'], 'c_world_1.png')
        Util.wait_and_click(
            self.kc_region,
            '_event_world_{}.png'.format(self.map.subworld))
        # dismiss first chalkboard on second pass
        self.regions['lower'].wait('event_chalkboard.png', 10)
        Util.click_preset_region(self.regions, 'center')
        self._switch_difficulty(self.config.event_reset['farm_difficulty'])
        # update internal states
        self.stats.increment_event_resets_done()
        self.next_reset_sortie = (
            self.stats.combat_done + self.config.event_reset['frequency'])
        Util.log_msg("Next event map progress reset after sortie #{}.".format(
            self.next_reset_sortie))

    def _switch_difficulty(self, difficulty):
        """Method that clicks through to execute the difficulty reset to the
        specified difficulty. The starting point for this method should be the
        second event chalkboard, where the button to switch the difficulty
        exists.
        """
        Util.wait_and_click(
            self.regions['upper'], 'event_difficulty_select.png')
        Util.wait_and_click(
            self.kc_region,
            'event_difficulty_{}.png'.format(difficulty))
        Util.wait_and_click(
            self.regions['lower_right'], 'event_difficulty_accept.png')
        self.regions['lower_right'].wait('sortie_select.png')
