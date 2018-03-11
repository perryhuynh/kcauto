from sikuli import Region, Pattern
from math import ceil
from re import sub
from threading import Thread
from kca_globals import Globals
from nav import Nav
from util import Util


class ShipSwitcher(object):
    SHIPS_PER_PAGE = 10

    def __init__(self, config, stats, regions, fleets, combat):
        self.config = config
        self.stats = stats
        self.regions = regions
        self.kc_region = regions['game']
        self.fleets = fleets
        self.combat = combat

        self.ship_count = 1
        self.ship_page_count = 1
        self.ship_last_page_count = 1
        self.current_shiplist_page = 1
        self.temp_ship_config_dict = {}
        self.temp_ship_position_dict = {}
        self.position_cache = {}
        self.sparkling_cache = {}

        x = self.kc_region.x
        y = self.kc_region.y
        self.module_regions = {
            'panels': [],
            'shiplist_class_col': Region(x + 350, y + 150, 200, 285),
        }
        for slot in range(0, 6):
            # create panel regions per slot
            panel_region = Region(
                x + 121 + (352 * (slot % 2)),
                y + 135 + (113 * (slot / 2)),
                330, 110)
            panel_region.setAutoWaitTimeout(0)
            self.module_regions['panels'].append(panel_region)

            # set sparkle check points per relevant slot
            if slot not in self.config.ship_switcher:
                continue
            slot_config = self.config.ship_switcher[slot]
            if 'sparkle' in slot_config['criteria']:
                self._set_sparkle_cache(slot)

    def goto_fleetcomp(self):
        """Method to navigate to the fleet composition menu.
        """
        Nav.goto(self.regions, 'fleetcomp')
        self.module_regions['panels'][0].wait('shiplist_button.png', 2)
        self.current_shiplist_page = 1

    def check_need_to_switch(self):
        fleet = self.fleets[1]
        if fleet.damage_counts['repair'] > 0:
            # if ships are being repaired, attempt switch
            return True
        if fleet.get_damage_counts_at_threshold(
                self.config.combat['repair_limit']) > 0:
            # if ships are damaged at or above threshold, attempt switch
            return True
        if 'CheckFatigue' in self.config.combat['misc_options']:
            if fleet.fatigue['medium'] > 0 or fleet.fatigue['high'] > 0:
                # if ships are known to be fatigued, attempt switch
                return True
        for slot in self.sparkling_cache:
            if self.sparkling_cache[slot] <= self.stats.combat_done:
                # if a ship being sparkled has run the required number of
                # sorties, attempt switch
                return True
        return False

    def ship_switch_logic(self):
        """Primary logic loop which goes through the 6 ship slots and switches
        ships as necessary. Only avilable for Fleet 1.
        """
        self._set_shiplist_counts()
        # loop through slots and switch ships as necessary
        for slot in range(0, 6):
            if slot not in self.config.ship_switcher:
                continue
            slot_config = self.config.ship_switcher[slot]
            if self._check_need_to_switch_ship(slot, slot_config['criteria']):
                Util.wait_and_click_and_wait(
                    self.module_regions['panels'][slot],
                    'shiplist_button.png',
                    self.regions['lower_right'],
                    'page_first.png')
                Util.rejigger_mouse(self.regions, 'top')
                if self._resolve_replacement_ship(slot_config):
                    self.stats.increment_ships_switched()
                    if 'sparkle' in slot_config['criteria']:
                        # if this is a sparkle slot, update the sparkle cache
                        self._set_sparkle_cache(slot)
                else:
                    Util.check_and_click(
                        self.regions['top_submenu'], 'fleet_1_active.png')
                self.module_regions['panels'][0].wait('shiplist_button.png', 2)

        # check new fleet status
        # TODO: only checks on damage and repair states only, not fatigue!
        Util.kc_sleep(2)
        fleet = self.fleets[1]
        damage_counts = fleet.check_damages(self.kc_region)
        if (fleet.get_damage_counts_at_threshold(
                self.config.combat['repair_limit']) == 0 and
                damage_counts['repair'] == 0):
            # all ships in fleet pass checks: continue sortie
            Util.log_msg(
                "Fleet is ready to sortie. Updating next sortie time.")
            self.combat.set_next_combat_time()
        else:
            fleet.print_damage_counts(repair=True)
            Util.log_msg("Fleet is still not ready to sortie.")

    def _set_shiplist_counts(self):
        """Method that sets the ship-list related internal counts based on the
        number of ships in the port.
        """
        self.ship_count = self._get_ship_count()
        self.ship_page_count = int(
            ceil(self.ship_count / float(self.SHIPS_PER_PAGE)))
        self.ship_last_page_count = (
            self.ship_count % self.SHIPS_PER_PAGE
            if self.ship_count % self.SHIPS_PER_PAGE is not 0
            else self.SHIPS_PER_PAGE)
        Util.log_msg("Detecting {} ships across {} pages.".format(
            self.ship_count, self.ship_page_count))

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
        initial_read = Util.read_ocr_number_text(
            self.regions['ship_counter'], 'shipcount_label.png', 'r', 48)
        number_read = sub(r"\D", "", initial_read)
        if len(number_read) > 3:
            # the read number is too long; truncate anything past the 3rd digit
            number_read = number_read[:3]
        number_read = int(number_read)
        if number_read > 370:
            # to account for edge cases where a digit is appended at the end
            number_read = number_read / 10
        return number_read

    def _check_need_to_switch_ship(self, slot, criteria):
        """Method that checks whether or not the ship in the specified slot
        needs to be switched out based on the criteria.

        Args:
            slot (int): slot ID (0-base)
            criteria (list): dictionary of criteria for the slot

        Returns:
            bool: True if the ship meets the criteria to be swapped out; False
                otherwise
        """
        Util.log_msg("Checking ship in slot {}.".format(slot + 1))
        panel_regions = self.module_regions['panels']
        if 'damage' in criteria:
            valid_damages = list(self.fleets[1].get_damages_at_threshold(
                self.config.combat['repair_limit']))
            valid_damages.append('repair')
            for damage in valid_damages:
                if panel_regions[slot].exists(
                        Pattern('ship_state_dmg_{}.png'.format(damage))
                        .similar(Globals.DAMAGE_SIMILARITY)):
                    Util.log_msg("Ship is damaged: attempting switch.")
                    return True
        if 'fatigue' in criteria:
            for fatigue in ('medium', 'high'):
                if panel_regions[slot].exists(
                        Pattern('ship_state_fatigue_{}.png'.format(fatigue))
                        .similar(Globals.FATIGUE_SIMILARITY)):
                    Util.log_msg("Ship is fatigued: attempting switch.")
                    return True
        if 'sparkle' in criteria:
            if (panel_regions[slot].exists('sparkle_indicator.png', 2) and
                    self.sparkling_cache[slot] <= self.stats.combat_done):
                Util.log_msg("Ship is sparkled: attempting switch.")
                return True
        return False

    def _switch_shiplist_sorting(self, target):
        """Switches the shiplist sorting to the specified target mode.

        Args:
            target (str): the sorting to switch the shiplist to
        """
        while not self.regions['top_submenu'].exists(
                'shiplist_sort_{}.png'.format(target)):
            Util.check_and_click(
                self.regions['top_submenu'],
                'shiplist_sort_arrow.png',
                Globals.EXPAND['shiplist_sort'])

    def _change_shiplist_page(self, target):
        """Method that clicks on the arrow and page number navigation at the
        bottom of the ship list. 'first', 'prev', 'next', 'last' targets will
        click their respective arrow buttons, while an int target between 1 and
        5 (inclusive) will click the page number at that position at the bottom
        of the page (left to right).

        Args:
            target (str, int): specifies which navigation button to press
        """
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
        """Wrapper method that navigates the shiplist to the specified target
        page from the known current page. Uses _change_shiplist_page for
        navigation.

        Args:
            target_page (int): page to navigate to

        Raises:
            ValueError: invalid target_page specified
        """
        if target_page > self.ship_page_count:
            raise ValueError(
                "Invalid shiplist target page ({}) for number of known pages "
                "({}).".format(target_page, self.ship_page_count))

        current_page = self.current_shiplist_page
        # logic that fires off the series of _change_shiplist_page method calls
        # to navigate to the desired target page from the current page
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
        Util.kc_sleep()

    def _choose_ship_by_position(self, position):
        """Method that clicks the ship in the specified position in the ship
        list.

        Args:
            position (int): integer between 1 and 10 specifying the position
                that should be clicked on the ship list

        Raises:
            ValueError: invalid position specified
        """
        if not 1 <= position <= 10:
            raise ValueError(
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
        """Checks the chosen ship's returns its availability for switching.

        Args:
            criteria (list): dictionary containing shipswitch criteria

        Returns:
            bool or str: True if the ship is available; False if it does not
                meet the criteria; 'conflict' if it meets the criteria but a
                ship of the same type is already in the fleet
        """
        # wait until the panel is ready before speeding through checks
        self.regions['lower_right'].wait(
            Pattern('shiplist_shipswitch_button.png').similar(0.75))

        # temp region for speed matching
        temp_region = Region(self.regions['upper_right'])
        temp_region.setAutoWaitTimeout(0)

        # check damage state; repair and heavy checked by default
        valid_damages = list(self.fleets[1].get_damages_at_threshold(
            self.config.combat['repair_limit']))
        valid_damages.extend(['repair', 'heavy'])
        for damage in set(valid_damages):
            if temp_region.exists(
                    Pattern('ship_state_dmg_{}.png'.format(damage))
                    .similar(Globals.DAMAGE_SIMILARITY)):
                return False
        # check fatigue states if it is a criteria
        if 'fatigue' in criteria:
            for fatigue in ('medium', 'high'):
                if temp_region.exists(
                        Pattern('ship_state_fatigue_{}.png'.format(fatigue))
                        .similar(Globals.FATIGUE_SIMILARITY)):
                    return False
        # check sparkle if it is a criteria
        if 'sparkle' in criteria:
            if temp_region.exists(
                    Pattern('sparkle_indicator_shiplist.png').similar(0.9), 2):
                return False
        # passed criteria; check if there is a conflicting ship in fleet
        if Util.check_and_click(
                self.regions['lower_right'], 'shiplist_shipswitch_button.png'):
            return True
        else:
            return 'conflict'

    def _resolve_ship_page_and_position(self, reference, offset):
        """Given a start point (reference) and the offset, figure out the
        page and position based off the current number of ships.

        Args:
            reference (str): 'start' or 'end', indiciating where the offset
                begins from
            offset (int): n-position from reference

        Returns:
            int: page where the specified ship is
            list: list with one value indicating the position where the
                specified ship is on the specified page
        """
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

    def _filter_ships(self, matched_ships, ship_config):
        """Given a list of possible ship matches on the current ship list page,
        filter on the ship lock and ring criteria and return a list of valid
        positions on the page.

        Args:
            matched_ships (list): list of regions, usually from a findAll
                wrapper
            ship_config (dict): dictionary of ship switch config

        Returns:
            list: list of positions of ships matching the criteria
        """
        ship_position_temp = []
        for ship in matched_ships:
            criteria_matched = True
            # create new region based on the match
            ship_row = ship.left(1).right(430)
            ship_row.setAutoWaitTimeout(0)  # speed
            # find numeric position based on the new region's y-position
            position = (ship_row.y - self.kc_region.y - 129) / 28

            # check against ship-specific criterias, if any
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

            if criteria_matched:
                ship_position_temp.append(position)
        ship_position_temp.sort()
        return ship_position_temp

    def _filter_ships_on_level(self, ship_positions):
        """Given a list of ship positions, such as one generated by the
        _filter_ships method, generate a new ship positions list based on the
        levels.

        Args:
            ship_positions (list): list of ints of previously matched ship
                positions

        Returns:
            list: list of positions of ships matching the level criteria
        """
        filtered_ship_positions = []
        for position in ship_positions:
            # get ship config based on position
            ship_config = {}
            for ship_name in self.temp_ship_position_dict:
                if position in self.temp_ship_position_dict[ship_name]:
                    ship_config = self.temp_ship_config_dict[ship_name]
                    break

            if 'level' in ship_config:
                # create new region based on the position
                level_area = Region(
                    self.kc_region.x + 540,
                    self.kc_region.y + 128 + (28 * position),
                    50, 22)
                ship_level = Util.read_ocr_number_text(level_area)
                ship_level = sub(r"\D", "", ship_level)
                ship_level = 1 if not ship_level else int(ship_level)
                if ship_config['level'][0] == '<':
                    if ship_level <= int(ship_config['level'][1:]):
                        filtered_ship_positions.append(position)
                if ship_config['level'][0] == '>':
                    if ship_level >= int(ship_config['level'][1:]):
                        filtered_ship_positions.append(position)
            else:
                filtered_ship_positions.append(position)
        filtered_ship_positions.sort()
        return filtered_ship_positions

    def _choose_and_check_availability_of_ship(self, position, criteria):
        """Select a ship in the ship list based on the specified position,
        and see if it available for switching in.

        Args:
            position (int): position in ship list
            criteria (dict): dictionary of criteria

        Returns:
            bool or str: result of _check_ship_availability() call
        """
        fleet_indicator_area = Region(
            self.kc_region.x + 360, self.kc_region.y + 128 + (28 * position),
            25, 25)
        if fleet_indicator_area.exists(
                Pattern('fleet_indicator_shiplist.png').similar(
                    Globals.SHIP_LIST_FLEET_ICON_SIMILARITY)):
            # if the ship is already in a fleet, skip it
            return False
        self._choose_ship_by_position(position)
        availability = self._check_ship_availability(criteria)
        if availability is True:
            return True
        Util.check_and_click(
            self.regions['lower_right'], 'page_first.png')
        return availability

    def _resolve_replacement_ship(self, slot_config):
        """Wrapper method to find and resolve a replacement ship.

        Args:
            slot_config (dict): dictionary containing the slot's config

        Returns:
            bool: True if a successful switch was made; False otherwise
        """
        if slot_config['mode'] == 'position':
            return self._resolve_replacement_ship_by_position(slot_config)
        elif slot_config['mode'] == 'ship':
            return self._resolve_replacement_ship_by_asset(
                'ship', slot_config)
        elif slot_config['mode'] == 'class':
            return self._resolve_replacement_ship_by_asset(
                'class', slot_config)

    def _resolve_replacement_ship_by_position(self, slot_config):
        """Method that finds a resolves a replacement ship by position.

        Args:
            slot_config (dict): dictionary containing the slot's config

        Returns:
            bool: True if a successful switch was made; False otherwise
        """
        for ship in list(slot_config['ships']):
            self._switch_shiplist_sorting(ship['sort_order'])
            if 'offset_ref' in ship and 'offset' in ship:
                page, positions = self._resolve_ship_page_and_position(
                    ship['offset_ref'], ship['offset'])
                self._navigate_to_shiplist_page(page)
            if 'sparkle' in slot_config['criteria']:
                # if in sparkle mode, remove the checked ship from the list of
                # possible ships so we don't go back to it
                slot_config['ships'].pop(0)
            # there should only be one returned position
            if self._choose_and_check_availability_of_ship(
                    positions[0], slot_config['criteria']) is True:
                return True
        if 'sparkle' in slot_config['criteria']:
            # if in sparkle mode and we reach this point, we've exhausted the
            # list of possible ships; disable the combat module
            self.combat.disable_module()
        return False

    def _resolve_replacement_ship_by_asset(self, mode, slot_config):
        """Method that finds a resolves a replacement ship by class or ship
        asset.

        Args:
            mode (str): specifies whether the resolution is by 'ship' or
                'class'
            slot_config (dict): dictionary containing the slot's config

        Returns:
            bool: True if a successful switch was made; False otherwise
        """
        cache_override = True
        self.temp_ship_config_dict = {}
        self.temp_ship_position_dict = {}
        self._switch_shiplist_sorting('class')

        # start search from cached position, if available
        if slot_config['slot'] in self.position_cache:
            Util.log_msg("Jumping to cached page {}.".format(
                self.position_cache[slot_config['slot']]))
            self._navigate_to_shiplist_page(
                self.position_cache[slot_config['slot']])

        while (not self.temp_ship_position_dict and
                self.current_shiplist_page < self.ship_page_count):
            ship_search_threads = []
            for ship in slot_config['ships']:
                ship_search_threads.append(Thread(
                    target=self._match_shiplist_ships_func,
                    args=(mode, ship[mode], ship)))
            Util.multithreader(ship_search_threads)

            if not self.temp_ship_position_dict:
                # no matches on this page; continue loop
                self._navigate_to_shiplist_page(self.current_shiplist_page + 1)
                continue

            if cache_override:
                # update cache on first encounter
                self._set_position_cache(slot_config['slot'])
                cache_override = False

            ship_position_list = [
                i for j in [
                    self.temp_ship_position_dict[x]
                    for x in self.temp_ship_position_dict]
                for i in j]
            ship_position_list.sort()
            ship_position_list = self._filter_ships_on_level(
                ship_position_list)

            Util.log_msg(
                "Potential replacement ships found in page {} positions {}"
                .format(
                    self.current_shiplist_page,
                    ", ".join([str(i) for i in ship_position_list])))

            if mode == 'ship':
                for ship in self.temp_ship_position_dict:
                    for position in self.temp_ship_position_dict[ship]:
                        if position not in ship_position_list:
                            # ship in position did not pass filtering on level
                            continue
                        availability = (
                            self._choose_and_check_availability_of_ship(
                                position, slot_config['criteria']))
                        if availability is True:
                            return True
                        elif availability == 'dupe':
                            break
            elif mode == 'class':
                for position in ship_position_list:
                    if self._choose_and_check_availability_of_ship(
                            position, slot_config['criteria']) is True:
                        return True

            # no available ships on this page; reset matches and continue loop
            self.temp_ship_config_dict = {}
            self.temp_ship_position_dict = {}
            if 'sparkle' in slot_config['criteria']:
                # if in sparkle mode and we didn't see any valid ships here,
                # don't jump to this page on the next pass
                cache_override = True
            self._navigate_to_shiplist_page(self.current_shiplist_page + 1)
        if 'sparkle' in slot_config['criteria']:
            # if in sparkle mode and we reach this point, we've exhausted the
            # list of possible ships; disable the combat module
            self.combat.disable_module()
        return False

    def _match_shiplist_ships_func(self, mode, name, ship_config):
        """Child multithreaded method for finding matching classes and ships.

        Args:
            mode (str): specifies whether or not the search is for 'ship's or
                'class'es
            name (str): name of class or ship
            ship_config (dict): dictionary of ship criteria
        """
        img = (
            'shiplist_ship_{}.png'.format(name) if mode == 'ship'
            else 'shiplist_class_{}.png'.format(name))
        matched_ships = Util.findAll_wrapper(
            self.module_regions['shiplist_class_col'],
            Pattern(img).similar(Globals.SHIP_LIST_SIMILARITY))

        ship_positions = self._filter_ships(matched_ships, ship_config)
        if ship_positions:
            self.temp_ship_position_dict[name] = ship_positions
            self.temp_ship_config_dict[name] = ship_config

    def _set_position_cache(self, name):
        self.position_cache[name] = (
            self.current_shiplist_page - 1
            if self.current_shiplist_page - 1 > 0
            else 1)

    def _set_sparkle_cache(self, slot):
        self.sparkling_cache[slot] = (
            self.stats.combat_done + Globals.SPARKLING_RUN_COUNT)
