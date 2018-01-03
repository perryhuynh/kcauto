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
        at the top of the screen when at home. Directly calls the
        read_ocr_number_text method then strips all non-number characters
        because Tesseract OCR has issues detecting short number of characters
        that are also white font on black backgrounds. Trick this by capturing
        more of the region than is needed (includes a bit of the bucket icon)
        then stripping out the superfluous/mis-recognized characters.

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
        """Switches the shiplist sorting to the specified target mode. 'first',
        'prev', 'next', 'last' targets will click their respective buttons,
        while an int target between 1 and 5 (inclusive) will click the page
        number at that position at the bottom of the page (left to right).

        Args:
            target (str, int): the sorting to switch the shiplist to
        """
        while not self.regions['top_submenu'].exists(
                'shiplist_sort_{}.png'.format(target)):
            Util.check_and_click(
                self.regions['top_submenu'],
                'shiplist_sort_arrow.png',
                Globals.EXPAND['shiplist_sort'])

    def _change_shiplist_page(self, target):
        if target == 'first':
            Util.check_and_click(
                self.regions['lower'], 'page_first.png',
                Globals.EXPAND['arrow_navigation'])
        elif target == 'prev':
            Util.check_and_click(
                self.regions['lower'], 'page_prev.png',
                Globals.EXPAND['arrow_navigation'])
        elif target == 'next':
            Util.check_and_click(
                self.regions['lower'], 'page_next.png',
                Globals.EXPAND['arrow_navigation'])
        elif target == 'last':
            Util.check_and_click(
                self.regions['lower'], 'page_last.png',
                Globals.EXPAND['arrow_navigation'])
        elif 1 <= target <= 5:
            zero_target = target - 1
            x_start = 512 + (zero_target * 21) + (zero_target * 11)
            x_stop = x_start + 11
            y_start = 444
            y_stop = 452

            Util.click_coords(
                self.kc_region,
                Util.randint_gauss(x_start, x_stop),
                Util.randint_gauss(y_start, y_stop))

    def _navigate_to_shiplist_page(self, target_page):
        if target_page > self.ship_page_count:
            raise Exception(
                "Invalid shiplist target page ({}) for number of known pages "
                "({}).".format(target_page, self.ship_page_count))
        current_page = self.curent_shiplist_page

    def _choose_ship_by_position(self, position):
        """Method that chooses the ship in the specified position in the
        ship list.

        Args:
            position (int): integer between 1 and 10 specifying the position
                that should be clicked on the ship list

        Raises:
            Exception: if position is not between 1 and 10
        """
        if not 1 <= position <= 10:
            raise Exception(
                "Invalid position passed to _choose_ship_by_position: {}"
                .format(position))
        zero_position = position - 1
        # x start/stop do not change
        x_start = 389
        x_stop = 715
        # y start/stop change depending on specified position; region has width
        # of 326 pixels, height of 23 pixels, with a 5-pixel padding between
        # each nth position on the list
        y_start = 156 + (zero_position * 5) + (zero_position * 23)
        y_stop = y_start + 23

        Util.click_coords(
            self.kc_region,
            Util.randint_gauss(x_start, x_stop),
            Util.randint_gauss(y_start, y_stop))
        Util.kc_sleep(1)

    def _check_ship_availability(self):
        ship_not_available = False
        if ship_not_available:
            return False
        return True

    def _resolve_replacement_ship(self):
        self._switch_shiplist_sorting('__TARGET')
        self._navigate_to_shiplist_page(5)
        self._choose_ship_by_position(4)
        if self._check_ship_availability():
            # click switch button
            return True
        else:
            return False
