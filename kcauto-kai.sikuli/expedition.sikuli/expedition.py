from sikuli import Pattern
from datetime import datetime, timedelta
from random import choice
from fleet import Fleet
from nav import Nav
from util import Util


class ExpeditionModule(object):
    def __init__(self, config, stats, regions, fleets):
        """Initializes the Expedition module.

        Args:
            config (Config): kcauto-kai Config instance
            stats (Stats): kcauto-kai Stats instance
            regions (dict): dict of pre-defined kcauto-kai regions
            fleets (dict): dict of active ExpeditionFleet instances
        """
        self.enabled = True
        self.disabled_time = None
        self.config = config
        self.stats = stats
        self.regions = regions
        self.kc_region = regions['game']
        self.fleets = fleets

    def goto_expedition(self):
        """Method to navigate to the expedition menu.
        """
        Nav.goto(self.regions, 'expedition')

    def expect_returned_fleet(self):
        """Method to check whether or not the expedition module should expect
        expedition fleets to return based on their return timers.

        Returns:
            bool: True if expeditions are expected to return, False otherwise
        """
        for fleet_id, fleet in self.fleets.items():
            if fleet.return_time < datetime.now():
                # default to being true so we can force an expedition sortie
                fleet.at_base = True
                return True
        return False

    def fleets_at_base(self):
        """Method to check whether or not any of the expedition fleets are at
        base and waiting to be sent on an expedition.

        Returns:
            bool: True if fleets are at base, False otherwise
        """
        for fleet_id, fleet in self.fleets.items():
            if fleet.at_base:
                return True
        return False

    def receive_expedition(self):
        """Method to resolve a returning expedition. Does not actually interact
        with the game itself, but sets the correct flags on the ExpeditionFleet
        instances.
        """
        for fleet_id, fleet in self.fleets.items():
            if fleet.return_time < datetime.now() and not fleet.at_base:
                Util.log_msg(
                    "An expedition fleet has returned. Probably fleet {:d}"
                    .format(fleet_id))
                self.stats.increment_expeditions_received()
                fleet.at_base = True
                fleet.needs_resupply = True
                break

    def sortie_expedition(self, fleet):
        """Method to sortie an expedition fleet to its assigned expeditions.

        Args:
            fleet (ExpeditionFleet): ExpeditionFleet to send on an expedition

        Returns:
            bool: True if the fleet was successfully sent on an expedition,
                False otherwise
        """
        self.stats.increment_expeditions_attempted()
        fleet.choose_expedition()
        Util.log_msg("Sortieing fleet {:d} to expedition {:d}".format(
            fleet.fleet_id, fleet.expedition))
        # change expedition world if necessary
        while not Util.check_and_click(
                self.kc_region,
                'expedition_{}.png'.format(fleet.expedition)):
            Util.kc_sleep()
            Util.wait_and_click(
                self.kc_region,
                'e_world_{}.png'.format(fleet.expedition_area))
        Util.kc_sleep(1)
        if not Util.check_and_click(self.kc_region, 'sortie_select.png'):
            if self.kc_region.exists(
                    Pattern('expedition_timer_complete.png').exact()):
                fleet.update_return_time(0, -1)
            else:
                expedition_timer = Util.read_timer(
                    self.kc_region, 'expedition_timer.png', 'r', 80)
                fleet.update_return_time(
                    expedition_timer['hours'], expedition_timer['minutes'] - 1)
                Util.log_warning(
                    "Expedition is already running. Return time: {}"
                    .format(fleet.return_time.strftime('%Y-%m-%d %H:%M:%S')))
            return False

        Util.rejigger_mouse(self.regions, 'top')
        # switch fleet as necessary
        if fleet.fleet_id != 2:
            Fleet.switch(self.regions['top_submenu'], fleet.fleet_id)

        if self.kc_region.exists('ship_state_busy.png'):
            # fleet is already on an expedition
            Util.log_warning('Fleet not available. Check back later')
            fleet.update_return_time(0, 15)
            Util.wait_and_click_and_wait(
                self.kc_region,
                'e_world_1.png',
                self.regions['top_submenu'],
                'sortie_top_menu_expedition_active.png')
            return False
        else:
            if not fleet.check_supplies(self.regions['check_supply']):
                # fleet needs resupply
                Util.wait_and_click_and_wait(
                    self.kc_region,
                    'e_world_1.png',
                    self.regions['top_submenu'],
                    'sortie_top_menu_expedition_active.png')
                return False
            # successful expedition sortie
            Util.wait_and_click(
                self.kc_region, 'expedition_dispatch.png')
            fleet.dispatch_fleet()
            self.stats.increment_expeditions_sent()
            Util.log_msg(
                "Fleet {:d} sortied. Expected return time: {}".format(
                    fleet.fleet_id,
                    fleet.return_time.strftime('%Y-%m-%d %H:%M:%S')))
            Util.kc_sleep(3)
        Util.rejigger_mouse(self.regions, 'top')
        Util.kc_sleep()
        return True

    def reset_support_fleets(self):
        """Method to reset boss and node support expedition fleets since they
        do not have a typical expedition receive screen, and they return as
        soon as the subsequent sortie is over.
        """
        for fleet_id, fleet in self.fleets.items():
            if (9998 in fleet.expeditions or 9999 in fleet.expeditions or
                    33 in fleet.expeditions or 34 in fleet.expeditions):
                Util.log_msg(
                    "Resetting fleet {}'s expedition status.".format(fleet_id))
                fleet.at_base = True
                fleet.needs_resupply = True

    def disable_module(self):
        Util.log_success("De-activating the expedition module.")
        self.enabled = False
        self.disabled_time = datetime.now()

    def enable_module(self):
        Util.log_success("Re-activating the expedition module.")
        self.enabled = True
        self.disabled_time = None

    def print_status(self):
        """Method to print the arrival times of the expedition fleets.
        """
        if self.enabled:
            for fleet_id in self.fleets:
                Util.log_success("Fleet {}: Expedition returns at {}".format(
                    self.fleets[fleet_id].fleet_id,
                    self.fleets[fleet_id].return_time.strftime(
                        '%Y-%m-%d %H:%M:%S')))
        else:
            Util.log_success("Expedition module disabled as of {}".format(
                self.disabled_time.strftime('%Y-%m-%d %H:%M:%S')))


