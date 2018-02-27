from datetime import datetime, timedelta
from random import randint
from combat import CombatModule, CombatFleet
from expedition import ExpeditionModule, ExpeditionFleet
from pvp import PvPModule
from quest import QuestModule
from repair import RepairModule
from resupply import ResupplyModule
from shipswitcher import ShipSwitcher
from nav import Nav
from stats import Stats
from util import Util


class KCAutoKai(object):
    """Primary class of kcauto-kai. The master class that contains the high
    level logic.

    Attributes:
        active_fleets (dict): dictionary of Fleet instances undergoing any
            kcauto-kai-mediated activity
        combat_fleets (dict): dictionary of Fleet instances undergoing combat
            sorties
        config (Config): Config instance, passed in during instantiation
        expedition_fleets (dict): dictionary of Fleet instances undergoing
            expeditions
        kc_region (Region): sikuli Region instance containing the last known
            location of the Kantai Collection game screen
        modules (dict): dictionary of individual module instances
        next_scheduled_sleep_time (datetime): when the next scheduled sleep
            should occur
        regions (dict): dictionary of pre-calculated game regions for faster
            searching and matching
        paused (bool): whether or not the script was in a paused state
        print_stats_check (bool): whether or not the stats should be displayed
            at the end of the loop
        sleep_wake_time (datetime): when the script should exit out of
            scheduled sleep
        stats (Stats): Stats instance
    """

    kc_region = None
    config = None
    stats = None
    modules = {
        'resupply': None,
        'pvp': None,
        'combat': None,
        'repair': None,
        'ship_switcher': None,
        'expedition': None,
        'quest': None
    }
    print_stats_check = True
    paused = False
    regions = {}
    active_fleets = {}
    combat_fleets = {}
    expedition_fleets = {}
    combat_cycle = False
    next_scheduled_sleep_time = None
    sleep_wake_time = None

    def __init__(self, config):
        """Initializes the primary kcauto-kai instance with the passed in
        Config instance; creates the Stats instance and resets scheduled sleep
        timers.

        Args:
            config (Config): kcauto-kai Config instance
        """
        self.config = config
        self.stats = Stats(self.config)
        self._reset_scheduled_sleep()

    def refresh_config(self):
        """Method that allows for the hot-reloading of the config files. Run at
        the beginning of every cycle and instantiates, re-instantiates, or
        destroys modules as necessary.
        """
        self.config.read()
        self.config.validate()

        if self.config.changed:
            self.active_fleets = {}
            self.combat_fleets = {}
            self.expedition_fleets = {}
            self._reset_scheduled_sleep()
            self._focus_kancolle()

            # initialize pvp module
            if self.config.pvp['enabled']:
                self.active_fleets[1] = CombatFleet(1)
                self.modules['pvp'] = PvPModule(
                    self.config, self.stats, self.regions,
                    self.active_fleets[1])
            else:
                self.modules['pvp'] = None

            # initialize combat fleets
            if self.config.combat['enabled']:
                if self.config.combat['combined_fleet']:
                    if 1 not in self.active_fleets:
                        self.active_fleets[1] = CombatFleet(1)
                    self.combat_fleets[1] = self.active_fleets[1]
                    self.active_fleets[2] = CombatFleet(2)
                    self.combat_fleets[2] = self.active_fleets[2]
                elif self.config.combat['fleet_mode'] == 'striking':
                    self.active_fleets[3] = CombatFleet(3)
                    self.combat_fleets[3] = self.active_fleets[3]
                else:
                    if 1 not in self.active_fleets:
                        self.active_fleets[1] = CombatFleet(1)
                    self.combat_fleets[1] = self.active_fleets[1]

            # initialize combat module
            if self.config.combat['enabled']:
                self.modules['combat'] = CombatModule(
                    self.config, self.stats, self.regions, self.combat_fleets)
                self.modules['repair'] = RepairModule(
                    self.config, self.stats, self.regions, self.combat_fleets,
                    self.modules['combat'])
            else:
                self.modules['combat'] = None
                self.modules['repair'] = None

            # initialize ship switcher module
            if self.config.ship_switcher['enabled'] and self.modules['combat']:
                self.modules['ship_switcher'] = ShipSwitcher(
                    self.config, self.stats, self.regions, self.combat_fleets,
                    self.modules['combat'])
            else:
                self.modules['ship_switcher'] = None

            # initialize expedition module
            if self.config.expeditions['enabled']:
                if 'fleet2' in self.config.expeditions:
                    fleet2 = ExpeditionFleet(
                        2, self.config.expeditions['fleet2'])
                    self.active_fleets[2] = fleet2
                    self.expedition_fleets[2] = fleet2
                if 'fleet3' in self.config.expeditions:
                    fleet3 = ExpeditionFleet(
                        3, self.config.expeditions['fleet3'])
                    self.active_fleets[3] = fleet3
                    self.expedition_fleets[3] = fleet3
                if 'fleet4' in self.config.expeditions:
                    fleet4 = ExpeditionFleet(
                        4, self.config.expeditions['fleet4'])
                    self.active_fleets[4] = fleet4
                    self.expedition_fleets[4] = fleet4

                self.modules['expedition'] = ExpeditionModule(
                    self.config, self.stats, self.regions,
                    self.expedition_fleets)
            else:
                self.modules['expedition'] = None

            # initialize resupply module
            self.modules['resupply'] = ResupplyModule(
                self.config, self.stats, self.regions, self.active_fleets)

            # initialize quest module
            if self.config.quests['enabled']:
                self.modules['quest'] = QuestModule(
                    self.config, self.stats, self.regions)
            else:
                self.modules['quest'] = None

            # reset the config module's changed status
            self.config.changed = False
            self.print_stats_check = True

    def _reset_scheduled_sleep(self):
        """Method to reset the scheduled sleep attributes.
        """
        self.next_scheduled_sleep_time = None
        self.sleep_wake_time = datetime.now()

    def _focus_kancolle(self):
        """Method that focuses the specified Kantai Collection game window,
        generates the pre-calculated regions, then populates them down to any
        active modules that require them.
        """
        self.kc_region, self.regions = Util.focus_kc(self.config)
        for module in self.modules:
            if hasattr(self.modules[module], 'regions'):
                self.modules[module].regions = self.regions

    def _run_expedition_check(self):
        """Method to navigate home and receive expeditions; if already at home,
        this method refreshes it (UNUSED)

        Returns:
            bool: returns True if expeditions were received, False otherwise
        """
        if not self.modules['expedition']:
            return False

        if self.modules['expedition'].expect_returned_fleet():
            if not Nav.goto(self.regions, 'home'):
                if not self.run_receive_expedition_cycle():
                    Nav.goto(self.regions, 'refresh_home')
                    return self.run_receive_expedition_cycle()
                else:
                    return True
            else:
                return self.run_receive_expedition_cycle()
        return False

    def _run_fast_expedition_check(self):
        """Method to navigate home and receive expeditions. Does not refresh
        home if already there.

        Returns:
            bool: returns True if expeditions were received, False otherwise
        """
        Nav.goto(self.regions, 'home')
        return self.run_receive_expedition_cycle()

    def run_receive_expedition_cycle(self):
        """Method that checks for and receives the returned expedition. Calls
        itself to check for and receive additional returned expeditions.

        Returns:
            bool: True if expeditions were received, False otherwise
        """
        if self.regions['expedition_flag'].exists('expedition_flag.png'):
            Util.click_preset_region(self.regions, 'center')
            if self.modules['expedition']:
                # expedition module is enabled
                self.modules['expedition'].receive_expedition()
            self.regions['lower_right_corner'].wait('next.png', 30)
            while not self.regions['home_menu'].exists('home_menu_sortie.png'):
                Util.click_preset_region(self.regions, 'shipgirl')
                Util.kc_sleep()
            # recurse in case there are more expedition fleets to receive
            self.run_receive_expedition_cycle()
            self.print_stats_check = True
            return True
        return False

    def run_expedition_cycle(self):
        """Method to run the expedition cycle.

        Returns:
            bool: False if there is no Expeditions module
        """
        if not self.modules['expedition']:
            return False

        if self.modules['expedition'].expect_returned_fleet():
            if not Nav.goto(self.regions, 'home'):
                if not self.run_receive_expedition_cycle():
                    Nav.goto(self.regions, 'refresh_home')
            self.run_receive_expedition_cycle()

        self.run_resupply_cycle()

        if self.modules['expedition'].fleets_at_base():
            self.print_stats_check = True
            self._focus_kancolle()
            Nav.goto(self.regions, 'home')
            self._run_fast_expedition_check()
            self.modules['expedition'].goto_expedition()
            for params in self.modules['expedition'].fleets.items():
                fleet_id, fleet = params
                if fleet.at_base:
                    self.modules['expedition'].sortie_expedition(fleet)
            self.run_resupply_cycle()
            return True
        return False

    def run_pvp_cycle(self):
        """Method to run the PvP cycle.

        Returns:
            bool: False if there is no PvP module
        """
        if not self.modules['pvp']:
            return False

        if self.modules['pvp'].check_need_to_pvp():
            self.print_stats_check = True
            self._focus_kancolle()
            Nav.goto(self.regions, 'home')
            self._run_fast_expedition_check()
            # Check quests if active
            if self.modules['quest']:
                self.modules['quest'].goto_quests()
                self.modules['quest'].quests_logic_wrapper()
            Nav.goto(self.regions, 'home')
            self._run_fast_expedition_check()
            self.modules['pvp'].goto_pvp()

            while self.modules['pvp'].run_pvp_logic():
                self._run_fast_expedition_check()
                self.run_resupply_cycle()
                Nav.goto(self.regions, 'home')
                self._run_fast_expedition_check()
                # Check quests if active
                if self.modules['quest']:
                    self.modules['quest'].goto_quests()
                    self.modules['quest'].quests_logic_wrapper_fast()
                Nav.goto(self.regions, 'home')
                self._run_fast_expedition_check()
                self.modules['pvp'].goto_pvp()
            return True
        return False

    def run_combat_cycle(self):
        """Method to run the combat cycle.

        Returns:
            bool: False if there is no Combat module
        """
        if not self.modules['combat']:
            return False

        if self.modules['combat'].check_need_to_sortie():
            self.print_stats_check = True
            self.combat_cycle = True
            self._focus_kancolle()
            Nav.goto(self.regions, 'home')
            self._run_fast_expedition_check()
            self.modules['combat'].goto_combat()

            if self.modules['combat'].combat_logic_wrapper():
                if self.modules['expedition']:
                    self.modules['expedition'].reset_support_fleets()

            self._run_fast_expedition_check()
            return True
        else:
            self.combat_cycle = False
        return False

    def run_quest_cycle(self):
        """Method to run the quest cycle.

        Returns:
            bool: False if there is no Quest module
        """
        if not self.modules['quest']:
            return False

        if self.modules['quest'].check_need_to_check_quests():
            self.print_stats_check = True
            self._focus_kancolle()
            Nav.goto(self.regions, 'home')
            self._run_fast_expedition_check()
            self.modules['quest'].goto_quests()
            self.modules['quest'].quests_logic_wrapper()
            return True
        return False

    def run_resupply_cycle(self):
        """Method that runs the resupply cycle.
        """
        if self.modules['resupply'].check_need_to_resupply():
            self.print_stats_check = True
            Nav.goto(self.regions, 'resupply')
            self.modules['resupply'].resupply_fleets()
            Nav.goto(self.regions, 'home')

    def run_repair_cycle(self):
        """Method that runs the repair cycle.

        Returns:
            bool: False if there is no Combat module
        """
        if not self.modules['combat']:
            return False

        if self.modules['repair'].check_need_to_repair():
            self.modules['repair'].goto_repair()

            self.modules['repair'].repair_fleets()

    def run_ship_switch_cycle(self):
        """Method that runs the ship switch cycle.

        Returns:
            bool: False if there is no ShipSwitcher module
        """
        if not self.modules['ship_switcher']:
            return False

        if (self.modules['ship_switcher'].check_need_to_switch() and
                self.combat_cycle):
            self.modules['ship_switcher'].goto_fleetcomp()

            self.modules['ship_switcher'].ship_switch_logic()

    def conduct_scheduled_sleep(self):
        """Method that schedules and conducts the scheduled sleep of
        kcauto-kai.

        Returns:
            bool: False if scheduled sleep is disabled or if it is not time
                for the scheduled sleep, otherwise True
        """
        if not self.config.scheduled_sleep['enabled']:
            return False

        cur_time = datetime.now()

        # if a scheduled sleep time is not set, set it
        if not self.next_scheduled_sleep_time:
            self.next_scheduled_sleep_time = datetime.now().replace(
                hour=int(self.config.scheduled_sleep['start_time'][:2]),
                minute=int(self.config.scheduled_sleep['start_time'][2:]),
                second=0, microsecond=0)
            if cur_time >= self.next_scheduled_sleep_time:
                # specified time has already passed today, set to next day
                self.next_scheduled_sleep_time = (
                    self.next_scheduled_sleep_time + timedelta(days=1))

        # if the current time is before the wake time, stay asleep
        if cur_time < self.sleep_wake_time:
            return True

        # if the current time is past the schedule sleep time, go to sleep
        if cur_time >= self.next_scheduled_sleep_time:
            sleep_length = self.config.scheduled_sleep['sleep_length']
            Util.log_warning(
                "Scheduled Sleep beginning. Resuming in ~{} hours.".format(
                    sleep_length))
            # set the wake time when going to sleep so the previous conditional
            # is triggered
            self.sleep_wake_time = cur_time + timedelta(
                hours=int(sleep_length),
                minutes=int(sleep_length % 1 * 60) + randint(1, 15))
            # set the next scheduled sleep time as well
            self.next_scheduled_sleep_time = (
                self.next_scheduled_sleep_time + timedelta(days=1))
            return True
        return False

    def conduct_pause(self):
        """Method that pauses the script, much like scheduled sleep. Still
        allows for config updates to happen.
        """
        if self.config.pause:
            if not self.paused:
                # first time getting paused
                Util.log_success("Pausing kcauto-kai!")
                self.paused = True
            return True
        else:
            if self.paused:
                # unpausing
                Util.log_success("Resuming kcauto-kai!")
                self.paused = False
        return False

    def print_cycle_stats(self):
        """Method to print a summary of the stats stored in the different
        modules.
        """
        if self.print_stats_check:
            self.stats.increment_cycles_completed()

            Util.log_success("End of cycle {:d}".format(
                self.stats.cycles_completed))
            if self.modules['combat']:
                self.modules['combat'].print_status()
            if self.modules['pvp']:
                self.modules['pvp'].print_status()
            if self.modules['expedition']:
                self.modules['expedition'].print_status()
            if self.modules['quest']:
                self.modules['quest'].print_status()

            self.stats.print_stats()
        self.print_stats_check = False
