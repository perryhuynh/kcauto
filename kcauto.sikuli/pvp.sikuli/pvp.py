from sikuli import Region, Pattern
from datetime import datetime, timedelta
from random import randint
from threading import Thread
from nav import Nav
from util import Util
from kca_globals import Globals


class PvPModule(object):
    def __init__(self, config, stats, regions, fleet):
        """Initialies the PvP module.

        Args:
            config (Config): kcauto Config instance
            stats (Stats): kcauto Stats instance
            regions (dict): dict of pre-defined kcauto regions
            fleets (Fleet): Fleet instance of fleet that will conduct PvP
        """
        self.config = config
        self.stats = stats
        self.regions = regions
        self.kc_region = regions['game']
        self.fleet = fleet
        self.next_pvp_time = None
        self._set_next_pvp_time()
        self.opponent = {}

        x = self.kc_region.x
        y = self.kc_region.y
        self.module_regions = {
            'enemy_pvp_fleet': Region(x + 710, y, 365, Globals.GAME_HEIGHT)
        }

    def goto_pvp(self):
        """Method to navigate to the PvP menu
        """
        Nav.goto(self.regions, 'pvp')

    def check_need_to_pvp(self):
        """Method to check whether or not it is time to PvP.

        Returns:
            boolean: True if it is time to PvP, False otherwise
        """
        if self.next_pvp_time < datetime.now():
            return True
        return False

    def run_pvp_logic(self):
        """Primary PvP logic

        Returns:
            boolean: True if PvP was run, False otherwise
        """
        if not Util.check_and_click(
                self.kc_region, Pattern('pvp_row.png').similar(0.8)):
            Util.log_warning("No PvP opponents available.")
            self._reset_next_pvp_time()
            return False

        self.stats.increment_pvp_attempted()

        Util.rejigger_mouse(self.regions, 'top')
        self.regions['lower_left'].wait('pvp_start_1.png', 30)

        # wait for ship portraits to load to accurately ascertain sub counts
        Util.kc_sleep(2)
        opponent_counts = self._count_ships()
        formation, night_battle = self._pvp_planner(opponent_counts)
        Util.log_msg("PvPing against {:d} ships ({:d} subs).".format(
            opponent_counts['ship'],
            opponent_counts['ss'] + opponent_counts['ssv']))
        Util.log_msg("Selecting {} and {!s} on night battle.".format(
            formation.replace('_', ' '), night_battle))
        # start pvp
        Util.wait_and_click(self.regions['lower_left'], 'pvp_start_1.png', 30)
        Util.wait_and_click(self.regions['lower'], 'pvp_start_2.png', 30)
        Util.log_msg("Beginning PvP sortie.")
        Util.rejigger_mouse(self.regions, 'top')
        Util.wait_and_click(self.regions[formation], formation)

        while not self.regions['lower_right_corner'].exists('next.png', 1 + Globals.SLEEP_MODIFIER):
            if self.kc_region.exists('combat_nb_fight.png', 1 + Globals.SLEEP_MODIFIER):
                if night_battle:
                    Util.check_and_click(self.kc_region, 'combat_nb_fight.png')
                else:
                    Util.check_and_click(self.kc_region, 'combat_nb_retreat.png')
                Util.rejigger_mouse(self.regions, 'top')

        while not self.regions['home_menu'].exists('home_menu_sortie.png', 1 + Globals.SLEEP_MODIFIER):
            if self.regions['lower_right_corner'].exists('next.png', 1 + Globals.SLEEP_MODIFIER):
                Util.check_and_click(self.regions['lower_right_corner'], 'next.png')
                Util.rejigger_mouse(self.regions, 'top')
        self.stats.increment_pvp_done()
        Util.log_msg("Finished PvP sortie.")
        self.fleet.needs_resupply = True
        return True

    def print_status(self):
        """Prints the next PvP time to console.
        """
        Util.log_success("Next PvP sortie at {}".format(
            self.next_pvp_time.strftime('%Y-%m-%d %H:%M:%S')))

    def _set_next_pvp_time(self):
        """Method to set the next PvP time. Called on first instantiation.
        """
        jst_time = Util.convert_to_jst(datetime.now(), self.config)
        if 3 <= jst_time.hour < 5:
            # do not PvP between 3 AM and 5 AM; wait until quests reset at 5AM
            temp_time = jst_time.replace(hour=5)
            self.next_pvp_time = Util.convert_from_jst(temp_time, self.config)
        else:
            self.next_pvp_time = datetime.now()

    def _reset_next_pvp_time(self):
        """Method to reset the next PvP time. Called when the next PvP time
        needs to be reset in subsequent times.
        """
        jst_time = Util.convert_to_jst(datetime.now(), self.config)
        if 5 <= jst_time.hour < 15:
            temp_time = jst_time.replace(hour=15, minute=randint(5, 55))
        elif 15 <= jst_time.hour < 24:
            temp_time = jst_time + timedelta(days=1)
            temp_time = temp_time.replace(hour=5, minute=randint(5, 55))
        else:
            temp_time = jst_time.replace(hour=5, minute=randint(5, 55))
        self.next_pvp_time = Util.convert_from_jst(temp_time, self.config)

    def _pvp_planner(self, opponent):
        """Method to ascertain the formation and night battle of the PvP.

        Args:
            opponent (dict): dict containing number of enemy ships, enemy SSs,
                and enemy SSVs

        Returns:
            str: formation to select
            boolean: True if night battle should be conducted, False otherwise
        """
        formation = 'formation_line_ahead'
        night_battle = True
        if opponent['ship'] == 0:
            # something funky happened here and no ships were detected; use
            # fallback formation and night battle mode
            return (formation, night_battle)

        # determine formation and night battle mode depending on sub ratio of
        # enemy fleet
        sub_ratio = float(opponent['ss'] + opponent['ssv']) / float(
            opponent['ship'])
        if sub_ratio > 0.5:
            formation = 'formation_line_abreast'
        elif sub_ratio == 0.5:
            formation = 'formation_diamond'
        if sub_ratio >= 0.8:
            night_battle = False
        return (formation, night_battle)

    def _count_ships(self):
        """Method to multithread counting of opponent ships.

        Returns:
            dict: dict of enemy ship counts
        """
        t1 = Thread(target=self._count_ships_func, args=('ship', ))
        t2 = Thread(target=self._count_ships_func, args=('ss', ))
        t3 = Thread(target=self._count_ships_func, args=('ssv', ))
        Util.multithreader([t1, t2, t3])
        return self.opponent

    def _count_ships_func(self, mode):
        """Child multithreaded method for counting opponent ships.

        Args:
            mode (str): specifies whether to count ships, SSs, or SSVs
        """
        if mode == 'ship':
            img_target = 'pvp_lvl.png'
        elif mode == 'ss':
            img_target = 'ship_class_ss.png'
        elif mode == 'ssv':
            img_target = 'ship_class_ssv.png'

        self.opponent[mode] = 0
        count = Util.findAll_wrapper(
            self.module_regions['enemy_pvp_fleet'], img_target)

        for i in count:
            self.opponent[mode] += 1
