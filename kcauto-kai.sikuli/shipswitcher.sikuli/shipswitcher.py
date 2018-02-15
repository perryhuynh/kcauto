from sikuli import Region, Pattern
from math import ceil
from re import sub
from threading import Thread
from globals import Globals
from fleet import Fleet
from util import Util


# Order by NEW
# - select NTH ship from END

# Order by LEVEL
# - select NTH ship from START/END that is LOCKED/UNLOCKED/EITHER

# Order by TYPE
# - select ship of TYPE that is LOCKED/UNLOCKED/EITHER
# - (for subs) select specific SHIP of TYPE that is LOCKED/UNLOCKED/EITHER

# [N/L][#][S/E][L/U/E]
# T[L/U/E][SS/SSV/etc]

# { slot: 1, ships: { sort order: 'new', offset: 50 }, {...} }
# { slot: 1, ships: { sort order: 'new', start_offset: 50 }, {...} }
# { slot: 1, ships: {sort order: 'level', start_offset: 50, class: 'sub', level: '<50'} }
# { slot: 1, ships: {sort order: 'type', class: 'sub', level: '<50', locked: True } }
# slot, order, class (only when sorting on class), level, locked, sparkled
# switch_criteria (damage, fatigue, sparkled)
# TODO: ADD "CUSTOM" SHIP-SPECIFIC SUPPORT
# TODO: cache page position for class and custom
# TODO: account for if matching ship cannot be found for class and custom


