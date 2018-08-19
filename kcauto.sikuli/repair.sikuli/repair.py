from sikuli import Region, Pattern, Location
from datetime import datetime, timedelta
from kca_globals import Globals
from combat import CombatFleet
from nav import Nav, NavList
from util import Util


class RepairModule(object):
    def __init__(self, config, stats, regions, fleets, combat):
        """Initializes the Repair module.

        Args:
            config (Config): kcauto Config instance
            stats (Stats): kcauto Stats instance
            regions (dict): dict of pre-defined kcauto regions
            fleets (dict): dict of active combat Fleet instances
            combat (ComabtModule): active Combat Module instance
        """
        self.config = config
        self.stats = stats
        self.regions = regions
        self.kc_region = self.regions['game']
        self.fleets = fleets
        self.combat = combat

        self.ship_count = 1
        self.ship_page_count = 1
        self.ship_last_page_count = 1
        self.current_shiplist_page = 1
        self.repair_slots = 0
        self.repair_timers = []

        x = self.kc_region.x
        y = self.kc_region.y
        self.module_regions = {
            'repair_shiplist_fleet_markers': Region(x + 555, y + 188, 45, 462)
        }

    def goto_repair(self):
        """Method to navigate to the repair menu.
        """
        Nav.goto(self.regions, 'repair')
        self.current_shiplist_page = 1

    def check_need_to_repair(self):
        """Method to check whether or not ships need to be repaired in the
        active combat fleets.

        Returns:
            boolean: True if ships need to be repaired, False otherwise
        """
        self._remove_old_timers()
        for fleet_id, fleet in self.fleets.items():
            # first check if there is a forced check
            if fleet.force_check_repair:
                # immediately unset this flag so it does not cause false
                # positives later on
                fleet.force_check_repair = False
                return True
            # then check against damage counts
            if fleet.get_damage_counts_at_threshold(
                    self.config.combat['repair_limit']) > 0:
                if (len(self.repair_timers) == self.repair_slots and
                        self.repair_slots != 0):
                    # there are ships to repair, but the docks are full with
                    # ongoing repairs so do not attempt repairs yet
                    return False
                return True
        return False

    def repair_fleets(self):
        """Method that finds ships to repair and repairs them in the repair
        menu.
        """
        Util.log_msg("Begin repairing fleets.")
        self._set_shiplist_counts()

        # find busy docks and resolve existing repair timers
        self.repair_timers = []  # clear previously tracked timers
        dock_busy_matches = Util.findAll_wrapper(
            self.kc_region, 'dock_timer.png')
        dock_busy_count = 0

        for match in dock_busy_matches:
            dock_busy_count += 1
            repair_timer = Util.read_timer(self.kc_region, match, 'l', 130)
            self.repair_timers.append(self._timer_to_datetime(repair_timer))

        # find empty docks
        dock_empty_matches = Util.findAll_wrapper(
            self.kc_region, 'dock_empty.png')
        dock_empty_count = 0

        for match in dock_empty_matches:
            dock_empty_count += 1

        if dock_busy_count + dock_empty_count > self.repair_slots:
            # update the known number of total repair slots if it is different
            # from what is already stored, with a max of 4 slots
            self.repair_slots = min(dock_busy_count + dock_empty_count, 4)

        if dock_empty_count == 0:
            # TODO: handle repair_timers, come back on shortest timer
            return False
        else:
            while True:
                if self.kc_region.exists('dock_empty.png'):
                    # while there are empty docks, if there are ships to
                    # repair, continue repairing; otherwise, stop
                    if self.check_need_to_repair():
                        self._conduct_repair()
                    else:
                        break
                    Util.kc_sleep(1)
                else:
                    # no empty docks, so just exit out of loop
                    break
        if len(self.repair_timers) > dock_busy_count:
            self._update_combat_next_sortie_time()

    def _conduct_repair(self):
        """Method that chooses an empty dock, chooses a ship, toggles the
        bucket switch if necessary, and begins the repair.
        """
        Util.wait_and_click_and_wait(
            self.kc_region, 'dock_empty.png',
            self.regions['right'], 'repairlist_icon.png')

        if self._pick_fleet_ship():
            # TODO: only picks fleet ships at the moment... figure out logic
            # to repair other ships?? Or at least change the page?
            use_bucket = False
            if self.config.combat['repair_time_limit'] == 0:
                use_bucket = True
            elif ('ReserveDocks' in self.config.combat['misc_options'] and
                    len(self.repair_timers) == self.repair_slots - 1):
                use_bucket = True
            else:
                repair_timer = Util.read_timer(
                    self.regions['right'], 'repair_timer.png', 'r', 115, 5)
                if ((repair_timer['hours'] * 100 + repair_timer['minutes']) >
                        self.config.combat['repair_time_limit']):
                    use_bucket = True

            if use_bucket:
                Util.check_and_click(
                    self.regions['right'], 'bucket_switch.png')

            Util.wait_and_click(self.regions['right'], 'repair_confirm_1.png')
            Util.wait_and_click(self.regions['lower'], 'repair_confirm_2.png')

            self.stats.increment_repairs_done()
            if use_bucket:
                self.stats.increment_buckets_used()
                self.kc_region.wait('dock_empty.png')
            else:
                self._add_to_repair_timers(repair_timer)
                self.regions['lower_right'].waitVanish('page_prev.png')
                Util.kc_sleep(1)
        Util.kc_sleep()

    def _pick_fleet_ship(self):
        """Method to click a fleet ship based on the fleet icons displayed next
        to the ship in the ship list.

        Returns:
            boolean: True if a fleet ship was chosen and clicked, False
                otherwise
        """
        Util.log_msg("Picking damaged ship from combat fleet(s) to repair.")
        # generate markers for fleets to repair
        fleet_markers = []
        if self.config.combat['fleet_mode'] == 'striking':
            fleet_markers = ['repairlist_fleet_3.png']
        else:
            fleet_markers = [
                'repairlist_fleet_1_flag.png', 'repairlist_fleet_1.png']
            if self.config.combat['combined_fleet']:
                fleet_markers.append('repairlist_fleet_2.png')

        # get damages to repair
        valid_damages = CombatFleet.get_damages_at_threshold(
            self.config.combat['repair_limit'])

        while self.current_shiplist_page <= self.ship_page_count:
            for fleet_marker in fleet_markers:
                fleet_id = int(fleet_marker[17])  # infer from filename
                fleet_instance = self.fleets[fleet_id]

                if fleet_instance.get_damage_counts_at_threshold(
                        self.config.combat['repair_limit']) == 0:
                    # if this fleet has no longer has ships that need repair,
                    # don't search for its marker
                    continue

                ship_matches = Util.findAll_wrapper(
                    self.module_regions['repair_shiplist_fleet_markers'],
                    Pattern(fleet_marker).similar(0.9))
                for ship_match in ship_matches:
                    target_region = ship_match.offset(
                        Location(525, 0)).nearby(10)
                    for damage in valid_damages:
                        if fleet_instance.damage_counts[damage] == 0:
                            # if no ships in this fleet are at this damage
                            # state, don't search for it
                            continue

                        damage_icon = 'repairlist_dmg_{}.png'.format(damage)
                        if Util.check_and_click(
                                target_region, damage_icon,
                                Globals.EXPAND['repair_list']):
                            fleet_instance.damage_counts[damage] -= 1
                            fleet_instance.damage_counts['repair'] += 1
                            return True
            if self.current_shiplist_page < self.ship_page_count:
                # check if there were even any damaged ships on the page
                damage_exists = False
                for damage in valid_damages:
                    damage_icon = 'repairlist_dmg_{}.png'.format(damage)
                    if self.regions['right'].exists(damage_icon):
                        damage_exists = True
                        break
                if damage_exists:
                    # did not select a ship but damaged ships exist; go to next
                    # page
                    self._navigate_to_shiplist_page(
                        self.current_shiplist_page + 1)
                else:
                    # no more ships of valid damage state exists in list;
                    # return to the first page
                    self._navigate_to_shiplist_page('first')
                    return False
        return False

    def _pick_any_ship(self):
        """UNUSED. Method to click any ship in the ship list.

        Returns:
            boolean: True if a ship was chosen and clicked, False otherwise
        """
        Util.log_msg("Picking any damaged ship to repair.")
        valid_damages = CombatFleet.get_damages_at_threshold(
            self.config.combat['repair_limit'])
        for damage in valid_damages:
            Util.log_msg("Checking for ship with {} damage.".format(damage))
            if Util.check_and_click(
                    self.regions['right'],
                    'repairlist_dmg_{}.png'.format(damage),
                    Globals.EXPAND['repair_list']):
                return True
        return False

    def _set_shiplist_counts(self):
        """Method that sets the ship-list related internal counts based on the
        number of ships in the port.
        """
        self.ship_count, self.ship_page_count, self.ship_last_page_count = (
            Util.get_shiplist_counts(self.regions))
        Util.log_msg("Detecting {} ships across {} pages.".format(
            self.ship_count, self.ship_page_count))

    def _navigate_to_shiplist_page(self, target_page):
        """Wrapper method that navigates the shiplist to the specified target
        page from the known current page. Uses NavList's navigate_to_page for
        navigation.

        Args:
            target_page (int): page to navigate to

        Raises:
            ValueError: invalid target_page specified
        """
        if type(target_page) is int and target_page > self.ship_page_count:
            raise ValueError(
                "Invalid shiplist target page ({}) for number of known pages "
                "({}).".format(target_page, self.ship_page_count))

        self.current_shiplist_page = NavList.navigate_to_page(
            self.regions, self.ship_page_count, self.current_shiplist_page,
            target_page, 'repair')

    def _timer_to_datetime(self, timer):
        """Method to convert the passed in timer dict to a datetime object

        Args:
            timer (dict): dict of timer readouts

        Returns:
            datetime: datetime instance based on the passed in timer
        """
        return datetime.now() + timedelta(
            hours=timer['hours'], minutes=timer['minutes'],
            seconds=timer['seconds'])

    def _remove_old_timers(self):
        """Method to go through the existing repair timers and remove them if
        they are past, implying that the repairs are done and the dock is free
        """
        self.repair_timers = [
            timer for timer in self.repair_timers if timer > datetime.now()]

    def _add_to_repair_timers(self, timer):
        """Method to add to the internally tracked list of timers with the
        passed in timer.

        Args:
            timer (datetime): datetime instance of when the repair that just
                started will end
        """
        repair_end_time = self._timer_to_datetime(timer)
        self.repair_timers.append(repair_end_time)
        Util.log_msg("Repair will complete at {}".format(
            repair_end_time.strftime('%Y-%m-%d %H:%M:%S')))

    def _update_combat_next_sortie_time(self):
        """Method to update the Combat module's next sortie timer based on the
        shortest timer in the internal repair timers list.
        """
        self.repair_timers.sort()
        shortest_timer = self.repair_timers[0]

        if shortest_timer > self.combat.next_combat_time:
            self.combat.next_combat_time = shortest_timer + timedelta(
                minutes=1)
            Util.log_msg("Delaying next combat sortie to {}".format(
                self.combat.next_combat_time.strftime('%Y-%m-%d %H:%M:%S')))
