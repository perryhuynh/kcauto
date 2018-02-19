from sikuli import Pattern
from random import choice
from datetime import datetime, timedelta
from threading import Thread
from expedition import get_expedition_info
from util import Util


class Fleet(object):
    """Base Fleet class, extended by ExpeditionFleet and CombatFleet in the
    Expedition and Combat modules, respectively.

    Attributes:
        at_base (bool): specifies whether or not the fleet is currently at base
            and not conducting a sortie
        fleet_id (int): id of the fleet, 1~4
        needs_resupply (bool): specifies whether or not the fleet needs to be
            resupplied
    """

    fleet_id = None
    at_base = True
    needs_resupply = False

    def __init__(self, id):
        """Initializes the Fleet object.

        Args:
            id (int): id of the fleet
        """
        self.fleet_id = id

    def print_state(self):
        """Method to print the at_base and needs_resupply state of the fleet.
        """
        Util.log_msg("Fleet {}: at base '{}' needs resupply '{}'".format(
            self.fleet_id, self.at_base, self.needs_resupply))
        Util.log_msg(self.damage_counts)

    def check_supplies(self, region):
        """Method to multithread the detection of fleet supply states
        pre-expedition or pre-sortie.

        Args:
            region (Region): Region in which to search for the supply states

        Returns:
            bool: False if the fleet needs resupply, True otherwise
        """
        thread_check_alert = Thread(
            target=self._check_supplies_func, args=('', region))
        thread_check_alert_red = Thread(
            target=self._check_supplies_func, args=('_red', region))
        Util.multithreader([thread_check_alert, thread_check_alert_red])

        if self.needs_resupply:
            Util.log_warning("Fleet needs resupply!")
            self.at_base = True
            return False
        return True

    def _check_supplies_func(self, type, region):
        """Child multithreaded method for checking supply states.

        Args:
            type (str): which supply state to check for
            region (Region): Region in which to search for the supply state
        """
        if region.exists('resupply_alert{}.png'.format(type)):
            self.needs_resupply = True

    @staticmethod
    def switch(region, fleet):
        """Method that switches to the specified fleet by pressing the fleet
        icon in the specified region.

        Args:
            region (Region): sikuli Region in which to search for the fleet
                icons
            fleet (int): id of fleet to switch to
        """
        Util.wait_and_click_and_wait(
            region, Pattern('fleet_{}.png'.format(fleet)).exact(),
            region, Pattern('fleet_{}_active.png'.format(fleet)).exact())
        Util.kc_sleep()