class ShipSwitcher(object):
    SHIPS_PER_PAGE = 10

    def __init__(self, config, stats, regions, fleets, combat):
        self.config = config
        self.stats = stats
        self.regions = regions
        self.kc_region = regions['game']
        self.fleets = fleets
        self.ship_count = 1
        self.ship_page_count = 1
        self.ship_last_page_count = 1
        self.current_shiplist_page = 1
        self.config.ship_switcher = {
            'enabled': True,
            3: {
                'slot': 3,
                'ships': [
                    {'sort_order': 'new', 'offset_ref': 'end', 'offset': 20},
                    {'sort_order': 'new', 'offset_ref': 'start', 'offset': 32},
                ],
                'criteria': {
                    'damage': 'minor'
                }
            },
            1: {
                'slot': 1,
                'ships': [
                    {'sort_order': 'type', 'class': 'ss', 'level': '>20'}
                ],
                'criteria': {
                    'sparkle': True
                }
            }
        }
        x = self.kc_region.x
        y = self.kc_region.y
        self.class_start_cache = {}
        self.matched_ship_position_cache = []
        self.shipswitcher_regions = {
            'panels': [],
            'shiplist_class_col': Region(x + 360, y + 120, 120, 315),
            'shiplist_class_ship_cols': Region(x + 360, y + 120, 190, 315),
        }
        for slot in range(0, 6):
            self.shipswitcher_regions['panels'].append(Region(
                x + 121 + (352 * (slot % 2)),
                y + 135 + (113 * (slot / 2)),
                330, 110))

    def ship_switch_logic(self):
        self._set_shiplist_counts()
        self.current_shiplist_page = 1
        for slot in range(0, 6):
            if slot not in self.config.ship_switcher:
                print('skipping slot {}'.format(slot))
                continue
            slot_config = self.config.ship_switcher[slot]
            if self._check_need_to_switch_ship(slot, slot_config['criteria']):
                Util.wait_and_click_and_wait(
                    self.shipswitcher_regions['panels'][slot],
                    'shiplist_button.png',
                    self.regions['lower_right'],
                    'page_first.png')
                Util.rejigger_mouse(self.regions, 'top')
                if not self._resolve_replacement_ship(slot_config):
                    Util.check_and_click(
                        self.regions['top_submenu'], 'fleet_1_active.png')

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

    def _check_need_to_switch_ship(self, slot, criteria):
        panel_regions = self.shipswitcher_regions['panels']
        if 'damage' in criteria:
            if panel_regions[slot].exists(
                    'ship_state_dmg_{}.png'.format(criteria['damage'])):
                return True
        if 'fatigue' in criteria:
            if panel_regions[slot].exists('__LOW_MORALE.png'):
                return True
        if 'sparkle' in criteria:
            print('checking for sparkle')
            if panel_regions[slot].exists('sparkle_indicator.png', 2):
                return True
        return False

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
        current_page = self.current_shiplist_page
        print("current page: {}".format(current_page))
        while target_page != current_page:
            page_delta = target_page - current_page
            if (target_page <= 5
                    and (current_page <= 3 or self.ship_page_count <= 5)):
                self._change_shiplist_page(target_page)
                current_page = target_page
            elif (current_page >= self.ship_page_count - 2
                    and target_page >= self.ship_page_count - 4):
                self._change_shiplist_page(
                    abs(self.ship_page_count - target_page - 5))
                current_page = target_page
            elif -3 < page_delta < 3:
                self._change_shiplist_page(3 + page_delta)
                current_page = current_page + page_delta
            elif page_delta <= - 3:
                if target_page <= 5:
                    self._change_shiplist_page('first')
                    current_page = 1
                else:
                    self._change_shiplist_page('prev')
                    current_page -= 5
            elif page_delta >= 3:
                if target_page > self.ship_page_count - 5:
                    self._change_shiplist_page('last')
                    current_page = self.ship_page_count
                else:
                    self._change_shiplist_page('next')
                    current_page += 5
        self.current_shiplist_page = current_page

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
        x_stop = 700
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

    def _check_ship_availability(self, criteria):
        if self.regions['upper_right'].exists('ship_state_dmg_heavy.png'):
            return False
        return Util.check_and_click(
            self.regions['lower_right'], 'shiplist_ship_switch_button.png')

    def _resolve_ship_page_and_position(self, reference, offset):
        if reference == 'start':
            start_offset = offset
        if reference == 'end':
            start_offset = self.ship_count - offset + 1
        page = int(ceil(start_offset / float(self.SHIPS_PER_PAGE)))
        position = (
            start_offset % self.SHIPS_PER_PAGE
            if start_offset % self.SHIPS_PER_PAGE is not 0
            else self.SHIPS_PER_PAGE)
        return (page, [position])

    def _resolve_ship_position(self, ship_config):
        ship_position_temp = []
        matched_ships = Util.findAll_wrapper(
            self.shipswitcher_regions['shiplist_class_col'],
            'shiplist_class_{}.png'.format(ship_config['class']))
        for ship in matched_ships:
            criteria_matched = True
            ship_row = ship.left(1).right(435)
            ship_row.setAutoWaitTimeout(0)  # speed
            position = (ship_row.y - self.kc_region.y - 129) / 28
            if 'locked' in ship_config and criteria_matched:
                ship_locked = (
                    True if ship_row.exists('shiplist_lock.png') else False)
                criteria_matched = (
                    True if ship_config['locked'] == ship_locked else False)
            if 'ringed' in ship_config and criteria_matched:
                ship_ringed = (
                    True if ship_row.exists('shiplist_ring.png') else False)
                criteria_matched = (
                    True if ship_config['ringed'] == ship_ringed else False)
            if 'level' in ship_config and criteria_matched:
                level_area = Region(
                    ship_row.x + 160, ship_row.y, 50, ship_row.h)
                ship_level = Util.read_ocr_number_text(level_area)
                ship_level = 1 if not ship_level else ship_level
                if ship_config['level'][0] == '<':
                    criteria_matched = (
                        True if ship_level <= int(ship_config['level'][1:])
                        else False)
                if ship_config['level'][0] == '>':
                    criteria_matched = (
                        True if ship_level >= int(ship_config['level'][1:])
                        else False)
            if criteria_matched:
                ship_position_temp.append(position)
        ship_position_temp.sort()
        return ship_position_temp

    def _choose_and_check_availability_of_ship(self, position, criteria):
        self._choose_ship_by_position(position)
        if self._check_ship_availability(criteria):
            return True
        Util.check_and_click(
            self.regions['lower_right'], 'page_first.png')
        return False

    def _resolve_replacement_ship(self, slot_config):
        positions = []
        for ship in slot_config['ships']:
            self._switch_shiplist_sorting(ship['sort_order'])
            if 'offset_ref' in ship and 'offset' in ship:
                page, positions = self._resolve_ship_page_and_position(
                    ship['offset_ref'], ship['offset'])
                self._navigate_to_shiplist_page(page)
            if 'class' in ship:
                while not positions and self.current_shiplist_page < self.ship_page_count:
                    positions = self._resolve_ship_position(ship)
                    if not positions:
                        self._navigate_to_shiplist_page(self.current_shiplist_page + 1)

            for position in positions:
                if self._choose_and_check_availability_of_ship(
                        position, slot_config['criteria']):
                    return True
        return False
