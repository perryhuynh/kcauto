from sikuli import Region, Pattern
from math import ceil
from re import sub
from threading import Thread
from globals import Globals
from fleet import Fleet
from util import Util


# Order by NEW
# - select NTH ship from START/END that is LOCKED/UNLOCKED/EITHER

# Order by LEVEL
# - select NTH ship from START/END that is LOCKED/UNLOCKED/EITHER

# Order by TYPE
# - select ship of TYPE that is LOCKED/UNLOCKED/EITHER
# - (for subs) select specific SHIP of TYPE that is LOCKED/UNLOCKED/EITHER

# [N/L][#][S/E][L/U/E]
# T[L/U/E][SS/SSV/etc]


class ShipSwitcher(object):
    SHIPS_PER_PAGE = 10

    def __init__(self, config, stats, regions, fleets, combat):
        self.config = config
        self.stats = stats
        self.regions = regions
        self.kc_region = regions['game']
        self.ship_count = 1
        self.ship_page_count = 1
        self.ship_last_page_count = 1
        self.current_shiplist_page = 1

    def ship_switch_logic(self):
        self._set_shiplist_counts()
        for i in range(1, 7):
            if self._check_need_to_switch_ship(i):
                self._press_switch_ship_button(i)
                # for '__OPTIONS':
                #     self._resolve_replacement_ship()

    def _set_shiplist_counts(self):
        """Method that sets the ship-list related internal counts based on the
        number of ships in the port
        """
        self.ship_count = self._get_ship_count()
        self.ship_page_count = int(
            ceil(self.ship_count / float(self.SHIPS_PER_PAGE)))
        self.ship_last_page_count = (
            self.ship_count % self.SHIPS_PER_PAGE
            if self.ship_count % self.SHIPS_PER_PAGE is not 0
            else self.SHIPS_PER_PAGE)

    def _get_ship_count(self):
        """Method that returns the number of ships in the port via the counter
        at the top of the screen when at home.

        Returns:
            int: number of ships in port
        """
        a = Util.read_ocr_number_text(
            self.regions['ship_counter'], 'shipcount_label.png', 'r', 48)
        return int(sub(r"\D", "", a))

    def _check_need_to_switch_ship(self, position):
        # check against settings in specific region: damage? fatigue?
        pass

    def _press_switch_ship_button(self, position):
        pass

    def _switch_shiplist_sorting(self, target):
        """Switches the shiplist sorting to the specified target mode.

        Args:
            target (str): the sorting to switch the shiplist to
        """
        while not self.regions['__SHIPLISTICON_REGION'].exists(
                'shiplist_sort_{}.png'.format(target)):
            Util.check_and_click(
                self.regions['__SHIPLISTICON_REGION'],
                'shiplist_sort_arrow.png',
                Globals.EXPAND['shiplist_sort'])
            Util.kc_sleep(1)

    def _change_shiplist_page(self, target):
        if target == 'end':
            pass
        elif target == 'back':
            pass
        elif target == 'forward':
            pass
        elif target == 'start':
            pass

    def _switch_shiplist_page(self, target_page):
        current_page = self.curent_shiplist_page
        pass

    def _choose_ship_by_position(self, position):
        pass

    def _check_ship_availability(self):
        ship_not_available = False
        if ship_not_available:
            return False
        return True

    def _resolve_replacement_ship(self):
        self._switch_shiplist_sorting('__TARGET')
        self._switch_shiplist_page(5)
        self._choose_ship_by_position(4)
        if self._check_ship_availability():
            # click switch button
            return True
        else:
            return False