class CombatFleet(Fleet):
    def __init__(self, fleet_id):
        """Initializes the CombatFleet object, an extension of the Fleet class.

        Args:
            fleet_id (int): id of the fleet
        """
        self.fleet_id = fleet_id
        self.flagship_damaged = False
        self.damage_counts = {}
        self.damaged_fcf_retreat_count = 0
        self.fatigue = {}

    def reset_fcf_retreat_counts(self):
        """Method for setting the fleet's damaged FCF retreat counter.
        """
        self.damaged_fcf_retreat_count = 0

    def resolve_fcf_retreat_counts(self):
        """Method for resolving the fleet's damaged FCF retreat counter by
        adding it back to the damage counter at the end of a sortie.
        """
        self.damage_counts['heavy'] += self.damaged_fcf_retreat_count
        self.reset_fcf_retreat_counts()

    def increment_fcf_retreat_count(self):
        """Method to increment the FCF retreat count if there is only one
        heavily damaged ship in the fleet, and decrement the heavy damage from
        the damage counter.
        """
        if 'heavy' in self.damage_counts and self.damage_counts['heavy'] == 1:
            Util.log_msg(
                "Retreating damaged ship via FCF from fleet {}."
                .format(self.fleet_id))
            self.damaged_fcf_retreat_count += 1
            self.damage_counts['heavy'] -= 1

    def print_damage_counts(self):
        """Method to report the fleet's damage counts in a more human-readable
        format
        """
        Util.log_msg(
            "Fleet {} damage counts: {} heavy / {} moderate / {} minor"
            .format(
                self.fleet_id, self.damage_counts['heavy'],
                self.damage_counts['moderate'], self.damage_counts['minor']))

    def print_fatigue_states(self):
        """Method to report the fleet's fatigue state in a more human-readable
        format
        """
        fatigue = 'Rested'
        if self.fatigue['high']:
            fatigue = 'High'
        elif self.fatigue['medium']:
            fatigue = 'Medium'
        Util.log_msg(
            "Fleet {} fatigue state: {}".format(self.fleet_id, fatigue))

    def get_damage_counts_at_threshold(self, threshold, counts={}):
        """Method for returning the number of ships at and below the specified
        damage threshold

        Args:
            threshold (str): the cutoff damage threshold
            counts (dict, optional): optionally passed in damage counts; if not
                specified, the fleet's internally stored damage counter is used
                to calculate the number

        Returns:
            int: the number of ships at or below the damage threshold
        """
        counts = counts if counts else self.damage_counts
        if not counts:
            # counts not initialized; return 0
            return 0

        valid_damages = self.get_damages_at_threshold(threshold)

        count = 0
        for damage in valid_damages:
            count += counts[damage]

        return count

    def check_damages(self, region, reset=True):
        """Method to multithread the detection of damage states of the fleet.

        Args:
            region (Region): Region in which to search for the damage states

        Returns:
            dict: dict of counts of the different damage states
        """
        thread_check_damages_heavy = Thread(
            target=self._check_damages_func, args=('heavy', region, reset))
        thread_check_damages_moderate = Thread(
            target=self._check_damages_func, args=('moderate', region, reset))
        thread_check_damages_minor = Thread(
            target=self._check_damages_func, args=('minor', region, reset))
        Util.multithreader([
            thread_check_damages_heavy, thread_check_damages_moderate,
            thread_check_damages_minor])
        return self.damage_counts

    def _check_damages_func(self, type, region, reset):
        """Child multithreaded method for checking damage states.

        Args:
            type (str): which damage state to check for
            region (Region): Region in which to search for the damage state
        """
        if reset:
            self.damage_counts[type] = 0

        dmg_img = 'ship_state_dmg_{}.png'.format(type)
        count = Util.findAll_wrapper(
            region, Pattern(dmg_img).similar(Globals.DAMAGE_SIMILARITY))

        for i in count:
            self.damage_counts[type] += 1

    def check_damages_7th(self, regions):
        """Method that specifically checks the damage in the 7th ship spot
        of the fleet during the pre-sortie damage check.

        Args:
            regions (dict): dict of pre-defined kcauto-kai regions

        Returns:
            dict: dict of counts of the different damage states, including that
                of the 7th ship
        """
        self.check_damages(regions['check_damage'])
        Util.click_preset_region(regions, '7th_next')
        return self.check_damages(regions['check_damage_7th'], reset=False)

    def check_damage_flagship(self, regions):
        """Method that checks whether or not the flagship of the fleet is
        damaged in the post-combat results screen. Important for ascertaining
        whether or not the flagship of the escort fleet is the ship with heavy
        damage as it is not sinkable.

        Args:
            regions (dict): dict of pre-defined kcauto-kai regions
        """
        if (regions['check_damage_flagship'].exists(Pattern(
                'ship_state_dmg_heavy.png').similar(
                    Globals.FATIGUE_SIMILARITY))):
            self.flagship_damaged = True

    def check_fatigue(self, region):
        """Method to multithread the detection of fatigue states of the fleet.

        Args:
            region (Region): Region in which to search for the fatigue states

        Returns:
            dict: dict of bools of the different fatigue states
        """
        thread_check_low_fatigue = Thread(
            target=self._check_fatigue_func, args=('medium', region))
        thread_check_high_fatigue = Thread(
            target=self._check_fatigue_func, args=('high', region))
        Util.multithreader([
            thread_check_low_fatigue, thread_check_high_fatigue])
        return self.fatigue

    def _check_fatigue_func(self, mode, region):
        """Child multithreaded method for checking fatigue states.

        Args:
            type (str): which fatigue state to check for
            region (Region): Region in which to search for the fatigue state
        """
        self.fatigue[mode] = (
            True
            if (region.exists(Pattern('ship_state_fatigue_{}.png'.format(mode))
                .similar(Globals.FATIGUE_SIMILARITY)))
            else False)

    @staticmethod
    def get_damages_at_threshold(threshold):
        """Method for returning the list of valid damages given a threshold.

        Args:
            threshold (str): the cutoff damage threshold

        Returns:
            list: list of valid damages (heavy, moderate, minor)
        """
        valid_damages = ('heavy', 'moderate', 'minor')
        return valid_damages[:valid_damages.index(threshold) + 1]


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
