from sikuli import Pattern, Location
from datetime import datetime, timedelta
from kca_globals import Globals
from combat import CombatFleet
from nav import Nav
from util import Util


class RepairModule(object):
    def __init__(self, config, stats, regions, fleets, combat):
        """Initializes the Repair module.

        Args:
            config (Config): kcauto-kai Config instance
            stats (Stats): kcauto-kai Stats instance
            regions (dict): dict of pre-defined kcauto-kai regions
            fleets (dict): dict of active combat Fleet instances
            combat (ComabtModule): active Combat Module instance
        """
        self.config = config
        self.stats = stats
        self.regions = regions
        self.kc_region = self.regions['game']
        self.fleets = fleets
        self.combat = combat
        self.repair_slots = 0
        self.repair_timers = []

    def goto_repair(self):
        """Method to navigate to the repair menu.
        """
        Nav.goto(self.regions, 'repair')

    def check_need_to_repair(self):
        """Method to check whether or not ships need to be repaired in the
        active combat fleets.

        Returns:
            boolean: True if ships need to be repaired, False otherwise
        """
        self._remove_old_timers()
        for fleet_id, fleet in self.fleets.items():
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

        # find busy docks and resolve existing repair timers
        self.repair_timers = []
        dock_busy_matches = Util.findAll_wrapper(
            self.kc_region, 'dock_timer.png')
        dock_busy_count = 0

        for match in dock_busy_matches:
            dock_busy_count += 1
            repair_timer = Util.read_timer(self.kc_region, match, 'l', 100)
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
                    self.regions['right'], 'repair_timer.png', 'r', 80, 5)
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
                self._update_combat_next_sortie_time(repair_timer)
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

        for fleet_marker in fleet_markers:
            fleet_id = int(fleet_marker[17])  # infer from filename
            fleet_instance = self.fleets[fleet_id]

            if fleet_instance.get_damage_counts_at_threshold(
                    self.config.combat['repair_limit']) == 0:
                # if this fleet has no longer has ships that need repair,
                # don't search for its marker
                continue

            ship_matches = Util.findAll_wrapper(
                self.regions['repair_shiplist_fleet_markers'],
                Pattern(fleet_marker).similar(0.9))
            for ship_match in ship_matches:
                target_region = ship_match.offset(Location(342, 0)).nearby(5)
                for damage in valid_damages:
                    if fleet_instance.damage_counts[damage] == 0:
                        # if no ships in this fleet are at this damage state,
                        # don't search for it
                        continue

                    damage_icon = 'repairlist_dmg_{}.png'.format(damage)
                    if Util.check_and_click(
                            target_region, damage_icon,
                            Globals.EXPAND['repair_list']):
                        fleet_instance.damage_counts[damage] -= 1
                        fleet_instance.damage_counts['repair'] += 1
                        return True
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

    def _update_combat_next_sortie_time(self, timer):
        """Method to update the internally tracked list of timers and update
        the combat module's next sortie time based on the shortest stored
        timer.

        Args:
            timer (datetime): datetime instance of when the repair that just
                started will end
        """
        repair_end_time = self._timer_to_datetime(timer)
        self.repair_timers.append(repair_end_time)
        self.repair_timers.sort()
        shortest_timer = self.repair_timers[0]

        if shortest_timer > self.combat.next_combat_time:
            self.combat.next_combat_time = shortest_timer + timedelta(
                minutes=1)
            Util.log_msg("Delaying next combat sortie to {}".format(
                self.combat.next_combat_time.strftime('%Y-%m-%d %H:%M:%S')))
