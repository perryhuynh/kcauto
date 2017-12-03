from sikuli import App, Region, Location, Pattern, Key
from time import sleep
from util import Util


class Recovery(object):
    """Recovery module that contains kcauto-kai's recover method (basic, WIP)
    """

    @staticmethod
    def recover(kcauto_kai, e):
        """Attempts very basic recovery actions on a FindFailed exception. WIP
        and does not integrate with the config.

        Args:
            kcauto_kai (KCAutoKai): KCAutoKai instance
            e (Exception): Exception

        Returns:
            bool: True on successful recovery, otherwise raises an error
        """
        kc_region = kcauto_kai.kc_region
        basic_recovery_enabled = True
        recovery_method = 'kc3'

        App.focus(kcauto_kai.config.program)
        kc_region.mouseMove(Location(0, 0))

        if basic_recovery_enabled:
            type(Key.ESC)
            sleep(1)
            if kc_region.exists(Pattern('home_menu_sortie.png').exact()):
                kcauto_kai.stats.increment_recoveries()
                return True
        if kc_region.exists('catbomb.png') and recovery_method != 'None':
            if recovery_method == 'browser':
                Region.type(Key.F5)
            elif recovery_method == 'kc3':
                Region.type(Key.F5)
                sleep(1)
                Region.type(Key.SPACE)
                sleep(1)
                Region.type(Key.TAB)
                sleep(1)
                Region.type(Key.SPACE)
            elif recovery_method == 'kcv':
                Region.type(Key.F5)
            elif recovery_method == 'kct':
                Region.type(Key.ALT)
                sleep(1)
                Region.type(Key.DOWN)
                sleep(1)
                Region.type(Key.DOWN)
                sleep(1)
                Region.type(Key.ENTER)
            elif recovery_method == 'eo':
                Region.type(Key.F5)
                sleep(1)
                Region.type(Key.TAB)
                sleep(1)
                Region.type(Key.SPACE)
            sleep(3)
            kc_region.mouseMove(Location(0, 0))
            sleep(3)
            Util.wait_and_click(
                kc_region, Pattern('game_start.png').similar(0.999), 60)
            sleep(5)
            Util.log_success("Recovery successful")
            kcauto_kai.stats.increment_recoveries()
            return True
        Util.log_error("Irrecoverable crash")
        print(e)
        raise