class ExpeditionFleet(Fleet):
    def __init__(self, fleet_id, expeditions):
        """Initializes the ExpeditionFleet object, an extension of the Fleet
        class.

        Args:
            fleet_id (int): id of the fleet
            expeditions (list): list of expeditions this expedition fleet
                can be sent to
        """
        self.fleet_id = fleet_id
        self.expeditions = expeditions
        self.expedition = None
        self.expedition_area = None
        self.expedition_duration = None
        self.dispatch_fleet_time = datetime.now()
        self.return_time = datetime.now()

    def choose_expedition(self):
        """Method to randomly choose one of the expeditions specified in the
        expedition fleet's valid expedition list
        """
        self.expedition = choice(self.expeditions)
        expedition_info = get_expedition_info(self.expedition)
        self.expedition_area = expedition_info['area']
        self.expedition_duration = expedition_info['duration']

    def dispatch_fleet(self):
        """Method to set the proper flags of the ExpeditionFleet instance once
        it has been sent on an expedition. Does not actually interact with the
        game itself.
        """
        self.dispatch_fleet_time = datetime.now()
        self.return_time = self.dispatch_fleet_time + self.expedition_duration
        self.at_base = False
        self.needs_resupply = False

    def update_return_time(self, hours, minutes):
        """Method to update the ExpeditionFleet's expected return time relative
        to the current time.

        Args:
            hours (int): delta of number of hours
            minutes (int): delta of number of minutes
        """
        self.dispatch_fleet_time = datetime.now()
        self.return_time = self.dispatch_fleet_time + timedelta(
            hours=hours, minutes=minutes)
        self.at_base = False
        self.needs_resupply = False


