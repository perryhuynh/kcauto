from sikuli import Pattern
from threading import Thread
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