def get_expedition_info(expedition):
    """Function to return the relevant information for the specified
    expedition.

    Args:
        expedition (int): expedition to get information for

    Returns:
        dict: dict with the expedition's world/area and completion duration
    """
    if expedition == 1:
        return {
            'area': 1,
            'duration': timedelta(minutes=14, seconds=30)}
    elif expedition == 2:
        return {
            'area': 1,
            'duration': timedelta(minutes=29, seconds=30)}
    elif expedition == 3:
        return {
            'area': 1,
            'duration': timedelta(minutes=19, seconds=30)}
    elif expedition == 4:
        return {
            'area': 1,
            'duration': timedelta(minutes=49, seconds=30)}
    elif expedition == 5:
        return {
            'area': 1,
            'duration': timedelta(hours=1, minutes=29, seconds=30)}
    elif expedition == 6:
        return {
            'area': 1,
            'duration': timedelta(minutes=39, seconds=30)}
    elif expedition == 7:
        return {
            'area': 1,
            'duration': timedelta(minutes=59, seconds=30)}
    elif expedition == 8:
        return {
            'area': 1,
            'duration': timedelta(hours=2, minutes=59, seconds=30)}
    elif expedition == 9:
        return {
            'area': 2,
            'duration': timedelta(hours=3, minutes=59, seconds=30)}
    elif expedition == 10:
        return {
            'area': 2,
            'duration': timedelta(hours=1, minutes=29, seconds=30)}
    elif expedition == 11:
        return {
            'area': 2,
            'duration': timedelta(hours=4, minutes=59, seconds=30)}
    elif expedition == 12:
        return {
            'area': 2,
            'duration': timedelta(hours=7, minutes=59, seconds=30)}
    elif expedition == 13:
        return {
            'area': 2,
            'duration': timedelta(hours=3, minutes=59, seconds=30)}
    elif expedition == 14:
        return {
            'area': 2,
            'duration': timedelta(hours=5, minutes=59, seconds=30)}
    elif expedition == 15:
        return {
            'area': 2,
            'duration': timedelta(hours=11, minutes=59, seconds=30)}
    elif expedition == 16:
        return {
            'area': 2,
            'duration': timedelta(hours=14, minutes=59, seconds=30)}
    elif expedition == 17:
        return {
            'area': 3,
            'duration': timedelta(minutes=44, seconds=30)}
    elif expedition == 18:
        return {
            'area': 3,
            'duration': timedelta(hours=4, minutes=59, seconds=30)}
    elif expedition == 19:
        return {
            'area': 3,
            'duration': timedelta(hours=5, minutes=59, seconds=30)}
    elif expedition == 20:
        return {
            'area': 3,
            'duration': timedelta(hours=1, minutes=59, seconds=30)}
    elif expedition == 21:
        return {
            'area': 3,
            'duration': timedelta(hours=2, minutes=19, seconds=30)}
    elif expedition == 22:
        return {
            'area': 3,
            'duration': timedelta(hours=2, minutes=59, seconds=30)}
    elif expedition == 23:
        return {
            'area': 3,
            'duration': timedelta(hours=3, minutes=59, seconds=30)}
    elif expedition == 24:
        return {
            'area': 3,
            'duration': timedelta(hours=8, minutes=19, seconds=30)}
    elif expedition == 25:
        return {
            'area': 4,
            'duration': timedelta(hours=39, minutes=59, seconds=30)}
    elif expedition == 26:
        return {
            'area': 4,
            'duration': timedelta(hours=79, minutes=59, seconds=30)}
    elif expedition == 27:
        return {
            'area': 4,
            'duration': timedelta(hours=19, minutes=59, seconds=30)}
    elif expedition == 28:
        return {
            'area': 4,
            'duration': timedelta(hours=24, minutes=59, seconds=30)}
    elif expedition == 29:
        return {
            'area': 4,
            'duration': timedelta(hours=23, minutes=59, seconds=30)}
    elif expedition == 30:
        return {
            'area': 4,
            'duration': timedelta(hours=47, minutes=59, seconds=30)}
    elif expedition == 31:
        return {
            'area': 4,
            'duration': timedelta(hours=1, minutes=59, seconds=30)}
    elif expedition == 32:
        return {
            'area': 4,
            'duration': timedelta(hours=23, minutes=59, seconds=30)}
    elif expedition == 33:
        return {
            'area': 5,
            'duration': timedelta(minutes=15, seconds=30)}
    elif expedition == 34:
        return {
            'area': 5,
            'duration': timedelta(minutes=29, seconds=30)}
    elif expedition == 35:
        return {
            'area': 5,
            'duration': timedelta(hours=6, minutes=59, seconds=30)}
    elif expedition == 36:
        return {
            'area': 5,
            'duration': timedelta(hours=8, minutes=59, seconds=30)}
    elif expedition == 37:
        return {
            'area': 5,
            'duration': timedelta(hours=2, minutes=44, seconds=30)}
    elif expedition == 38:
        return {
            'area': 5,
            'duration': timedelta(hours=2, minutes=54, seconds=30)}
    elif expedition == 39:
        return {
            'area': 5,
            'duration': timedelta(hours=29, minutes=59, seconds=30)}
    elif expedition == 40:
        return {
            'area': 5,
            'duration': timedelta(hours=6, minutes=49, seconds=30)}
    elif expedition == 9998:
        return {
            'area': 'event',
            'duration': timedelta(minutes=15)}
    elif expedition == 9999:
        return {
            'area': 'event',
            'duration': timedelta(minutes=30)}
    else:
        return {
            'area': 1,
            'duration': timedelta(minutes=29, seconds=30)}
